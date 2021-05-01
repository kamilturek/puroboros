from abc import ABCMeta, abstractmethod
from io import StringIO

from puroboros.asm.register import Register, RegisterManager, RegisterMeta


AssemblyMeta = type('AssemblyMeta', (ABCMeta, RegisterMeta), {})


class AssemblyBase(metaclass=AssemblyMeta):
    def __init__(self) -> None:
        self.registers = RegisterManager(self._meta['registers'])
        self.outstream = StringIO()

    @property
    def output(self) -> str:
        return self.outstream.getvalue()


class Assembly(AssemblyBase):
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
