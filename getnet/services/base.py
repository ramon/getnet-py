import re

from getnet import API


class ServiceBase:
    _client: API = None
    path: str = None

    def __init__(self, client: API) -> None:
        if not self.path:
            raise NotImplementedError("The classes parameter path must be defined")

        self._client = client

    def _format_url(self, path=None, **kwargs) -> str:
        data = {}

        path = self.path + path if path is not None else self.path

        matchs = re.search(r"{(\w+)}", path)
        if matchs:
            data = {}.fromkeys(list(matchs.groups()), "")

        data.update(**kwargs)

        return path.format(**data).rstrip("/")

    def get(self, *args, **kwargs):
        return self._client.get(*args, **kwargs)

    def post(self, *args, **kwargs):
        return self._client.post(*args, **kwargs)

    def delete(self, *args, **kwargs):
        return self._client.delete(*args, **kwargs)
