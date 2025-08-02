import dataclasses
import os

import gdown
from loguru import logger
import shutil

@dataclasses.dataclass
class Blob:
    url: str
    hash: str

    @property
    def path(self):
        return os.path.expanduser(f"~/.cache/osam/models/blobs/{self.hash}")

    @property
    def size(self):
        if os.path.exists(self.path):
            return os.stat(self.path).st_size
        else:
            return None

    @property
    def modified_at(self):
        if os.path.exists(self.path):
            return os.stat(self.path).st_mtime
        else:
            return None

    def pull(self):
        # gdown.cached_download(url=self.url, path=self.path, hash=self.hash)
        # 如果是本地檔案，就直接複製到 cache 目錄
        if self.url.startswith("file://"):
            local_path = self.url[len("file://"):]
            if os.path.exists(local_path):
                os.makedirs(os.path.dirname(self.path), exist_ok=True)
                logger.debug(f"Copying local model from {local_path} to cache {self.path}")
                shutil.copy(local_path, self.path)
                return
            else:
                logger.error(f"Local model file not found: {local_path}")
        # 否則還是走 gdown 下載／快取
        logger.debug(f"Downloading model from {self.url} to cache {self.path}")
        gdown.cached_download(url=self.url, path=self.path, hash=self.hash)

    def remove(self):
        if os.path.exists(self.path):
            logger.debug("Removing blob {path!r}", path=self.path)
            os.remove(self.path)
        else:
            logger.warning("Blob {path!r} not found", path=self.path)
