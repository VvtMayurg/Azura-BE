from rest_framework import serializers

from azura_be.base.constants import QuestionTypeChoices
from azura_be.core.apis.serializers import CategorySerializer
from azura_be.core.apis.serializers import ConditionRelatedSerializer
from azura_be.core.apis.serializers import FlagSerializer
from azura_be.core.apis.serializers import FrequencySerializer
from azura_be.core.apis.serializers import ICDCodeSerializer
from azura_be.core.apis.serializers import TagSerializer
from azura_be.plans.models import Form
from azura_be.plans.models import Plan


class QuestionSerializer(serializers.Serializer):
    question = serializers.CharField()
    question_type = serializers.ChoiceField(choices=QuestionTypeChoices)
    choices = serializers.ListField(child=serializers.CharField(), default=[])


class FormRelatedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Form
        fields = ("id", "title")


class FormCreateSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer()

    class Meta:
        model = Form
        fields = (
            "title",
            "tags",
            "flag",
            "frequency",
            "conditions",
            "category",
            "comment",
            "nas",
            "questions",
        )


class FormSerializer(serializers.ModelSerializer):
    conditions = ConditionRelatedSerializer(many=True, required=False)
    tags = TagSerializer(many=True, required=False)
    frequency = FrequencySerializer(required=False)
    category = CategorySerializer(required=False)
    flag = FlagSerializer(required=False)
    questions = QuestionSerializer()

    class Meta:
        model = Form
        fields = "__all__"


class PlanRelatedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = ("id", "name")


class NumberToTrackQuestionSerializer(serializers.Serializer):
    vitals = serializers.ListField(child=serializers.CharField(), default=[])
    labs = serializers.ListField(child=serializers.CharField(), default=[])


class PlanCreateSerializer(serializers.ModelSerializer):
    goals = QuestionSerializer(many=True, required=False)
    barriers = QuestionSerializer(many=True, required=False)
    symptoms = QuestionSerializer(many=True, required=False)
    interventions = QuestionSerializer(many=True, required=False)
    expected_outcomes = QuestionSerializer(many=True, required=False)
    supports = QuestionSerializer(many=True, required=False)
    allergies = QuestionSerializer(many=True, required=False)
    medications = QuestionSerializer(many=True, required=False)
    number_to_tracks = NumberToTrackQuestionSerializer(required=False)

    class Meta:
        model = Plan
        fields = (
            "programs",
            "name",
            "conditions",
            "icd_codes",
            "goals",
            "barriers",
            "symptoms",
            "interventions",
            "number_to_tracks",
            "expected_outcomes",
            "supports",
            "allergies",
            "medications",
        )


class PlanSerializer(serializers.ModelSerializer):
    conditions = ConditionRelatedSerializer(many=True, required=False)
    icd_codes = ICDCodeSerializer(many=True, required=False)
    goals = QuestionSerializer(many=True, required=False)
    barriers = QuestionSerializer(many=True, required=False)
    symptoms = QuestionSerializer(many=True, required=False)
    interventions = QuestionSerializer(many=True, required=False)
    expected_outcomes = QuestionSerializer(many=True, required=False)
    supports = QuestionSerializer(many=True, required=False)
    allergies = QuestionSerializer(many=True, required=False)
    medications = QuestionSerializer(many=True, required=False)
    number_to_tracks = NumberToTrackQuestionSerializer(required=False)

    class Meta:
        model = Plan
        fields = "__all__"
