from rest_framework import serializers
from timezone_field.rest_framework import TimeZoneSerializerField

from azura_be.base.serializers import AddressSerializer
from azura_be.base.serializers import Base64FileField
from azura_be.patients.models import EmailSMS
from azura_be.patients.models import Patient
from azura_be.provider_groups.apis.serializers import ProviderGroupRelatedSerializer
from azura_be.users.apis.serializers import UserRelatedSerializer


class PatientRelatedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ("id", "first_name", "last_name", "email", "phone")


class PatientCreateSerializer(serializers.ModelSerializer):
    address = AddressSerializer(required=False)
    picture = Base64FileField(
        file_types=["jpg", "jpeg", "png", "svg"],
        max_file_size=5,
        required=False,
        write_only=True,
    )

    class Meta:
        model = Patient
        fields = (
            "first_name",
            "last_name",
            "date_of_birth",
            "gender",
            "mrn",
            "provider_group",
            "email",
            "phone",
            "primary_provider",
            "active",
            "address",
            "picture",
        )


class PatientGetSerializer(serializers.ModelSerializer):
    provider_group = ProviderGroupRelatedSerializer()
    primary_provider = UserRelatedSerializer()
    timezone = TimeZoneSerializerField()

    class Meta:
        model = Patient
        fields = "__all__"


class EmailSMSCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailSMS
        fields = ("type", "subject", "content")

    def validate(self, attrs):
        if attrs.get("type") == "EMAIL" and not attrs.get("subject"):
            raise serializers.ValidationError({"subject": "Subject is required for email"})
        return super().validate(attrs)


class EmailSMSSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailSMS
        fields = ("id", "created_at", "subject", "content")
        
    
    
    
class column1Serializers(serializers.Serializer):
    created_at = serializers.DateTimeField(read_only=True)
    
    NOTE_CHOICES = [
        ('Office-note', 'Office-note'),
        ('progress-note', 'progress-note'),
        ('followup-note', 'followup-note'),
    ]
    DOCTOR_CHOICES=[
        
        ('Dr.James JOne','Dr.James JOne'),
        ('Dr.Smith','Dr.Smith'),
        ('Dr.Emily','Dr.Emily'),
    ]
    
    note = serializers.ChoiceField(choices=NOTE_CHOICES)
    
    doctor_name = serializers.ChoiceField(choices=DOCTOR_CHOICES)
    time_with_patients = serializers.DurationField()
    exam_reason = serializers.CharField()
    
    allergies = serializers.CharField(max_length=255, allow_blank=True)
    past_medical_history = serializers.CharField(max_length=255, allow_blank=True)
    past_surgical_history = serializers.CharField(max_length=255, allow_blank=True)
    family_history = serializers.CharField(allow_blank=True)
    social_history = serializers.CharField(allow_blank=True)
    habits = serializers.CharField(allow_blank=True)
    current_medication = serializers.CharField(allow_blank=True)
    review_of_system = serializers.CharField(allow_blank=True)
    followup = serializers.CharField(allow_blank=True)

    transition_of_care = serializers.BooleanField(default=False)
    received_from_other_setting_or_provider = serializers.BooleanField(default=False)
    referring_to_other_setting_or_provider = serializers.BooleanField(default=False)
    keep_this_confidential = serializers.BooleanField(default=False)

class column2Serializers(serializers.Serializer):
    created_at = serializers.DateTimeField(read_only=True)
    
    NOTE_CHOICES = [
        ('SOAP', 'SOAP'),
        ('Follow-up', 'Follow-up'),
        ('Discharge', 'Discharge'),
    ]
    DOCTOR_CHOICES=[
        
        ('Dr.James JOne','Dr.James JOne'),
        ('Dr.Smith','Dr.Smith'),
        ('Dr.Emily','Dr.Emily'),
    ]
    
    note = serializers.ChoiceField(choices=NOTE_CHOICES)
    
    doctor_name = serializers.ChoiceField(choices=DOCTOR_CHOICES)
    time_with_patients = serializers.DurationField()
    
    allergies = serializers.CharField(max_length=255, allow_blank=True)
    past_medical_history = serializers.CharField(max_length=255, allow_blank=True)
    past_surgical_history = serializers.CharField(max_length=255, allow_blank=True)
    family_history = serializers.CharField(allow_blank=True)
    social_history = serializers.CharField(allow_blank=True)
    habits = serializers.CharField(allow_blank=True)
    current_medication = serializers.CharField(allow_blank=True)
    review_of_system = serializers.CharField(allow_blank=True)
    followup = serializers.CharField(allow_blank=True)

    transition_of_care = serializers.BooleanField(default=False)
    received_from_other_setting_or_provider = serializers.BooleanField(default=False)
    referring_to_other_setting_or_provider = serializers.BooleanField(default=False)
    keep_this_confidential = serializers.BooleanField(default=False)
    
    
    
    
