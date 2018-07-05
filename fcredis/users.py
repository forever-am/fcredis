import redis
from .base import RedisDB
from .tag import UserInfoEnum


class RedisUsers(RedisDB):

    def __init__(self, db, salt=None):
        super(RedisUsers, self).__init__(db)
        self.salt = salt or "3268abddc"

    @classmethod
    def from_url(cls, url, salt=None):
        cls(redis.from_url(url), salt)

    @property
    def keys(self):
        return list(filter(
            lambda k: k.startswith(self._prefix), RedisDB.keys.fget(self)
        ))

    @property
    def _prefix(self):
        return "USER:"

    def iter_active_users(self):
        for key in self.keys:
            info = self[key]
            if info.get(UserInfoEnum.ACTIVE.lower(), False):
                yield int(self._key_without_prefix(key))
