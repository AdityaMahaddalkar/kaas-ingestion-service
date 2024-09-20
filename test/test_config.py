from config import Config


def test_config_read_yaml():
    assert Config().get_config() is not None
