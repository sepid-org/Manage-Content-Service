from rest_framework.exceptions import ParseError
from rest_framework import serializers

from apps.fsm.serializers.program_contact_info_serializer import ProgramContactInfoSerializer
from apps.fsm.utils import add_admin_to_program
from errors.error_codes import serialize_error
from apps.fsm.models import Program, RegistrationForm


class ProgramSummarySerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        representation = super(ProgramSummarySerializer,
                               self).to_representation(instance)
        representation['initial_participants_count'] = len(instance.initial_participants)
        representation['final_participants_count'] = len(instance.final_participants)
        return representation

    class Meta:
        model = Program
        fields = ['id', 'slug', 'cover_page', 'name', 'description', 'participation_type',
                  'is_visible', 'is_active', 'team_size', 'is_free']


class ProgramSerializer(serializers.ModelSerializer):
    program_contact_info = ProgramContactInfoSerializer(required=False)

    def create(self, validated_data):
        registration_form = RegistrationForm.objects.create(
            **{'paper_type': RegistrationForm.PaperType.RegistrationForm})

        creator = self.context.get('user', None)
        program = super(ProgramSerializer, self).create(
            {'creator': creator, 'registration_form': registration_form, **validated_data})

        add_admin_to_program(creator, program)

        program.registration_form = registration_form
        program.save()
        return program

    def update(self, instance, validated_data):
        program_contact_info = validated_data.pop('program_contact_info', None)
        program_contact_info_instance = instance.program_contact_info
        instance = super().update(instance, validated_data)
        if program_contact_info:
            if program_contact_info_instance:
                program_contact_info_serializer = ProgramContactInfoSerializer(
                    program_contact_info_instance, data=program_contact_info, partial=True)
            else:
                program_contact_info_serializer = ProgramContactInfoSerializer(
                    data=program_contact_info)
            program_contact_info_serializer.is_valid(raise_exception=True)
            program_contact_info_instance = program_contact_info_serializer.save()
            instance.program_contact_info = program_contact_info_instance
            instance.save()
        return instance

    def validate(self, attrs):
        team_size = attrs.get('team_size', 0)
        participation_type = attrs.get(
            'participation_type', Program.ParticipationType.INDIVIDUAL)
        if (team_size > 0 and participation_type != Program.ParticipationType.TEAM) or (
                participation_type == Program.ParticipationType.TEAM and team_size <= 0):
            raise ParseError(serialize_error('4074'))
        return attrs

    def to_representation(self, instance):
        representation = super(
            ProgramSerializer, self).to_representation(instance)
        registration_form = instance.registration_form
        representation['initial_participants_count'] = len(instance.initial_participants)
        representation['final_participants_count'] = len(instance.final_participants)
        representation['has_certificate'] = registration_form.has_certificate
        representation['certificates_ready'] = registration_form.certificates_ready
        representation['registration_start_date'] = registration_form.start_date
        representation['registration_end_date'] = registration_form.end_date
        representation['audience_type'] = registration_form.audience_type
        representation['is_free'] = instance.is_free        
        return representation

    class Meta:
        model = Program
        fields = '__all__'
        read_only_fields = ['id', 'creator', 'is_approved',
                            'registration_form', 'program_contact_info']
