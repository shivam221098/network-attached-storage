import uuid
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


class StorageUser(models.Model):
    storage_user_id = models.AutoField(primary_key=True)
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    dir_uuid = models.UUIDField(unique=True,
                                default=uuid.uuid4,
                                editable=False)


class Directory(models.Model):
    file_id = models.AutoField(primary_key=True)
    dir_uuid = models.ForeignKey(StorageUser, on_delete=models.CASCADE)
    file_path = models.FilePathField(path=settings.FILE_PATH_DIRECTORY)
