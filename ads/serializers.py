from rest_framework import serializers

from ads.models import Ad
from user.models import Location, User


class AdListSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(read_only=True, slug_field='name')

    class Meta:
        model = Ad
        fields = '__all__'
