import signal


class SignalControllerMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class SignalController(metaclass=SignalControllerMeta):
    SIGTERM = signal.SIGTERM

    def __init__(self):
        self._handlers_by_signum = {}

    def add_handler(self, signum, handler):
        if self._handlers_by_signum.get(signum) is None:
            self._handlers_by_signum[signum] = [handler]
            signal.signal(
                signum,
                SignalController._reduce_handlers(self._handlers_by_signum[signum]),
            )
        else:
            self._handlers_by_signum[signum].append(handler)

    def _reduce_handlers(handlers):
        return lambda signum, frame: [handler(signum, frame) for handler in handlers]
