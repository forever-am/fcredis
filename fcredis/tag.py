from enum import Enum, unique

try:
    from enum import auto
except ImportError:
    _number_auto = 0

    def auto():
        global _number_auto
        _number_auto += 1
        return _number_auto


class StrEnum(Enum):
    def lower(self):
        return self.name.lower()


@unique
class UserInfoEnum(StrEnum):
    KRAKEN_PUBLIC_API_KEY = auto()
    KRAKEN_PRIVATE_API_KEY = auto()
    NAME = auto()
    USER_ID = auto()
    INDEX = auto()
    EXCHANGE = auto()
    ACTIVE = auto()
    IS_KEY_ENCRYPTED = auto()

    @classmethod
    def sensitive_fields(cls):
        return {
            cls.KRAKEN_PUBLIC_API_KEY.lower(),
            cls.KRAKEN_PRIVATE_API_KEY.lower()
        }
