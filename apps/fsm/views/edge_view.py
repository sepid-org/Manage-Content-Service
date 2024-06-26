import logging

from django.db import transaction
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.exceptions import ParseError, PermissionDenied
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from errors.error_codes import serialize_error
from apps.fsm.models import Edge, FSM, Team
from apps.fsm.permissions import IsEdgeModifier
from apps.fsm.serializers.fsm_serializers import EdgeSerializer, KeySerializer, TeamGetSerializer
from apps.fsm.serializers.player_serializer import PlayerStateSerializer
from apps.fsm.utils import get_a_random_player_from_team, get_player, transit_player_in_fsm, transit_team_in_fsm

logger = logging.getLogger(__name__)


class EdgeViewSet(ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Edge.objects.all()
    serializer_class = EdgeSerializer
    my_tags = ['edge']

    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super().get_serializer_class()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'user': self.request.user})
        return context

    def get_permissions(self):
        if self.action in ['create', 'retrieve', 'list', 'transit_player_on_edge', 'go_backward']:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [IsEdgeModifier]
        return [permission() for permission in permission_classes]

    @swagger_auto_schema(responses={200: PlayerStateSerializer}, tags=['player'])
    @transaction.atomic
    @action(detail=True, methods=['post'], serializer_class=KeySerializer)
    def transit_player_on_edge(self, request, pk):
        edge = self.get_object()
        fsm = edge.fsm
        user = request.user
        player = get_player(user, fsm)

        if player is None:
            raise ParseError(serialize_error('4082'))

        if not edge.is_visible:
            raise PermissionDenied(serialize_error('4087'))

        # check password:
        if edge.lock and len(edge.lock) > 0:
            password = request.data.get('password', None)
            if not password:
                raise PermissionDenied(serialize_error('4085'))
            elif edge.lock != password:
                raise PermissionDenied(serialize_error('4084'))

        if fsm.fsm_p_type == FSM.FSMPType.Team:
            team = player.team
            if player.receipt.id != team.team_head.id:
                raise ParseError(serialize_error('4089'))
            if player.current_state == edge.tail:
                transit_team_in_fsm(team, fsm, edge.tail, edge.head, edge)
                player = get_a_random_player_from_team(team, fsm)
            return Response(PlayerStateSerializer(player).data, status=status.HTTP_200_OK)

        elif fsm.fsm_p_type == FSM.FSMPType.Individual:
            if player.current_state == edge.tail:
                player = transit_player_in_fsm(
                    player, edge.tail, edge.head, edge)

            return Response(PlayerStateSerializer(player).data,
                            status=status.HTTP_200_OK)

    @swagger_auto_schema(responses={200: PlayerStateSerializer}, tags=['mentor'])
    @transaction.atomic
    @action(detail=True, methods=['post'], serializer_class=TeamGetSerializer)
    def mentor_move_forward(self, request, pk):
        edge = self.get_object()
        fsm = edge.tail.fsm
        serializer = TeamGetSerializer(
            data=request.data, context=self.get_serializer_context())
        serializer.is_valid(raise_exception=True)
        team: Team = serializer.validated_data['team']
        transit_team_in_fsm(team, fsm, edge.tail, edge.head, edge)
        player = get_a_random_player_from_team(team, fsm)

        return Response(PlayerStateSerializer(player).data, status=status.HTTP_200_OK)
