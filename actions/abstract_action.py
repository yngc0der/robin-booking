from abc import ABC, abstractmethod
from actions import Config

class AbstractAction(ABC):
    def __init__(self, config: Config) -> None:
        super().__init__()
        self._config = config

    @abstractmethod
    def exec(self) -> None:
        pass
