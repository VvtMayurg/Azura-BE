from django.db import models


class ProviderGroupLocationStatusChoices(models.TextChoices):
    ACTIVE = "Active"
    INACTIVE = "Inactive"
    PENDING = "Pending"
    SUSPENDED = "Suspended"


class ProviderGroupTypeChoices(models.TextChoices):
    HOSPITAL_SYSTEM = "Hospital System"
    PRIMARY_CARE = "Primary Care"
    SPECIALTY_CARE = "Specialty Care"
    URGENT_CARE = "Urgent Care"


class DisciplineChoices(models.TextChoices):
    ACUPUNCTURE = "Acupuncture"
    ADMINISTRATIVE = "Administrative"
    ATHLETIC_THERAPY = "Athletic Therapy"
    AUDIOLOGY = "Audiology"
    AYURVEDA = "Ayurveda"
    CHINESE_MEDICINE = "Chinese Medicine"
    CHIROPODY = "Chiropody"
    CHIROPRACTIC = "Chiropractic"
    COACHING = "Coaching"
    COLONICS = "Colonics"
    CONSULTING = "Consulting"
    COUNSELLING = "Counselling"
    DAY_SPA = "Day Spa"
    DENTISTRY = "Dentistry"
    DERMATOLOGY = "Dermatology"
    DIETETICS = "Dietetics"
    FLOATING = "Floating"
    FOOT_CARE_NURSING = "Foot Care Nursing"
    FUNCTIONAL_MEDICINE = "Functional Medicine"
    HOMEOPATHY = "Homeopathy"
    IV_THERAPY = "IV Therapy"
    IMAGING = "Imaging"
    KINESIOLOGY = "Kinesiology"
    LASER_SKIN_HAIR = "Laser Skin + Hair"
    MASSAGE_THERAPY = "Massage Therapy"
    MEDICAL_PRIMARY_CARE = "Medical - Primary Care / Family Medicine"
    MEDICAL_AESTHETICS = "Medical Aesthetics"
    MEDICAL_SPECIALISTS = "Medical Specialists"
    MIDWIFERY = "Midwifery"
    NATUROPATHIC_MEDICINE = "Naturopathic Medicine"
    NUTRITION = "Nutrition"
    OCCUPATIONAL_THERAPY = "Occupational Therapy"
    OPTOMETRY = "Optometry"
    OSTEOPATHY = "Osteopathy"
    PERSONAL_TRAINING = "Personal Training"
    PHYSICAL_THERAPY = "Physical Therapy"
    PHYSIOTHERAPY = "Physiotherapy"
    PILATES = "Pilates"
    PLASTIC_SURGERY = "Plastic Surgery"
    PODIATRY = "Podiatry"
    PSYCHIATRY = "Psychiatry"
    PSYCHOLOGY = "Psychology / Mental Health"
    PSYCHOTHERAPY = "Psychotherapy"
    REFLEXOLOGY = "Reflexology"
    RESPIRATORY = "Respiratory"
    SPEECH_THERAPY = "Speech Therapy"
    WEIGHT_MANAGEMENT = "Weight Management"
    WOMENS_HEALTH = "Women's Health"
    YOGA = "Yoga"
    UNKNOWN = "I can't find my discipline"


class EmailConfigurationProtocolChoices(models.TextChoices):
    TLS = "TLS"
    SSL = "SSL"


class SMSConfigurationProviderChoices(models.TextChoices):
    TWILLIO = "Twillio"


class CommunicationTemplateTypeChoices(models.TextChoices):
    SMS = "SMS"
    EMAIL = "Email"


class CommunicationTemplateUserTypeChoices(models.TextChoices):
    ADMIN = "Admin"
    PROVIDER = "Provider"
    PATIENT = "Patient"
    ALL = "All"


class GenderChoices(models.TextChoices):
    MALE = "Male"
    FEMALE = "Female"
    OTHER = "Other"
    UNKNOWN = "Unknown"


class DayChoices(models.TextChoices):
    MND = "Monday"
    TSD = "Tuesday"
    WND = "Wednesday"
    TD = "Thrusday"
    FRD = "Friday"
    STD = "Saturday"
    SND = "Sunday"


class EducationFormTypeChoices(models.TextChoices):
    USER = "User"
    PATIENT = "Patient"
    ALL = "All"


class ProgramChoices(models.TextChoices):
    CCM = "CCM"
    PCM = "PCM"
    BHI = "BHI"
    RPM = "RPM"


class TaskPriorityChoices(models.TextChoices):
    HIGH = "High"
    LOW = "Low"
    MEDIUM = "Medium"


class AppointmentTypeChoices(models.TextChoices):
    FOLLOW_UP = "Follow-Up"
    NEW = "New"


class AppointmentVisitTypeChoices(models.TextChoices):
    IN_PERSON = "In Person"
    VIRTUAL = "Virtual"


class AppointmentStatusChoices(models.TextChoices):
    SCHEDULED = "Scheduled"
    PENDING = "Pending"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"
    NOT_SHOW = "Not Show"
    DECLINED = "Declined"


class EncounterStatusChoice(models.TextChoices):
    PLANED = "Planed"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"


class CommunicationMessageType(models.TextChoices):
    IN_APP = "In App"
    EMAIL = "Email"
    SMS_TEXT = "SMS/Text"


class NotificationCategoryChoices(models.TextChoices):
    APPOINTMENT = "Appointments"
    PATIENT_MESSAGE = "Patient Messages"
    SCHEDULE = "Schedule Changes"
    SECURITY = "Security Alerts"
    PROFILE = "Profile Updates"
    SYSTEM = "System Updates"


class ReminderTypeChoices(models.TextChoices):
    APPOINTMENT = "Appointment"
    FOLLOW_UP = "Follow-up"
    MEDICATION = "Medication"
    LAB_RESULT = "Lab Result"


class DocumentCategoryChoices(models.TextChoices):
    CLINICAL = "Clinical"
    CONSENT = "Consent"
    REFERRAL = "Referral"
    LAB_RESULT = "Lab Result"
    AMENDMENT = "Amendment"
    OTHER = "Other"


class VisitNoteTypeChoices(models.TextChoices):
    SIMPLE = "Simple"
    SOAP = "SOAP"
    HP1 = "H&p Note1"
    HP2 = "H&p Note2"
    HP_AP = "H&p Note (2 column - A/P)"
    PRE_OP = "Pre-OP Notes"


class NoteTypeChoices(models.TextChoices):
    PHONE_NOTE = "Phone Note"
    NON_VISIT_NOTE = "Non Visit Notes"
    EMAIL = "Email Notes"
    POINT_OF_CARE = "Point of Care Labs"


class QuestionTypeChoices(models.TextChoices):
    FREE_TEXT = "Free Text"
    SINGLE_SELECT = "Single Select"
    MULTI_SELECT = "Multi Select"
    FILE_UPLOAD = "File Upload"
