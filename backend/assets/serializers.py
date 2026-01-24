from rest_framework import serializers
from .models import Asset, AssetVersion

class AssetVersionSerializer(serializers.ModelSerializer):
    created_by_name = serializers.ReadOnlyField(source='created_by.username')

    class Meta:
        model = AssetVersion
        fields = ['id', 'version_number', 'file', 'file_path', 'file_size', 'file_type', 'thumbnail', 'note', 'created_at', 'created_by', 'created_by_name']
        read_only_fields = ['created_by', 'created_at']

class AssetSerializer(serializers.ModelSerializer):
    versions = AssetVersionSerializer(many=True, read_only=True)
    latest_version = serializers.SerializerMethodField()
    owner_name = serializers.ReadOnlyField(source='owner.username')
    project_name = serializers.ReadOnlyField(source='project.name')

    class Meta:
        model = Asset
        fields = [
            'id', 'name', 'description', 'asset_type', 'project', 'project_name',
            'owner', 'owner_name', 'tags', 'created_at', 'updated_at',
            'versions', 'latest_version'
        ]
        read_only_fields = ['owner', 'created_at', 'updated_at']

    def get_latest_version(self, obj):
        latest = obj.get_latest_version()
        if latest:
            return AssetVersionSerializer(latest).data
        return None
