import abc
from typing import Dict


class Model(abc.ABC):

    @abc.abstractmethod
    def predict(self, text: str) -> Dict:
        """
        Start processing messages with given strategy, e.g. push, pull etc.
        :param text: Text to predict.
        :param callback: process all messages with this callback
        """
        pass
