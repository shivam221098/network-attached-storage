import uuid
import os
from . import models
from django.conf import settings
from django.contrib.auth.models import User
from pathlib import Path


def get_uuid_as_string(uuid_obj: uuid.UUID) -> str:
    return uuid_obj.urn[9:]


def get_current_user_storage_path(username: str) -> dict:
    """
    returns current logged-in user's storage path and directory name as dictionary
    """
    current_user = User.objects.filter(username=username).first()
    if current_user:
        storage_user = models.StorageUser.objects.filter(username=current_user).first()
        if storage_user:
            dir_uuid = get_uuid_as_string(storage_user.dir_uuid)
            user_storage_path = settings.FILE_PATH_DIRECTORY / dir_uuid
            return {
                "user_storage_path": user_storage_path,
                "dir_uuid": dir_uuid
            }

    return {}


def find_valid_path(user_storage_path: Path, given_path: str, is_redirect_required=False) -> dict:
    """
    recursively finds the given path in the user storage and returns all directories and files found in the path as list
    """
    path = user_storage_path / given_path
    if os.path.exists(path):
        return {
            "files": [
                {
                    "file_path": path / blob,
                    "file_name": blob,
                    "is_dir": os.path.isdir(path / blob)
                }
                for blob in os.listdir(path)
            ],
            "redirect_path": given_path,
            "is_redirect_required": is_redirect_required
        }

    return find_valid_path(user_storage_path, "/".join(given_path.split("/")[:-1]), True)


def find_url(endpoint_path: str) -> list:
    """
    creates link to all directories
    """
    results = []
    split_path = endpoint_path.split("/")
    for idx, path in enumerate(split_path):
        results.append(
            {
                "name": path,
                "path": "/" + "/".join(split_path[:idx + 1])
            }
        )

    return results
