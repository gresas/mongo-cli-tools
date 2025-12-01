from unittest.mock import MagicMock, patch
from tools._helpers import (
    is_instance_list,
    is_instance_dict,
    is_instance_datetime
)


def test_is_list_instance():
  mock_list = list()
  assert is_instance_list(mock_list)


def test_is_not_list_instance():
  mock_list = MagicMock()
  assert not is_instance_list(mock_list)


def test_is_dict_instance():
  mock_dict = dict()
  assert is_instance_list(mock_dict)


def test_is_not_dict_instance():
  mock_dict = MagicMock()
  assert not is_instance_list(mock_dict)


@patch('tools._helpers.datetime')
def test_is_datetime_instance(datetime):
  mock_datetime = datetime()
  assert is_instance_list(mock_datetime)


def test_is_not_datetime_instance(datetime):
  mock_datetime = datetime()
  assert not is_instance_list(mock_datetime)
