from abc import ABC, abstractmethod

from puroboros.asm.register import Register


class AssemblyGenerator(ABC):
    @property
    @abstractmethod
    def output(self) -> str:
        pass

    @abstractmethod
    def load(self, value: int) -> Register:
        pass

    @abstractmethod
    def add(self, r1: Register, r2: Register) -> Register:
        pass

    @abstractmethod
    def sub(self, r1: Register, r2: Register) -> Register:
        pass

    @abstractmethod
    def mul(self, r1: Register, r2: Register) -> Register:
        pass

    @abstractmethod
    def div(self, r1: Register, r2: Register) -> Register:
        pass
