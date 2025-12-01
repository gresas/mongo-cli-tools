from datetime import datetime


def is_instance_list(blob):
  return isinstance(blob, list)


def is_instance_dict(blob):
  return isinstance(blob, dict)


def is_instance_datetime(blob):
  return isinstance(blob, datetime)
