import uuid
import pytz
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models, transaction
from django.contrib.auth.models import AbstractUser
from datetime import timedelta, datetime
from polymorphic.managers import PolymorphicManager
from polymorphic.models import PolymorphicModel

from apps.sales.validators import percentage_validator
from manage_content_service.settings.base import VOUCHER_CODE_LENGTH, DISCOUNT_CODE_LENGTH, PURCHASE_UNIQ_CODE_LENGTH
from proxies.sms_system.settings import SMS_CODE_DELAY, SMS_CODE_LENGTH
from proxies.sms_system.sms_service_proxy import SMSServiceProxy


class User(AbstractUser):
    class Gender(models.TextChoices):
        Male = 'Male'
        Female = 'Female'

    id = models.UUIDField(primary_key=True, unique=True,
                          default=uuid.uuid4, editable=False)
    phone_number = models.CharField(
        max_length=15, blank=True, null=True, unique=True)
    # national code should not be unique, due it's not validated
    national_code = models.CharField(max_length=10, null=True, blank=True)
    profile_picture = models.URLField(blank=True, null=True, max_length=2000)
    bio = models.CharField(max_length=300, blank=True, null=True)
    gender = models.CharField(max_length=10, null=True,
                              blank=True, choices=Gender.choices)
    birth_date = models.DateField(null=True, blank=True)

    country = models.CharField(max_length=50, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    province = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    postal_code = models.CharField(max_length=10, null=True, blank=True)
    is_artificial = models.BooleanField(default=False)

    def get_user_website(self, website):
        try:
            return self.user_websites.get(website=website)
        except:
            return None

    def get_receipt(self, form):
        from apps.fsm.models import RegistrationReceipt
        try:
            return RegistrationReceipt.objects.get(user=self, form=form)
        except:
            return None

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return self.username


class UserWebsite(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name='user_websites')
    website = models.CharField(max_length=50)
    password = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now=True)

    def set_password(self, new_password):
        from django.contrib.auth.hashers import make_password
        self.password = make_password(new_password)
        self.save()

    class Meta:
        unique_together = ('user', 'website')

    def __str__(self):
        return f'{self.user} | {self.website}'


class UserWebsiteLogin(models.Model):
    datetime = models.DateTimeField(auto_now=True)
    user_website = models.ForeignKey(to=UserWebsite, on_delete=models.CASCADE)


class InstituteManager(PolymorphicManager):
    @transaction.atomic
    def create(self, **args):
        institute = super().create(**args)
        institute.owner = institute.creator
        institute.admins.add(institute.creator)
        # ct = ContentType.objects.get_for_model(institute)
        # assign_perm(Permission.objects.filter(codename='add_admin', content_type=ct).first(), institute.owner, institute)
        # these permission settings worked correctly but were too messy
        institute.save()
        return institute


class EducationalInstitute(PolymorphicModel):
    class InstituteType(models.TextChoices):
        School = 'School'
        University = 'University'
        Other = 'Other'

    name = models.CharField(max_length=100, null=False, blank=False)
    institute_type = models.CharField(
        max_length=10, null=False, blank=False, choices=InstituteType.choices)
    address = models.CharField(max_length=100, null=True, blank=True)
    province = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    postal_code = models.CharField(max_length=10, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    contact_info = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateField(null=True, blank=True)

    is_approved = models.BooleanField(null=True, blank=True)
    date_added = models.DateField(auto_now_add=True)
    owner = models.ForeignKey(User, related_name='owned_institutes',
                              on_delete=models.SET_NULL, null=True, blank=True)
    creator = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)
    admins = models.ManyToManyField(
        User, related_name='institutes', blank=True)

    objects = InstituteManager()

    class Meta:
        permissions = [
            ('add_admin', 'Can add new admins to educational institute')
        ]

    def __str__(self):
        return self.name


class School(EducationalInstitute):
    class Gender(models.TextChoices):
        Male = 'Male'
        Female = 'Female'

    class SchoolType(models.Choices):
        Elementary = 'Elementary'
        JuniorHigh = 'JuniorHigh'
        High = 'High'
        SchoolOfArt = 'SchoolOfArt'

    principal_name = models.CharField(max_length=30, null=True, blank=True)
    principal_phone = models.CharField(max_length=15, null=True, blank=True)
    school_type = models.CharField(
        max_length=15, null=True, blank=True, choices=SchoolType.choices)
    gender_type = models.CharField(
        max_length=10, null=True, blank=True, choices=Gender.choices, default='Male')


class University(EducationalInstitute):
    pass


class Studentship(PolymorphicModel):
    class StudentshipType(models.Choices):
        School = 'School'
        Academic = 'Academic'

    studentship_type = models.CharField(
        max_length=10, null=False, blank=False, choices=StudentshipType.choices)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    document = models.FileField(
        upload_to='studentship_documents/', null=True, blank=True)
    is_document_verified = models.BooleanField(default=False)


