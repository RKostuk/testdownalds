from rest_framework import serializers


class AggregatedDataSerializer(serializers.Serializer):
    year = serializers.SerializerMethodField()
    total_impressions = serializers.IntegerField()

    def get_year(self, obj):
        # Convert datetime.date to integer year
        return obj['year'].year if obj['year'] else None