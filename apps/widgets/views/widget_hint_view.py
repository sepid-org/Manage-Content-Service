from rest_framework import viewsets

from apps.fsm.models import WidgetHint
from apps.fsm.models.base import Paper
from apps.widgets.serializers.widget_hint_serializer import WidgetHintSerializer


class WidgetHintViewSet(viewsets.ModelViewSet):
    serializer_class = WidgetHintSerializer
    queryset = WidgetHint.objects.all()
    my_tags = ['state']

    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super().get_serializer_class()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'user': self.request.user})
        context.update(
            {'domain': self.request.build_absolute_uri('/api/')[:-5]})
        return context

    def create(self, request, *args, **kwargs):
        request.data['paper_type'] = Paper.PaperType.WidgetHint
        return super().create(request, *args, **kwargs)
