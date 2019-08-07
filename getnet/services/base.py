class ServiceBase:
    _api = None
    path: str = None

    def __init__(self, client) -> None:
        if not self.path:
            raise NotImplementedError('The classes parameter path must be defined')

        self._api = client

    def call(self, *args, **kwargs):
        raise NotImplementedError('This method must be implemented.')

    def _format_url(self, **kwargs) -> str:
        return self.path.format(**kwargs)

    def _get(self, *args, **kwargs):
        return self._api.get(*args, **kwargs)

    def _post(self, *args, **kwargs):
        return self._api.post(*args, **kwargs)

    def _put(self, *args, **kwargs):
        return self._api.put(*args, **kwargs)
