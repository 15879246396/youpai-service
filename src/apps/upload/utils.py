from django.core.cache import cache
from django.contrib.contenttypes.models import ContentType
from upload.models import FileUpload
from upload.serializers import FileUploadSerializer

def get_content_type_id(content_type_name):
    """
        将content_type 进行缓存
    :param content_type_name:
    :return:
    """
    content_type_dict = cache.get("CONTENT_TYPE_DICT", {})
    if content_type_dict.get(content_type_name):
        return content_type_dict.get(content_type_name)
    else:
        content_type = ContentType.objects.all()
        for con_type in content_type:
            content_type_dict[con_type.model] = con_type.id
        cache.set("CONTENT_TYPE_DICT", content_type_dict, 60 * 60 * 24)
        return content_type_dict.get(content_type_name)


def file_data(file_id_list):
    """
        所有的文件数据进行缓存
    :param file_id_list:
    :return:
    """
    files_map = cache.get("FILE_DATA", {})
    if files_map:
        return [files_map.get(file_id) for file_id in file_id_list]
    else:
        files = FileUpload.objects.filter(delete_status=0)
        file_data = FileUploadSerializer(files, many=True).data
        files_map = {file.get("id"): file for file in file_data}
        cache.set('FILE_DATA', files_map, 60 * 60 * 24 * 30 * 2)
        return [files_map.get(file_id) for file_id in file_id_list]


def update_file_data(data):
    files_map = cache.get("FILE_DATA", {})
    files_map[data.get("id")] = data
    cache.set('FILE_DATA', files_map, 60 * 60 * 24 * 30 * 2)