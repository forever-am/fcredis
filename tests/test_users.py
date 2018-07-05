from unittest import TestCase, mock
import json
from os import path, remove
import fakeredis

from fcredis.tag import UserInfoEnum
from fcredis.base import RedisDB
from fcredis import users


class RedisUsersTest(TestCase):
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
        self.users = users.RedisUsers(self.db)
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
        assert expected_keys == result.keys() == set(self.users.keys)

        filename = path.join(self.data_path, "users.json")
        self.users.to_json(filename)
        result_json = json.load(open(filename, "r"))
        assert expected_keys == result_json.keys()
        remove(filename)

        s = self.users.to_json()
        result_json_from_s = json.loads(s)
        assert expected_keys == result_json_from_s.keys()

    def test_contains(self):
        self.users.from_json(self.json_filename)
        assert self.user_id in self.users

    def test_iter_active_users(self):
        self.users.from_json(self.json_filename)
        active_users = list(self.users.iter_active_users())
        assert [590082058] == active_users

    @mock.patch("redis.from_url")
    def test_from_url(self, mock_from_url):
        url = "redis_url"
        users.RedisUsers.from_url(url)
        mock_from_url.assert_called_with(url)

    def test_redis_db_keys(self):
        redis_db = RedisDB(self.db)
        redis_db.from_json(self.json_filename)
        expected_keys = {
            'USER:590082058', 'USER:910081058', 'ALLOC:2018-06-25'
        }
        assert expected_keys == set(redis_db.keys)


