from fcredis import tag


def test_user_info_enum():
    assert tag.UserInfoEnum.API_KEY.name == "API_KEY"
    assert tag.UserInfoEnum.API_KEY.lower() == "api_key"