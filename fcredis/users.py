import hashlib
import logging
import rncryptor
from .base import RedisDB
from .tag import UserInfoEnum

log = logging.getLogger(__name__)


def _sensitive_fields(info):
    return UserInfoEnum.sensitive_fields().intersection(info.keys())


class RedisUsers(RedisDB):

    def __init__(self, db, salt=None):
        super(RedisUsers, self).__init__(db)
        self.salt = salt
        if self.salt:
            self.salt = hashlib.sha256(str.encode(self.salt)).hexdigest()
        else:
            log.info("No salt provided. It won't be possible to decrypt "
                     "sensitive fields.")
        self.cryptor = rncryptor.RNCryptor()

    @property
    def keys(self):
        return list(filter(
            lambda k: k.startswith(self._prefix), RedisDB.keys.fget(self)
        ))

    @property
    def _prefix(self):
        return "USER:"

    def add(self, key, info=None):
        info = dict(info or {})
        sensitive_fields = _sensitive_fields(info)
        if sensitive_fields:
            for field in sensitive_fields:
                bytes_value = self.cryptor.encrypt(info[field], self.salt)
                info[field] = bytes_value.hex()
            info[UserInfoEnum.IS_KEY_ENCRYPTED.lower()] = True
        super(RedisUsers, self).add(key, info)

    def __getitem__(self, key):
        info = super(RedisUsers, self).__getitem__(key)
        if not info or not self.salt:
            return info
        sensitive_fields = _sensitive_fields(info)
        if sensitive_fields:
            for field in sensitive_fields:
                bytes_value = bytes.fromhex(info[field])
                info[field] = self.cryptor.decrypt(bytes_value, self.salt)
            info[UserInfoEnum.IS_KEY_ENCRYPTED.lower()] = False
        return info

    def iter_active_users(self):
        for key in self.keys:
            info = self[key]
            if info.get(UserInfoEnum.ACTIVE.lower(), False):
                yield int(self._key_without_prefix(key))