class SchoolStudentship(Studentship):
    class Major(models.TextChoices):
        Math = 'Math'
        Biology = 'Biology'
        Literature = 'Literature'
        IslamicStudies = 'IslamicStudies'
        TechnicalTraining = 'TechnicalTraining'
        Others = 'Others'

    school = models.ForeignKey(
        School, related_name='students', on_delete=models.SET_NULL, null=True)
    grade = models.IntegerField(null=True, blank=True, validators=[
                                MaxValueValidator(12), MinValueValidator(0)])
    major = models.CharField(max_length=25, null=True,
                             blank=True, choices=Major.choices)
    user = models.OneToOneField(
        User, related_name='school_studentship', on_delete=models.CASCADE, null=False)


class AcademicStudentship(Studentship):
    class Degree(models.TextChoices):
        BA = 'BA'
        MA = 'MA'
        PHD = 'PHD'
        Postdoc = 'Postdoc'

    university = models.ForeignKey(
        University, related_name='academic_students', on_delete=models.SET_NULL, null=True)
    degree = models.CharField(max_length=15, null=True,
                              blank=True, choices=Degree.choices)
    university_major = models.CharField(max_length=30, null=True, blank=True)
    user = models.OneToOneField(
        User, related_name='academic_studentship', on_delete=models.CASCADE, null=False)


class Player(models.Model):
    user = models.ForeignKey(
        User, related_name='workshops', on_delete=models.CASCADE)
    fsm = models.ForeignKey(
        'fsm.FSM', related_name='users', on_delete=models.CASCADE)
    # purchase = models.ForeignKey('accounts.Purchase', related_name='purchase', on_delete=models.SET_NULL, null=True)
    # registration_receipt = models.ForeignKey('fsm.RegistrationReceipt', on_delete=models.SET_NULL, null=True, blank=True)
    scores = models.JSONField(null=True, blank=True)
    is_active = models.BooleanField(default=True)


# class OwnableMixin(models.Model):
#     owners = models.ManyToManyField(User, related_name='owned_entities')
#
#     # TODO - work on its details
#     class Meta:
#         abstract = True


