import signal


class SignalHandler:
    @classmethod
    def register_signal(cls, signum):
        signal.signal(signum, cls.sighandler)

    @staticmethod
    def sighandler(signum, frame):
        print(f"Receive signal({signum})")
        exit(1)
