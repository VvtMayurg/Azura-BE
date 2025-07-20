from rest_framework import serializers

from azura_be.core.models import Specialty, ICDCode, Condition, CPTCode, HCPCSCode, RxCode, LoincCode
from azura_be.core.models import Frequency, Category, Tag, Flag


class FrequencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Frequency
        fields = ("id", "name")

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name")

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("id", "name")

class FlagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flag
        fields = ("id", "name")


class SpecialtyRelatedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialty
        fields = ("id", "name")


class SpecialtyPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialty
        fields = ("name", "description", "active", "parent", "code", "category")


class SpecialtyGetSerializer(serializers.ModelSerializer):
    parent = SpecialtyRelatedSerializer(required=False)

    class Meta:
        model = Specialty
        fields = "__all__"


class ICDCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ICDCode
        fields = ("title", "code", "icd9")

class ICDCodeGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = ICDCode
        fields = "__all__"

class ConditionRelatedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Condition
        fields = ("id", "name")

class ConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Condition
        fields = ("name", "description", "icd_codes", "ccm", "pcm", "rpm", "bhi")


class ConditionGetSerializer(serializers.ModelSerializer):
    icd_codes = ICDCodeGetSerializer(many=True, required=False)

    class Meta:
        model = Condition
        fields = "__all__"

class CPTCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CPTCode
        fields = ("title", "code", "description", "notes", "type", "category", 'section', "subsection", "clinical_descriptor_id", "version", "source", "start_date", "end_date")

class CPTCodeGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = CPTCode
        fields = "__all__"


class HCPCSCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = HCPCSCode
        fields = ("title", "code", "description", "type", "sequence_number", "record_id")

class HCPCSCodeGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = HCPCSCode
        fields = "__all__"

class RxCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RxCode
        fields = ("title", "code", "description", "ndc")

class RxCodeGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = RxCode
        fields = "__all__"

class LoincCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoincCode
        fields = ("category", "code", "description")

class LoincCodeGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoincCode
        fields = "__all__"
