from rest_framework import serializers
from product.models import Stone


class StoneSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    def get_image(self, obj):
        if obj.image:
            return obj.image
        return None

    class Meta:
        model = Stone
        fields = '__all__'
