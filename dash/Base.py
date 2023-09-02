from abc import ABCMeta, abstractmethod


class BaseBlock(metaclass=ABCMeta):
    def __init__(self, app=None, prefix=''):
        self.app = app
        self.prefix = prefix

        if self.app is not None and hasattr(self, 'callbacks'):
            self.callbacks(self.app)
            print(prefix, 'init analysis')

    @abstractmethod
    def callbacks(self):
        pass
