from abc import ABC, abstractmethod


class Command(ABC):
    @abstractmethod
    def execute():
        """Generic call for command.
        """
