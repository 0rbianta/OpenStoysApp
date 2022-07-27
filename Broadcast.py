import datetime
from threading import Thread

from kivy.clock import Clock

import Helper


class Broadcast:
    def __init__(self, name, *callbacks):
        self.broadcast_len = len(Helper.broadcast)
        self.name = name
        self.callbacks = callbacks

        Clock.schedule_interval(self.update, 1)

    def update(self, _):
        if self.broadcast_len != len(Helper.broadcast):

            signal = Helper.broadcast[self.broadcast_len]
            if signal == f"reload_required_{self.name}":
                for callback in self.callbacks:
                    callback(datetime.datetime.today().strftime("%Y.%m.%d"))
                #    Thread(target=callback, args=(datetime.datetime.today().strftime("%Y.%m.%d"), )).start()

            self.broadcast_len = len(Helper.broadcast)
