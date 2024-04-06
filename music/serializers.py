from rest_framework import serializers
from .models import *
import ast



class SingerSpecificSerializer(serializers.ModelSerializer):
    class Meta:
        model = singer
        fields = ("id","name")


class PlayListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayList
        fields = "__all__"


class MusicSerializer(serializers.ModelSerializer):
    singer = SingerSpecificSerializer(many=True,source='singer_music.all')
    class Meta:
        model = Music
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['tags'] = ast.literal_eval(instance.tags)
        return representation
    

class AllMusicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Music
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['tags'] = ast.literal_eval(instance.tags)
        return representation
    

class SingerSerializer(serializers.ModelSerializer):
    music = AllMusicSerializer(many=True)
    class Meta:
        model = singer
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['social'] = ast.literal_eval(instance.social)
        if instance.tags:
            representation['tags'] = ast.literal_eval(instance.tags)
        return representation