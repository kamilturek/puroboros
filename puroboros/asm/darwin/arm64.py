from io import StringIO

from puroboros.asm.base import Assembly
from puroboros.asm.register import Register


class DarwinARM64(Assembly):
    class Meta:
        registers = ['x8', 'x9', 'x10', 'x11']

    def preamble(self) -> None:
        self.outstream.writelines([
            '.global _start\n',
            '.align 4\n',
            '_start:\n',
        ])

    def postamble(self) -> None:
        self.outstream.writelines([
            'mov x0, #0\n',
            'mov x16, #1\n',
            'svc #0x80\n',
        ])

    def load(self, value: int) -> Register:
        r = self.registers.allocate()
        code = f'mov {r}, #{value}\n'
        self.outstream.write(code)
        return r

    def add(self, r1: Register, r2: Register) -> Register:
        code = f'add {r1}, {r1}, {r2}\n'
        self.outstream.write(code)
        self.registers.free(r2)
        return r1

    def sub(self, r1: Register, r2: Register) -> Register:
        code = f'sub {r1}, {r1}, {r2}\n'
        self.outstream.write(code)
        self.registers.free(r2)
        return r1

    def mul(self, r1: Register, r2: Register) -> Register:
        code = f'mul {r1}, {r1}, {r2}\n'
        self.outstream.write(code)
        self.registers.free(r2)
        return r1

    def div(self, r1: Register, r2: Register) -> Register:
        code = f'sdiv {r1}, {r1}, {r2}\n'
        self.outstream.writelines(code)
        self.registers.free(r2)
        return r1
