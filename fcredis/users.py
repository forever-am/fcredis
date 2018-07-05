import json

from .base import RedisDB
from .tag import UserInfoEnum


class Users(RedisDB):
    _prefix = "USER:"

    @property
    def keys(self):
        return list(filter(
            lambda k: k.startswith(self._prefix), RedisDB.keys.fget(self)
        ))

    def add(self, user_id, info=None):
        info = info or {}
        info[UserInfoEnum.USER_ID.lower()] = user_id
        super(Users, self).add(user_id, info)

    def iter_active_users(self):
        for key in self.db.scan_iter():
            info = self[key]
            if info.get(UserInfoEnum.ACTIVE.lower(), False):
                yield int(key)
