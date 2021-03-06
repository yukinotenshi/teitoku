from threading import Thread
from teitoku.intermediate import Request, Response


class RequestDispatcher:
    instance = None

    def __init__(self):
        self.handlers = {}
        self.active_events = []
        self.default_message = None

    @classmethod
    def load(cls):
        if cls.instance is None:
            cls.instance = cls()

        return cls.instance

    def dispatch(self, request):
        handler = self.lookup_handler(request)
        if handler is None:
            return

        response = Response()
        thread = Thread(target=handler.execute, args=[request, response, ])
        thread.start()

    def lookup_handler(self, message):
        for _, h in self.handlers.items():
            if h.check_applicable(message):
                return h

    def register_handler(self, handler):
        self.handlers[handler.command] = handler
