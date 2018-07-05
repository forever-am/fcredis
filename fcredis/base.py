import json
import redis


class RedisDB(object):

    def __init__(self, db):
        self.db = db

    @classmethod
    def from_url(cls, url):
        return cls(redis.from_url(url))

    @property
    def keys(self):
        return [k.decode() for k in self.db.keys()]

    @property
    def _prefix(self):
        return ""

    def _key(self, user_id):
        key = str(user_id)
        if not key.startswith(self._prefix):
            key = self._prefix + key
        return key

    def __contains__(self, user_id):
        return self.db.exists(self._key(user_id))

    def __getitem__(self, user_id):
        result = self.db.get(self._key(user_id))
        if result:
            return json.loads(result)

    def add(self, key, info=None):
        user_info = self[key] or {}
        user_info.update(info or {})
        self.db.set(self._key(key), json.dumps(user_info))

    def to_dict(self):
        return {key: self[key] for key in self.keys}

    def to_json(self, filename=None):
        result = self.to_dict()
        kwargs = dict(sort_keys=True, indent=2)
        if filename:
            json.dump(result, open(filename, "w"), **kwargs)
        else:
            json.dumps(result, **kwargs)

    def from_json(self, filename):
        result = json.load(open(filename, "r"))
        for key, info in result.items():
            if key.startswith(self._prefix):
                self.add(key, info)
