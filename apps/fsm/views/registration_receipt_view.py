from django.contrib.auth.models import AnonymousUser
from django.db import transaction
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied, NotFound, ParseError
from rest_framework.mixins import RetrieveModelMixin, DestroyModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from errors.error_codes import serialize_error
from apps.fsm.models import RegistrationReceipt
from apps.fsm.permissions import IsRegistrationReceiptOwner, IsReceiptsFormModifier
from apps.fsm.serializers.answer_sheet_serializers import RegistrationReceiptSerializer, RegistrationStatusSerializer
from apps.fsm.serializers.certificate_serializer import create_certificate
from proxies.sms_system.sms_service_proxy import SMSServiceProxy


class RegistrationReceiptViewSet(GenericViewSet, RetrieveModelMixin, DestroyModelMixin):
    serializer_class = RegistrationReceiptSerializer
    queryset = RegistrationReceipt.objects.all()
    my_tags = ['registration']

    def get_permissions(self):
        if self.action in ['destroy', 'get_certificate']:
            permission_classes = [IsRegistrationReceiptOwner]
        elif self.action == 'retrieve':
            permission_classes = [
                IsRegistrationReceiptOwner | IsReceiptsFormModifier]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super().get_serializer_class()

    def get_queryset(self):
        user = self.request.user
        if isinstance(user, AnonymousUser):
            return RegistrationReceipt.objects.none()
        return self.queryset

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update(
            {'domain': self.request.build_absolute_uri('/api/'[:-5])})
        return context

    @swagger_auto_schema(responses={200: RegistrationReceiptSerializer})
    @action(detail=True, methods=['post'], serializer_class=RegistrationStatusSerializer)
    @transaction.atomic
    def validate(self, request, pk=None):
        receipt = self.get_object()
        if self.request.user not in receipt.form.program_or_fsm.modifiers:
            raise PermissionDenied(serialize_error('4061'))
        # if not self.request.user.school_studentship.is_document_verified:
        #     raise PermissionDenied(serialize_error('4062'))
        status_serializer = RegistrationStatusSerializer(
            data=self.request.data)
        if status_serializer.is_valid(raise_exception=True):
            registration_status = status_serializer.data.get(
                'status', RegistrationReceipt.RegistrationStatus.Waiting)

            if registration_status == RegistrationReceipt.RegistrationStatus.Accepted:
                program = receipt.form.program
                if program.is_free:
                    receipt.is_participating = True
            else:
                receipt.is_participating = False

            older_status = receipt.status

            receipt.status = registration_status
            receipt.save()

            # todo: fix sending sms on registration receipt status change
            # # todo: fix academy name
            # if older_status != receipt.status:
            #     sms_service_proxy = SMSServiceProxy(provider='kavenegar')
            #     sms_service_proxy.send_otp(
            #         receptor_phone_number=receipt.user.phone_number,
            #         action=sms_service_proxy.RegularSMSTypes.UpdateRegistrationReceiptState,
            #         # todo: get real academy name from mps
            #         token='کاموا',
            #         token2=receipt.form.program_or_fsm.name
            #     )

            return Response(
                RegistrationReceiptSerializer(
                    context=self.get_serializer_context()).to_representation(receipt),
                status=status.HTTP_200_OK)

    @swagger_auto_schema(tags=my_tags + ['certificates'])
    @action(detail=True, methods=['get'])
    def get_certificate(self, request, pk=None):
        receipt = self.get_object()
        if not receipt.form.has_certificate or not receipt.form.certificates_ready:
            raise ParseError(serialize_error('4098'))
        if receipt.certificate:
            receipt.certificate.storage.delete(receipt.certificate.name)
        certificate_templates = receipt.form.certificate_templates.all()
        # filter templates accordingly to user performance
        if len(certificate_templates) > 0:
            receipt.certificate = create_certificate(
                certificate_templates.first(), request.user.full_name)
            receipt.save()
        else:
            raise NotFound(serialize_error('4095'))
        return Response(RegistrationReceiptSerializer(context=self.get_serializer_context()).to_representation(receipt),
                        status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def my_receipt(self, request, pk=None):
        form_id = request.GET.get('form')
        user = request.user
        answer_sheet = None
        try:
            answer_sheet = user.answer_sheets.get(form__id=form_id)
            return Response(RegistrationReceiptSerializer(answer_sheet).data)
        except:
            return Response({})
