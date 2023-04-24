from rest_framework import serializers

from apps.directions.models import Direction


class DirectionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Direction
        fields = ["id", "title", "number_of_stages"]
