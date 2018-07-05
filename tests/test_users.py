from unittest import TestCase
from os import path
import fakeredis

from fcredis.tag import UserInfoEnum
from fcredis import users


class UsersTest(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.user_id = 590082058
        cls.info = {
            UserInfoEnum.ACTIVE.lower(): True,
            UserInfoEnum.EXCHANGE.lower(): "kraken",
            UserInfoEnum.INDEX.lower(): "CRC3",
        }
        cls.data_path = path.join(path.dirname(__file__), "data")
        cls.json_filename = path.join(cls.data_path, "db.json")

    def setUp(self):
        self.db = fakeredis.FakeStrictRedis()
        self.users = users.Users(self.db)
        self.addCleanup(self.db.flushall)

    def test_add_and_getitem(self):
        self.users.add(self.user_id, self.info)
        expected = dict(self.info)
        expected[UserInfoEnum.USER_ID.lower()] = self.user_id
        assert expected == self.users[self.user_id]
        assert expected == self.users[self.users._key(self.user_id)]

    def test_from_to_json(self):
        self.users.from_json(self.json_filename)
        result = self.users.to_dict()
        expected_keys = {'USER:590082058', 'USER:910081058'}
        assert expected_keys == result.keys()

    def test_contains(self):
        self.users.from_json(self.json_filename)
        assert self.user_id in self.users

