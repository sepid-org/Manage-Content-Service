from django.db import transaction
from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied, ParseError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import AnonymousUser

from apps.accounts.serializers.user_serializer import UserSerializer
from apps.accounts.utils import find_user_in_website
from apps.fsm.pagination import StandardPagination
from errors.error_codes import serialize_error
from apps.fsm.models import RegistrationReceipt, FSM, PlayerStateHistory, Player, RegistrationReceipt, Problem
from apps.fsm.permissions import FSMMentorPermission, HasActiveRegistration
from apps.fsm.serializers.fsm_serializers import FSMMinimalSerializer, FSMSerializer, KeySerializer, EdgeSerializer, TeamGetSerializer
from apps.fsm.serializers.paper_serializers import StateSimpleSerializer, EdgeSimpleSerializer
from apps.fsm.serializers.player_serializer import PlayerSerializer, PlayerStateSerializer
from apps.fsm.serializers.widgets.mock_widget_serializer import MockWidgetSerializer
from apps.fsm.serializers.widgets.widget_polymorphic_serializer import WidgetPolymorphicSerializer
from apps.fsm.utils import get_player, get_receipt, get_a_player_from_team, _get_fsm_edges, register_user_in_program, transit_player_in_fsm
from utilities.cache_enabled_model_viewset import CacheEnabledModelViewSet


