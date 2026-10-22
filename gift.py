from abc import ABC, abstractmethod


class Gift(ABC):
    @abstractmethod
    def open_gift(self) -> None:
        pass
