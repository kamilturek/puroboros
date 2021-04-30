from dataclasses import dataclass
from typing import Iterable

from puroboros.exceptions import RegisterError


@dataclass
class Register:
    name: str
    free: bool = True

    def __str__(self) -> str:
        return self.name


class RegisterManager:
    def __init__(self, register_names: Iterable[str]) -> None:
        self.pool = [
            Register(name)
            for name in dict.fromkeys(register_names)
        ]

    def free(self, register: Register) -> None:
        if register.free:
            msg = f'Register {register} is already free'
            raise RegisterError(msg)
        register.free = True

    def free_all(self) -> None:
        for register in self.pool:
            register.free = True

    def allocate(self) -> Register:
        for register in self.pool:
            if register.free:
                register.free = False
                return register
        else:
            msg = 'Out of registers'
            raise RegisterError(msg)


class RegisterMeta(type):
    def __new__(cls, name, bases, attrs, **kwargs):
        new_class = super().__new__(cls, name, bases, attrs, **kwargs)
        meta = getattr(new_class, 'Meta', None)
        if hasattr(meta, 'registers'):
            new_class.registers = RegisterManager(meta.registers)
        return new_class
