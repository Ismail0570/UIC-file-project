from rest_framework import serializers
from .models import File, Folder
from django.contrib.auth.models import User

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = '__all__'

class FolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Folder
        fields = '__all__'

class FileShareSerializer(serializers.ModelSerializer):
    shared_with = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True)

    class Meta:
        model = File
        fields = ['shared_with']

    def update(self, instance, validated_data):
        shared_with = validated_data.get('shared_with')
        for user in shared_with:
            instance.shared_with.add(user)
        instance.save()
        return instance
