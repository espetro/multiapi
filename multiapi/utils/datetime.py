from datetime import datetime


def query_format(value: datetime) -> str:
    return value.strftime("%Y-%m-%d")
