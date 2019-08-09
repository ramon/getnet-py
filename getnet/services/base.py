import re


class ServiceBase:
    _api = None
    path: str = None

    def __init__(self, client) -> None:
        if not self.path:
            raise NotImplementedError("The classes parameter path must be defined")

        self._api = client

    def _format_url(self, **kwargs) -> str:
        keys = re.search(r"{(\w+)}", self.path).groups()
        data = {}.fromkeys(list(keys), "")
        data.update(**kwargs)

        return self.path.format(**data).rstrip("/")

    def _get(self, *args, **kwargs):
        return self._api.get(*args, **kwargs)

    def _post(self, *args, **kwargs):
        return self._api.post(*args, **kwargs)

    def _put(self, *args, **kwargs):
        return self._api.put(*args, **kwargs)

    def _delete(self, *args, **kwargs):
        return self._api.delete(*args, **kwargs)
