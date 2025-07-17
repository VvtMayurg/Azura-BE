from django.db import models

class ProviderGroupLocationStatusChoices(models.TextChoices):
    ACTIVE = "Active"
    INACTIVE = "Inactive"
    PENDING = "Pending"
    SUSPENDED = "Suspended"

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
