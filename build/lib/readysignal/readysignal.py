class ReadySignal(object):
    def __init__(self, signal_id):
        self.signal_id = signal_id

    def info(self):
        return {'signal_id': self.signal_id}
