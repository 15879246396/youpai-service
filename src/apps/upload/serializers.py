from rest_framework import serializers
from upload.models import FileSet, FileUpload


class FileUploadSerializer(serializers.ModelSerializer):
    file = serializers.FileField(max_length=128, allow_empty_file=True, use_url=True, allow_null=True)

    def validate(self, attrs):
        if not attrs.get('file_url') and not attrs.get('file'):
            raise serializers.ValidationError({'error:url and file null': 'url and path null'})
        else:
            return attrs

    class Meta:
        model = FileUpload
        fields = ('id', 'file', 'uploader', 'file_url', 'file_name', 'gmt_create')

#
# class FileSetSerializer(serializers.ModelSerializer):
#     file = FileUploadSerializer(read_only=True)
#     # gmt_create = serializers.DateTimeField(read_only=True, format="%Y-%m-%d %H:%M:%S")
#
#     class Meta:
#         model = FileSet
#         fields = ("file", )