class FSMViewSet(CacheEnabledModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = FSM.objects.filter(is_deleted=False)
    ordering_fields = ['order_in_program']
    ordering = ['-order_in_program']
    serializer_class = FSMSerializer
    my_tags = ['fsm']
    filterset_fields = ['website']
    pagination_class = StandardPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        program_slug = self.request.query_params.get('program', None)
        if program_slug is not None:
            queryset = queryset.filter(program__slug=program_slug)
        return queryset

    def get_permissions(self):
        if self.action in ['partial_update', 'update', 'destroy', 'add_mentor', 'get_states', 'get_edges',
                           'get_player_from_team', 'activate', 'players']:
            permission_classes = [FSMMentorPermission]
        elif self.action in ['enter', 'review']:
            permission_classes = [HasActiveRegistration]
        else:
            permission_classes = self.permission_classes
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action in ['players']:
            return PlayerSerializer
        if self.action in ['list']:
            return FSMMinimalSerializer
        else:
            return super().get_serializer_class()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'user': self.request.user})
        return context

    @swagger_auto_schema(responses={200: PlayerSerializer}, tags=['player'])
    @transaction.atomic
    @action(detail=True, methods=['post'], serializer_class=KeySerializer)
    def enter_fsm(self, request, pk=None):
        fsm = self.get_object()
        user = request.user

        if fsm.is_public:
            if isinstance(user, AnonymousUser):
                pass

        password = self.request.data.get('password', None)
        receipt = get_receipt(user, fsm)
        is_mentor = user in fsm.mentors.all()

        if receipt is None:
            raise ParseError(serialize_error('4079'))

        if fsm.fsm_p_type in [FSM.FSMPType.Team, FSM.FSMPType.Hybrid]:
            if receipt.team is None:
                raise ParseError(serialize_error('4078'))

        if not fsm.first_state:
            raise ParseError(serialize_error('4111'))

        if not fsm.first_state.is_user_permitted(user):
            raise ParseError(serialize_error('4108'))

        if fsm.entrance_lock and password != fsm.entrance_lock:
            raise PermissionDenied(serialize_error('4080'))

        player = get_player(user, fsm)

        # first time entering fsm
        if not player:
            serializer = PlayerSerializer(data={'user': user.id, 'fsm': fsm.id, 'receipt': receipt.id,
                                                'current_state': fsm.first_state.id, 'last_visit': timezone.now()},
                                          context=self.get_serializer_context())
            serializer.is_valid(raise_exception=True)
            player = serializer.save()
            transit_player_in_fsm(
                player=player, source_state=None, target_state=fsm.first_state, edge=None)

        # if any state has been deleted and player has no current state:
        if player.current_state is None:
            player.current_state = fsm.first_state
            player.save()

        return Response(status=status.HTTP_202_ACCEPTED)

    @swagger_auto_schema(responses={200: PlayerSerializer}, tags=['player'])
    @transaction.atomic
    @action(detail=True, methods=['get'], serializer_class=KeySerializer)
    def current_user_fsm_player(self, request, pk=None):
        fsm = self.get_object()
        user = request.user
        player = get_player(user, fsm)
        return Response(PlayerStateSerializer(player).data, status=status.HTTP_200_OK)

    @swagger_auto_schema(responses={200: MockWidgetSerializer}, tags=['player', 'fsm'])
    @transaction.atomic
    @action(detail=True, methods=['get'])
    def review(self, request, pk):
        problems = Problem.objects.filter(
            paper__in=self.get_object().states.filter(is_exam=True))
        return Response(WidgetPolymorphicSerializer(problems, context=self.get_serializer_context(), many=True).data,
                        status=status.HTTP_200_OK)

    @swagger_auto_schema(responses={200: PlayerSerializer}, tags=['mentor'])
    @transaction.atomic
    @action(detail=True, methods=['get'])
    def players(self, request, pk):
        gender = request.query_params.get('gender', None)
        first_name = request.query_params.get('first_name', None)
        last_name = request.query_params.get('last_name', None)

        queryset = self.get_object().players.all()
        queryset = queryset.filter(
            user__gender=gender) if gender is not None else queryset
        queryset = queryset.filter(
            user__first_name__startswith=first_name) if first_name is not None else queryset
        queryset = queryset.filter(
            user__first_name__startswith=last_name) if last_name is not None else queryset

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(
                page, many=True, context=self.get_serializer_context())
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(
            queryset, many=True, context=self.get_serializer_context())
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(responses={200: StateSimpleSerializer}, tags=['mentor'])
    @transaction.atomic
    @action(detail=True, methods=['get'])
    def get_states(self, request, pk):
        return Response(data=StateSimpleSerializer(self.get_object().states.order_by('id'), context=self.get_serializer_context(),
                                                   many=True).data, status=status.HTTP_200_OK)

    @swagger_auto_schema(responses={200: EdgeSimpleSerializer}, tags=['mentor'])
    @action(detail=True, methods=['get'])
    def get_edges(self, request, pk):
        edges = _get_fsm_edges(self.get_object())
        return Response(data=EdgeSerializer(edges, context=self.get_serializer_context(), many=True).data,
                        status=status.HTTP_200_OK)

    @swagger_auto_schema(responses={200: UserSerializer(many=True)}, tags=['mentor'])
    @transaction.atomic
    @action(detail=True, methods=['get'])
    def get_mentors(self, request, pk):
        mentors = self.get_object().mentors
        return Response(data=UserSerializer(mentors, many=True).data)

    @swagger_auto_schema(responses={200: FSMSerializer}, tags=['mentor'])
    @action(detail=True, methods=['post'], serializer_class=UserSerializer, permission_classes=[FSMMentorPermission, ])
    def add_mentor(self, request, pk=None):
        fsm = self.get_object()
        account_serializer = UserSerializer(data=request.data)
        account_serializer.is_valid(raise_exception=True)
        new_mentor = find_user_in_website(
            user_data={**account_serializer.validated_data},
            website=request.data.get("website"),
            raise_exception=True,
        )
        fsm.mentors.add(new_mentor)
        register_user_in_program(new_mentor, fsm.program)
        return Response()

    @swagger_auto_schema(responses={200: FSMSerializer}, tags=['mentor'])
    @action(detail=True, methods=['post'], serializer_class=UserSerializer, permission_classes=[FSMMentorPermission, ])
    def remove_mentor(self, request, pk=None):
        fsm = self.get_object()
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        removed_mentor = find_user_in_website(
            user_data={**serializer.validated_data}, website=request.data.get("website"))
        if removed_mentor == fsm.creator:
            raise ParseError(serialize_error('5006'))
        if removed_mentor in fsm.mentors.all():
            fsm.mentors.remove(removed_mentor)
        return Response()

    @swagger_auto_schema(responses={200: PlayerSerializer}, tags=['mentor'])
    @action(detail=True, methods=['post'], serializer_class=TeamGetSerializer)
    def get_player_from_team(self, request, pk):
        fsm = self.get_object()
        serializer = TeamGetSerializer(
            data=self.request.data, context=self.get_serializer_context())
        if serializer.is_valid(raise_exception=True):
            team = serializer.validated_data['team']
            player = get_a_player_from_team(team, fsm)
        return Response(PlayerSerializer(context=self.get_serializer_context()).to_representation(player),
                        status=status.HTTP_200_OK)

    @transaction.atomic
    @action(detail=True, methods=['get'])
    def activate(self, request, pk=None):
        f = self.get_object()
        previous_players = len(f.players.all())
        for r in RegistrationReceipt.objects.filter(is_participating=True):
            if len(Player.objects.filter(user=r.user, fsm=f, receipt=r)) <= 0:
                p = Player.objects.create(user=r.user, fsm=f, receipt=r, current_state=f.first_state,
                                          last_visit=timezone.now())
                PlayerStateHistory.objects.create(
                    player=p, state=f.first_state, start_time=p.last_visit)

        return Response(data={'new_players_count': len(f.players.all()), 'previous_players_count': previous_players},
                        status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'])
    def soft_delete(self, request, pk=None):
        fsm = self.get_object()
        fsm.is_deleted = True
        fsm.deleted_at = timezone.now()
        fsm.save()
        self.cache.invalidate_list_cache()
        return Response()
