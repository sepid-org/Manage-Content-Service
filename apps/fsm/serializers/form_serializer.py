from apps.fsm.models.form import Form
from apps.fsm.serializers.papers.paper_serializer import PaperSerializer


class FormSerializer(PaperSerializer):

    class Meta(PaperSerializer.Meta):
        model = Form
        ref_name = 'registration_form'
        fields = PaperSerializer.Meta.get_fields() + \
            ['audience_type', 'start_date', 'end_date']
        read_only_fields = PaperSerializer.Meta.read_only_fields + []
