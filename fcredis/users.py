import hashlib
import logging
import rncryptor
from .base import RedisDB
from .tag import UserInfoEnum


def _sensitive_fields(info):
    return UserInfoEnum.sensitive_fields().intersection(info.keys())


class Cryptor(object):
    def __init__(self, salt):
        self.salt = salt
        if self.salt:
            self.salt = hashlib.sha256(str.encode(self.salt)).hexdigest()
            logging.info("salt is set.")
        else:
            logging.info("No salt provided. It won't be possible to "
                         "decrypt sensitive fields.")
        self.cryptor = rncryptor.RNCryptor()

    def __bool__(self):
        return self.salt is not None

    def encrypt(self, value):
        bytes_value = self.cryptor.encrypt(value, self.salt)
        return bytes_value.hex()

    def decrypt(self, value):
        bytes_value = bytes.fromhex(value)
        return self.cryptor.decrypt(bytes_value, self.salt)


class RedisUsers(RedisDB):

    def __init__(self, db, salt=None):
        super(RedisUsers, self).__init__(db)
        self.cryptor = Cryptor(salt)

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
        if sensitive_fields and self.cryptor:
            result = {k: self.cryptor.encrypt(info[k])
                      for k in sensitive_fields}
            result[UserInfoEnum.IS_KEY_ENCRYPTED.lower()] = True
            info.update(result)
        super(RedisUsers, self).add(key, info)

    def __getitem__(self, key):
        info = super(RedisUsers, self).__getitem__(key)
        if not info or not self.cryptor:
            return info
        sensitive_fields = _sensitive_fields(info)
        if sensitive_fields and info[UserInfoEnum.IS_KEY_ENCRYPTED.lower()]:
            result = {k: self.cryptor.decrypt(info[k])
                      for k in sensitive_fields}
            result[UserInfoEnum.IS_KEY_ENCRYPTED.lower()] = False
            info.update(result)
        return info

    def iter_active_users(self):
        for key in self.keys:
            info = super(RedisUsers, self).__getitem__(key)
            if info.get(UserInfoEnum.ACTIVE.lower(), False):
                yield int(self._key_without_prefix(key))
