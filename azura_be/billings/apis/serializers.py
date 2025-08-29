from rest_framework import serializers


class ApiRateLimitInfoSerializer(serializers.Serializer):
    current_call_count = serializers.IntegerField()
    call_limit = serializers.IntegerField()
    reset_interval = serializers.IntegerField()
    interval_expire_seconds = serializers.IntegerField()


class MetaInfoSerializer(serializers.Serializer):
    api_version = serializers.CharField()
    api_rate_limit_info = ApiRateLimitInfoSerializer()


class ServiceCodeDataSerializer(serializers.Serializer):
    code = serializers.CharField()
    amount = serializers.FloatField()
    description = serializers.CharField()
    start_date = serializers.DateField()
    end_date = serializers.DateField()


class ServiceCodeResponseSerializer(serializers.Serializer):
    result = serializers.CharField()
    data = ServiceCodeDataSerializer(many=True)
    meta_info = MetaInfoSerializer()


class DiagnosticCodeDataSerializer(serializers.Serializer):
    code = serializers.CharField()
    description = serializers.CharField()


class DiagnosticCodeResponseSerializer(serializers.Serializer):
    result = serializers.CharField()
    data = DiagnosticCodeDataSerializer(many=True)
    meta_info = MetaInfoSerializer()


class MasterNumberDataSerializer(serializers.Serializer):
    master_number = serializers.CharField()
    location = serializers.CharField()
    name = serializers.CharField()
    master_number_type = serializers.CharField()
    facility_number = serializers.CharField()


class MasterNumberResponseSerializer(serializers.Serializer):
    result = serializers.CharField()
    data = MasterNumberDataSerializer(many=True)
    meta_info = MetaInfoSerializer()


class EligibilityCheckDataSerializer(serializers.Serializer):
    service_code = serializers.CharField()
    fee_service_code = serializers.CharField()
    fee_service_date = serializers.DateField()
    fee_service_response_code = serializers.CharField()
    fee_service_response_description = serializers.CharField()
    eligibility_queued_at = serializers.DateTimeField()
    eligibility_checked_at = serializers.DateField()
    check_status = serializers.CharField()


class EligibilityCheckResponseSerializer(serializers.Serializer):
    result = serializers.CharField()
    data = EligibilityCheckDataSerializer(many=True)
    meta_info = MetaInfoSerializer()


class CalculateValueSerializer(serializers.Serializer):
    service_code = serializers.CharField()
    fee_override = serializers.CharField(allow_blank=True)
    number_of_services_override = serializers.CharField(allow_blank=True)
    percent_increase = serializers.CharField(allow_blank=True)
    service_date = serializers.DateField()
    diagnostic_code = serializers.CharField()

    def validate(self, attrs):
        attrs = super().validate(attrs)
        attrs.update({"service_date": attrs.get("service_date").strftime("%Y-%m-%d")})
        return attrs


class CalculateValueDataSerializer(serializers.Serializer):
    service_code = serializers.CharField()
    fee_override = serializers.CharField()
    fee_calculated = serializers.DecimalField(max_digits=10, decimal_places=3)
    number_of_services_override = serializers.CharField()
    number_of_services_calculated = serializers.IntegerField()
    percent_increase = serializers.CharField()
    service_date = serializers.DateField()
    diagnostic_code = serializers.CharField()


class CalculateValueResponseSerializer(serializers.Serializer):
    result = serializers.CharField()
    data = CalculateValueDataSerializer(many=True)
    meta_info = MetaInfoSerializer()
