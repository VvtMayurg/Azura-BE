from rest_framework import serializers

from azura_be.notes.models import Note
from azura_be.notes.models import VisitNote
from azura_be.users.apis.serializers import UserRelatedSerializer


class VisitNoteCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = VisitNote
        fields = ("patient", "user", "visit_start_at", "visit_end_at", "note", "note_type")


class VisitNoteSerializer(serializers.ModelSerializer):
    user = UserRelatedSerializer()

    class Meta:
        model = VisitNote
        fields = "__all__"


class NoteCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ("patient", "user", "note", "note_type")


class NoteSerializer(serializers.ModelSerializer):
    user = UserRelatedSerializer()

    class Meta:
        model = Note
        fields = "__all__"
