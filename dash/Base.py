from abc import ABCMeta, abstractmethod


class BaseBlock(metaclass=ABCMeta):
    def __init__(self, df, app=None, prefix=''):
        self.app = app
        self.prefix = prefix
        self._sample_data = df
        self._player_name = None
        self._player_df = None
        self._player_position = None

        if self.app is not None and hasattr(self, 'callbacks'):
            self.callbacks(self.app)
            print(prefix, 'init analysis')

    @abstractmethod
    def callbacks(self):
        pass

    def change_player(self, player_name):
        self._player_name = player_name
        self._player_df = self._sample_data[self._sample_data['Name'] == player_name]
        self._player_position = self._player_df['Position'].to_list()[0]
