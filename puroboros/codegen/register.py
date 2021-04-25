from dataclasses import dataclass

from puroboros.exceptions import RegisterError


@dataclass
class Register:
    name: str
    free: bool = True

    def __str__(self) -> str:
        return self.name


# maybe instead of having register manager, just use classmethods etc.
class RegisterManager:
    def __init__(self, register_names: list[str]) -> None:
        self.registers = [
            Register(name)
            for name in register_names
        ]

    def free(self, register: Register) -> None:
        if register.free:
            msg = f'Register {register} is already free'
            raise RegisterError(msg)
        register.free = True
    
    def free_all(self) -> None:
        for register in self.registers:
            register.free = True

    def allocate(self) -> Register:
        for register in self.registers:
            if register.free:
                register.free = False
                return register
        else:
            msg = 'Out of registers'
            raise RegisterError(msg)
