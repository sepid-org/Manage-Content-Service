from rest_polymorphic.serializers import PolymorphicSerializer

from apps.fsm.models import DetailBoxWidget, Iframe, Video, Image, TextWidget, SmallAnswerProblem, MultiChoiceProblem, UploadFileProblem, BigAnswerProblem, Aparat, Audio, BoxWidget
from apps.widgets.serializers.content_widgets.content_widget_serializers\
    import AudioSerializer, BoxWidgetSerializer, DetailBoxWidgetSerializer, TextWidgetSerializer, ImageSerializer, VideoSerializer, AparatSerializer, \
    IframeSerializer
from apps.widgets.serializers.question_widgets.question_widget_serializers \
    import SmallAnswerProblemSerializer, BigAnswerProblemSerializer, MultiChoiceProblemSerializer, UploadFileProblemSerializer


class WidgetPolymorphicSerializer(PolymorphicSerializer):
    model_serializer_mapping = {
        # Widget
        TextWidget: TextWidgetSerializer,
        Image: ImageSerializer,
        Video: VideoSerializer,
        Audio: AudioSerializer,
        Aparat: AparatSerializer,
        Iframe: IframeSerializer,
        BoxWidget: BoxWidgetSerializer,
        DetailBoxWidget: DetailBoxWidgetSerializer,
        # Question,
        SmallAnswerProblem: SmallAnswerProblemSerializer,
        BigAnswerProblem: BigAnswerProblemSerializer,
        MultiChoiceProblem: MultiChoiceProblemSerializer,
        UploadFileProblem: UploadFileProblemSerializer,
    }

    resource_type_field_name = 'widget_type'