class Merchandise(models.Model):
    id = models.UUIDField(primary_key=True, unique=True,
                          default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    price = models.IntegerField()
    discounted_price = models.IntegerField(null=True)
    is_active = models.BooleanField(default=True)
    program = models.ForeignKey(
        to='fsm.Program', on_delete=models.CASCADE, related_name='merchandises', null=True)


# class Code(models.Model):
#     TODO - create a 'code' class  and subclass discounts, vouchers & verification codes from it.
#     class CodeType(models.TextChoices):
#         DISCOUNT_CODE = 'DISCOUNT_CODE'
#         VOUCHER = 'VOUCHER'
#         VERIFICATION_CODE = 'VERIFICATION_CODE'
#
#     code_type = models.CharField(max_length=15, choices=CodeType.choices, blank=False, null=False)
#     code = models.CharField(max_length=10, null=False, blank=False)


class DiscountCodeManager(models.Manager):
    @transaction.atomic
    def create_discount_code(self, **args):

        code = User.objects.make_random_password(length=DISCOUNT_CODE_LENGTH)
        return super().create(**{'code': code, **args})


# TODO - add date validators for datetime fields
class DiscountCode(models.Model):
    code = models.CharField(max_length=10, unique=True,
                            null=False, blank=False)
    value = models.FloatField(null=False, blank=False,
                              validators=[percentage_validator])
    expiration_date = models.DateTimeField(blank=True, null=True)
    remaining = models.IntegerField(default=1)
    user = models.ForeignKey(User, related_name='discount_codes', on_delete=models.CASCADE, null=True, blank=True,
                             default=None)
    merchandise2 = models.ManyToManyField(
        to=Merchandise, related_name='discount_codes')

    objects = DiscountCodeManager()

    def __str__(self):
        return self.code + " " + str(self.value)

    @staticmethod
    def calculate_discount(value, price):
        return ((price * (1 - value) + 50) // 100) * 100


class VoucherManager(models.Manager):
    @transaction.atomic
    def create_voucher(self, **args):
        code = User.objects.make_random_password(length=VOUCHER_CODE_LENGTH)
        return super().create(**{'remaining': args.get('amount', 0), 'code': code, **args})


class Voucher(models.Model):
    user = models.ForeignKey(
        User, related_name='vouchers', on_delete=models.CASCADE, null=False)
    code = models.CharField(max_length=10, null=False)
    amount = models.IntegerField(null=False)
    remaining = models.IntegerField(null=False)
    expiration_date = models.DateTimeField(blank=True, null=True)
    is_valid = models.BooleanField(default=True)

    objects = VoucherManager()

    @transaction.atomic
    def use_on_purchase(self, purchase):
        # TODO - work on how purchase flow is.
        #  Eg. can users use a discount and a voucher or just one of them?
        if self.remaining >= purchase.merchandise.price:
            purchase.amount = max(0, purchase.amount - self.remaining)
            self.remaining -= purchase.merchandise.price
        else:
            purchase.amount = purchase.merchandise.price - self.remaining
            self.remaining = 0
        purchase.voucher = self
        purchase.save()
        self.save()


class PurchaseManager(models.Manager):
    @transaction.atomic
    def create_purchase(self, **args):
        uniq_code = User.objects.make_random_password(
            length=PURCHASE_UNIQ_CODE_LENGTH)
        return super(PurchaseManager, self).create(**{'uniq_code': uniq_code, **args})


class Purchase(models.Model):
    class Status(models.TextChoices):
        Success = "Success"
        Repetitious = "Repetitious"
        Failed = "Failed"
        Started = "Started"

    ref_id = models.CharField(blank=True, max_length=100, null=True)
    amount = models.IntegerField()
    authority = models.CharField(blank=True, max_length=37, null=True)
    status = models.CharField(
        blank=False, default=Status.Started, choices=Status.choices, max_length=25)
    created_at = models.DateTimeField(auto_now_add=True)
    uniq_code = models.CharField(blank=False, max_length=100, default="")
    callback_domain = models.CharField(blank=True, null=True, max_length=100)

    user = models.ForeignKey(
        User, related_name='purchases', on_delete=models.CASCADE)

    merchandise = models.ForeignKey(
        Merchandise, related_name='purchases', on_delete=models.SET_NULL, null=True)
    voucher = models.ForeignKey(Voucher, related_name='purchases', on_delete=models.SET_NULL, null=True,
                                blank=True, default=None)
    discount_code = models.ForeignKey(DiscountCode, related_name='purchases', on_delete=models.SET_NULL, null=True,
                                      blank=True, default=None)

    objects = PurchaseManager()

    @property
    def registration_receipt(self):
        return self.merchandise.program_or_fsm.registration_form.registration_receipts.filter(user=self.user).last()

    def __str__(self):
        return f'{self.uniq_code}-{self.merchandise}-{self.amount}-{self.status}'


class VerificationCodeManager(models.Manager):
    @transaction.atomic
    def create_verification_code(self, phone_number, time_zone='Asia/Tehran'):
        code = User.objects.make_random_password(
            length=SMS_CODE_LENGTH, allowed_chars='1234567890')
        other_codes = VerificationCode.objects.filter(
            phone_number=phone_number, is_valid=True)
        for c in other_codes:
            c.is_valid = False
            c.save()
        verification_code = VerificationCode.objects.create(code=code, phone_number=phone_number,
                                                            expiration_date=datetime.now(pytz.timezone(time_zone)) +
                                                            timedelta(minutes=SMS_CODE_DELAY))
        return verification_code


class VerificationCode(models.Model):
    class VerificationType(models.TextChoices):
        CreateUserAccount = 'create-user-account'
        ChangeUserPassword = 'change-user-password'
        ChangeUserPhoneNumber = 'change-user-phone-number'

    # todo: set verification code while sending verification code
    verification_type = models.CharField(
        blank=False, null=True, choices=VerificationType.choices, max_length=30)
    phone_number = models.CharField(blank=True, max_length=13, null=True)
    code = models.CharField(blank=True, max_length=10, null=True)
    expiration_date = models.DateTimeField(blank=False, null=False)
    is_valid = models.BooleanField(default=True)

    objects = VerificationCodeManager()

    def notify(self, verification_type, party_display_name='سپید'):
        sms_service_proxy = SMSServiceProxy(provider='kavenegar')
        sms_service_proxy.send_otp(
            receptor_phone_number=self.phone_number,
            action=verification_type,
            token=party_display_name,
            token2=str(self.code)
        )

    def __str__(self):
        return f'{self.phone_number}\'s code is: {self.code} {"+" if self.is_valid else "-"}'


# ----------------------------------------------

class MemberManager(BaseUserManager):
    pass


class Member(AbstractBaseUser):
    objects = MemberManager()
    username = models.CharField(
        unique=True, max_length=15, blank=True, null=True)
    is_participant = models.BooleanField(default=True)
    is_mentor = models.BooleanField(default=False)
    is_program_owner = models.BooleanField(default=False)
    first_name = models.CharField(max_length=15, blank=True, null=True)
    last_name = models.CharField(max_length=15, blank=True, null=True)
    email = models.CharField(max_length=15, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    school = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=20, null=True, blank=True)
    document = models.FileField(upload_to='documents/', null=True, blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True,
                              default='Male')
    grade = models.CharField(max_length=15, null=True, blank=True,
                             default='ONE')
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []
    is_anonymous = False
    is_authenticated = False

    class Meta:
        db_table = "auth_user"

    def __str__(self):
        return self.username
