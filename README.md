# fcredis
[![Build Status](https://travis-ci.com/forever-am/fcredis.svg?branch=master)](https://travis-ci.com/forever-am/fcredis)
[![codecov](https://codecov.io/gh/forever-am/fcredis/branch/master/graph/badge.svg)](https://codecov.io/gh/forever-am/fcredis)
[![Maintainability](https://api.codeclimate.com/v1/badges/223b776a230b67ed426c/maintainability)](https://codeclimate.com/github/forever-am/fcredis/maintainability)

Redis API for user and allocation management

## RedisUsers

An object of `RedisUsers` can be created with an redis `url` and a `salt`, the latter is a password that helps 
to encrypt sensitive fields in the user data in storage and decrypt the sensitive data when reading.

When `salt` is not given, you will store the sensitive data directly into the database. And when you get the data,
you will still have the sensitive fields encrypted. An example of this is as following

```python
import os
import fcredis

users = fcredis.RedisUsers.from_url(os.environ["REDIS_URL"], os.environ.get("REDIS_USERS_SALT"))
users.add(5236871, {"name": "Wang", "kraken_public_api_key": "daeaereq12"})
print(users[5236871])
# {'name': 'Wang', 'kraken_public_api_key': 'daeaereq12'}

users_without_salt = users.RedisUsers.from_url(os.environ["REDIS_URL"])
print(users_without_salt[5236871])
# {'name': 'Wang', 'kraken_public_api_key': '0301688cd6efd8a3084352865ffade534ba3e20c9e3a527b5eb1b57e80c6f802782966ff897ecfe4843b4817d2286a05b570b852ab51d6bde1b4bcd652c6a3d7e9ed8fb54db4ac89597b6df07153001a60f3', 'is_key_encrypted': True}

```
