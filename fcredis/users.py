from .base import RedisDB
from .tag import UserInfoEnum


class RedisUsers(RedisDB):

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
