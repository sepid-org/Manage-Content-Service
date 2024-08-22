from rest_framework.exceptions import ParseError, PermissionDenied
from rest_framework import serializers
from apps.fsm.models import Player

from apps.accounts.serializers.user_serializer import MentorSerializer
from apps.fsm.serializers.content_serializer import ContentSerializer
from apps.sales.serializers.merchandise import MerchandiseSerializer
from errors.error_codes import serialize_error
from apps.fsm.models import Program, RegistrationReceipt, FSM, Edge, Team
from apps.fsm.serializers.paper_serializers import StateSerializer, StateSimpleSerializer


class FSMMinimalSerializer(ContentSerializer):

    class Meta:
        model = FSM
        fields = ['id', 'name', 'description', 'cover_page', 'is_active', 'is_visible',
                  'fsm_learning_type', 'fsm_p_type', 'order_in_program']

    def to_representation(self, instance):
        representation = super(FSMMinimalSerializer,
                               self).to_representation(instance)
        user = self.context.get('user', None)
        representation['players_count'] = len(
            Player.objects.filter(fsm=instance))
        representation['is_mentor'] = user in instance.mentors.all()
        return representation


class FSMSerializer(serializers.ModelSerializer):
    merchandise = MerchandiseSerializer(required=False)
    mentors = MentorSerializer(many=True, read_only=True)
    first_state = StateSerializer(read_only=True)

    def validate(self, attrs):
        program = attrs.get('program', None)
        team_size = attrs.get('team_size', None)
        merchandise = attrs.get('merchandise', None)
        registration_form = attrs.get('registration_form', None)
        fsm_p_type = attrs.get('fsm_p_type', FSM.FSMPType.Individual)
        creator = self.context.get('user', None)
        if program:
            if merchandise or registration_form:
                raise ParseError(serialize_error('4069'))
            if fsm_p_type == FSM.FSMPType.Team:
                if program.participation_type == Program.ParticipationType.INDIVIDUAL:
                    raise ParseError(serialize_error('4071'))
                if team_size and team_size != program.team_size:
                    raise ParseError(serialize_error('4072'))
            if creator not in program.modifiers:
                raise ParseError(serialize_error('4073'))
        else:
            if fsm_p_type == FSM.FSMPType.Team and team_size is None:
                raise ParseError(serialize_error('4074'))
        return attrs

    def create(self, validated_data):
        creator = self.context.get('user', None)
        merchandise = validated_data.pop('merchandise', None)
        team_size = validated_data.get('team_size', None)
        program = validated_data.get('program', None)
        fsm_p_type = validated_data.get('fsm_p_type')
        if team_size is None and program and fsm_p_type != FSM.FSMPType.Individual:
            validated_data['team_size'] = program.team_size

        instance = super(FSMSerializer, self).create(
            {'creator': creator, **validated_data})

        if merchandise and merchandise.get('name', None) is None:
            merchandise['name'] = validated_data.get('name', 'unnamed_program')
            serializer = MerchandiseSerializer(data=merchandise)
            if serializer.is_valid(raise_exception=True):
                merchandise_instance = serializer.save()
                instance.merchandise = merchandise_instance
                instance.save()
        return instance

    def to_representation(self, instance):
        representation = super(FSMSerializer, self).to_representation(instance)
        user = self.context.get('user', None)
        player = user.players.filter(is_active=True, fsm=instance).first()
        representation['is_mentor'] = user in instance.mentors.all()
        representation['player'] = player.id if player else 'NotStarted'
        representation['state'] = player.current_state.name if player and player.current_state else 'NotStarted'
        representation['last_visit'] = player.last_visit if player else 'NotStarted'
        if player and player.receipt.team:
            representation['team'] = player.receipt.team.id
            if player.receipt.team.team_head:
                representation['team_head_name'] = player.receipt.team.team_head.user.full_name
                representation['is_team_head'] = player.receipt.team.team_head.id == player.receipt.id
        else:
            representation['team'] = 'TeamNotCreatedYet'
            representation['team_head_name'] = None
            representation['is_team_head'] = False

        return representation

    class Meta:
        model = FSM
        fields = '__all__'
        read_only_fields = ['id', 'creator', 'mentors',
                            'first_state', 'registration_form', 'is_mentor', 'is_manager']


class EdgeSerializer(ContentSerializer):

    def validate(self, attrs):
        user = self.context.get('user', None)
        tail = attrs.get('tail', None)
        head = attrs.get('head', None)
        if tail.fsm != head.fsm:
            raise ParseError(serialize_error('4076'))

        if user not in tail.fsm.mentors.all():
            raise PermissionDenied(serialize_error('4075'))

        return super(EdgeSerializer, self).validate(attrs)

    def to_representation(self, instance):
        representation = super(
            EdgeSerializer, self).to_representation(instance)
        representation['tail'] = StateSimpleSerializer(
            context=self.context).to_representation(instance.tail)
        representation['head'] = StateSimpleSerializer(
            context=self.context).to_representation(instance.head)
        representation['str'] = str(instance)
        return representation

    class Meta:
        model = Edge
        fields = '__all__'
        read_only_fields = ['id']


class KeySerializer(serializers.Serializer):
    key = serializers.CharField(max_length=10, required=False)


class TeamGetSerializer(serializers.Serializer):
    team = serializers.PrimaryKeyRelatedField(
        queryset=Team.objects.all(), required=True)
