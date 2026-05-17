from typing import NamedTuple


class RefreshResult(NamedTuple):
    access_token: str
    refresh_token: str