class CBCSerializer(serializers.Serializer):
    hematocrit = serializers.FloatField()  
    hemoglobin = serializers.FloatField()  
    mcv = serializers.FloatField()         
    platelets = serializers.FloatField()
    rbc = serializers.FloatField()
    wbc = serializers.FloatField()


class CMPSerializer(serializers.Serializer):  
    ag_ratio = serializers.FloatField()
    albumin = serializers.FloatField()
    alkaline_phosphatase = serializers.FloatField()
    alt = serializers.FloatField()
    ast = serializers.FloatField()
    bilirubin_total = serializers.FloatField()
    bun = serializers.FloatField()
    bun_creatinine_ratio = serializers.FloatField()
    calcium = serializers.FloatField()
    carbon_dioxide = serializers.FloatField()
    chloride = serializers.FloatField()
    creatinine = serializers.FloatField()
    egfr = serializers.FloatField()
    globulin = serializers.FloatField()
    glucose = serializers.FloatField()
    potassium = serializers.FloatField()
    protein = serializers.FloatField()
    sodium = serializers.FloatField()


class CovidTestsSerializer(serializers.Serializer):
    sare_cov_2_igg = serializers.CharField()
    sars_cov_2_assay = serializers.CharField()
    architect_sars_cov_2_igg = serializers.CharField()
    abbott_real_time_sars_cov_2 = serializers.CharField()
    carestart_covid_19 = serializers.CharField()
    bd_veritor_sars_cov_2 = serializers.CharField()
    bio_rad_platelia_total = serializers.CharField()
    biofire_covid_19_test = serializers.CharField()
    biomerieux_argene_sars_cov_2_gene = serializers.CharField()
    biomerieux_vidas_sars_cov_2_igg = serializers.CharField()
    biomerieux_vidas_sars_cov_2_igm = serializers.CharField()
    cepheid_xpert_xpress_sars_cov_2 = serializers.CharField()
    diasorin_liaison_sars_cov_2_s1s2_igg = serializers.CharField()
    diasorin_molecular_simplexa_covid_19 = serializers.CharField()
    genmark_dx_eplex_sars_cov_2_test = serializers.CharField()
    healgen_scientific_covid_19_igg = serializers.CharField()
    healgen_scientific_covid_19_igm = serializers.CharField()
    hologic_panther_fusion_sars_cov_2 = serializers.CharField()
    luminex_aries_sars_cov_2_assay = serializers.CharField()
    luminex_nxtag_cov = serializers.CharField()
    mesa_biotech_accula_sars_cov_2 = serializers.CharField()
    quidel_lyra_sars_cov_2_assay = serializers.CharField()
    quidel_sofia_2_sars_antigen = serializers.CharField()


class LipidPanelSerializer(serializers.Serializer):
    cholesterol_total = serializers.FloatField()
    hdl_cholesterol = serializers.FloatField()
    ldl_cholesterol = serializers.FloatField()
    triglycerides = serializers.FloatField()


class UrinalysisSerializer(serializers.Serializer):
    urinalysis_bilirubin = serializers.FloatField()
    clarity = serializers.CharField()
    color = serializers.CharField()
    glucosel = serializers.CharField()  
    urine_glucose = serializers.FloatField()
    urine_hemoglobin = serializers.FloatField()
    ketones = serializers.FloatField()
    leukocytes = serializers.CharField()
    nitrite = serializers.CharField()
    ph = serializers.FloatField()
    urine_protein = serializers.FloatField()
    specific_gravity = serializers.FloatField()
    urobilinogen = serializers.FloatField()


class LabResultsSerializer(serializers.Serializer):
    collected = serializers.DateField()
    resulted = serializers.DateField()

    cbc = CBCSerializer()
    cmp = CMPSerializer()
    covid_tests = CovidTestsSerializer()
    lipid_panel = LipidPanelSerializer()
    urinalysis = UrinalysisSerializer()

    fit_ifobt = serializers.CharField()
    fit_dna = serializers.CharField()
    fobt = serializers.CharField()
    glucose_single = serializers.FloatField()
    hemoglobin_a1c = serializers.FloatField()
    microalbumin = serializers.FloatField()
    urine_hcg = serializers.CharField()
    psa = serializers.FloatField()
    inr = serializers.FloatField()
    prothrombin_time = serializers.FloatField()
    rapid_hiv = serializers.CharField()
    rapid_influenza_a = serializers.CharField()
    rapid_influenza_b = serializers.CharField()
    monospot = serializers.CharField()
    rapid_strep_a = serializers.CharField()
    induration = serializers.FloatField()
    tb = serializers.CharField()
