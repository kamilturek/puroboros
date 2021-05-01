import platform

from puroboros.asm.darwin.arm64 import DarwinARM64
from puroboros.exceptions import CodeGenerationError


class AssemblyFactory:
    @staticmethod
    def create(system=None, machine=None):
        system = system or platform.system()
        machine = machine or platform.machine()

        match [system, machine]:
            case ['Darwin', 'arm64']:
                return DarwinARM64()
            case _:
                msg = (f'Could not determine assembly engine for '
                       f'{system} {machine} platform')
                raise CodeGenerationError(msg)
