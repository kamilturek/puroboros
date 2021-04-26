from abc import ABC, abstractmethod

from puroboros.asm.register import Register


class AssemblyGenerator(ABC):
    @abstractmethod
    def load(self) -> Register:
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
