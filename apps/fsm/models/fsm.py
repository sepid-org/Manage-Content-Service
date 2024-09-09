from django.db import models, transaction
from apps.accounts.models import User

from apps.attributes.models import Attribute
from apps.fsm.models.base import Content, Paper
from apps.fsm.models.program import Program


class FSMManager(models.Manager):
    @transaction.atomic
    def create(self, **args):
        fsm = super().create(**args)
        fsm.mentors.add(fsm.creator)
        fsm.save()
        return fsm


class FSM(models.Model, Content):
    class FSMLearningType(models.TextChoices):
        Supervised = 'Supervised'
        Unsupervised = 'Unsupervised'

    class FSMPType(models.TextChoices):
        Team = 'Team'
        Individual = 'Individual'
        Hybrid = 'Hybrid'

    is_public = models.BooleanField(default=False)

    attributes = models.ManyToManyField(to=Attribute, null=True, blank=True)

    website = models.CharField(blank=True, null=True, max_length=50)

    program = models.ForeignKey(Program, on_delete=models.SET_NULL, related_name='fsms', default=None, null=True,
                                blank=True)
    registration_form = models.OneToOneField('fsm.RegistrationForm', related_name='fsm', on_delete=models.SET_NULL, null=True,
                                             blank=True)
    creator = models.ForeignKey('accounts.User', related_name='created_fsms', on_delete=models.SET_NULL, null=True,
                                blank=True)
    mentors = models.ManyToManyField(
        'accounts.User', related_name='fsms', blank=True)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    cover_page = models.URLField()
    is_active = models.BooleanField(default=True)
    is_visible = models.BooleanField(default=True)
    first_state = models.OneToOneField('fsm.State', null=True, blank=True, on_delete=models.SET_NULL,
                                       related_name='my_fsm')
    fsm_learning_type = models.CharField(max_length=40, default=FSMLearningType.Unsupervised,
                                         choices=FSMLearningType.choices)
    fsm_p_type = models.CharField(
        max_length=40, default=FSMPType.Individual, choices=FSMPType.choices)
    team_size = models.IntegerField(default=3)
    order_in_program = models.IntegerField(default=0)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    objects = FSMManager()

    def __str__(self):
        return self.name

    @transaction.atomic
    def clone(self):
        cloned_fsm = FSM(
            name=self.name,
            description=self.description,
            cover_page=self.cover_page,
            is_active=self.is_active,
            fsm_learning_type=self.fsm_learning_type,
            fsm_p_type=self.fsm_p_type,
            team_size=self.team_size,
        )

        cloned_states = {}
        cloned_fsm.save()
        for tail_state in self.states.all():
            for outward_edge in tail_state.outward_edges.all():
                if tail_state.id not in cloned_states:
                    cloned_states[tail_state.id] = tail_state.clone(cloned_fsm)

                head_state = outward_edge.head
                if head_state.id not in cloned_states:
                    cloned_states[head_state.id] = head_state.clone(cloned_fsm)

                cloned_outward_edge = outward_edge.clone(cloned_states[tail_state.id],
                                                         cloned_states[head_state.id])

        cloned_fsm.first_state = cloned_states[self.first_state.id]
        cloned_fsm.save()

    def get_fsm(fsm_id: int):
        return FSM.objects.filter(id=fsm_id).first()


class Player(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    user = models.ForeignKey(
        User, related_name='players', on_delete=models.CASCADE)
    fsm = models.ForeignKey(FSM, related_name='players',
                            on_delete=models.CASCADE)

    receipt = models.ForeignKey(
        'fsm.RegistrationReceipt', related_name='players', on_delete=models.CASCADE)

    current_state = models.ForeignKey('fsm.State', null=True, blank=True, on_delete=models.SET_NULL,
                                      related_name='players')
    last_visit = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    @property
    def team(self):
        return self.receipt.team if self.receipt else None

    @staticmethod
    def get_player(player_id: int):
        return Player.objects.filter(id=player_id).first()

    class Meta:
        unique_together = ('user', 'fsm', 'receipt')

    def __str__(self):
        return f'{self.user.full_name} in {self.fsm.name}'


class State(Paper):
    class StateTemplate(models.TextChoices):
        normal = 'normal'
        board = 'board'

    name = models.TextField(null=True, blank=True)
    fsm = models.ForeignKey(
        FSM, on_delete=models.CASCADE, related_name='states')
    template = models.CharField(max_length=20, default=StateTemplate.normal,
                                choices=StateTemplate.choices)

    @transaction.atomic
    def delete(self):
        try:
            if self.my_fsm:
                fsm = self.fsm
                fsm.first_state = fsm.states.exclude(id=self.id).first()
                fsm.save()
        except:
            pass
        return super(State, self).delete()

    def clone(self, fsm):
        cloned_state = clone_paper(self, fsm=fsm)
        cloned_widgets = [widget.clone(cloned_state)
                          for widget in self.widgets.all()]
        cloned_hints = [hint.clone(cloned_state) for hint in self.hints.all()]
        return cloned_state

    def __str__(self):
        return f'گام: {self.name} | کارگاه: {str(self.fsm)}'


class Edge(models.Model, Content):
    attributes = models.ManyToManyField(to=Attribute, null=True, blank=True)

    tail = models.ForeignKey(
        State, on_delete=models.CASCADE, related_name='outward_edges')
    head = models.ForeignKey(
        State, on_delete=models.CASCADE, related_name='inward_edges')
    is_back_enabled = models.BooleanField(default=True)
    priority = models.IntegerField(null=True, blank=True)
    is_visible = models.BooleanField(default=False)
    text = models.TextField(null=True, blank=True)

    class Meta:
        unique_together = ('tail', 'head')

    @property
    def fsm(self):
        return self.head.fsm

    def clone(self, tail, head):
        cloned_edge = Edge(
            tail=tail,
            head=head,
            is_back_enabled=self.is_back_enabled,
            is_visible=self.is_visible,
        )
        cloned_edge.save()
        return cloned_edge

    def __str__(self):
        return f'از {self.tail.name} به {self.head.name}'


class PlayerTransition(models.Model):
    player = models.ForeignKey(
        Player, on_delete=models.SET_NULL, null=True, related_name='player_transitions')
    source_state = models.ForeignKey(
        State, on_delete=models.SET_NULL, null=True, related_name='player_departure_transitions')
    target_state = models.ForeignKey(
        State, on_delete=models.SET_NULL, null=True, related_name='player_arrival_transitions')
    time = models.DateTimeField(null=True)
    transited_edge = models.ForeignKey(
        Edge, related_name='player_transitions', null=True, on_delete=models.SET_NULL)

    def is_edge_transited_in_reverse(self):
        return True  # todo: fix


class PlayerStateHistory(models.Model):
    player = models.ForeignKey(
        Player, on_delete=models.SET_NULL, null=True, related_name='player_state_histories')
    state = models.ForeignKey(
        State, on_delete=models.SET_NULL, null=True, related_name='player_state_histories')
    arrival = models.ForeignKey(
        PlayerTransition, on_delete=models.SET_NULL, null=True, related_name='player_target_state_history')
    departure = models.ForeignKey(
        PlayerTransition, on_delete=models.SET_NULL, null=True, related_name='player_source_state_history')

    def __str__(self):
        return f'{self.player} - {self.state.name if self.state else "DELETED"}'
