from puroboros.asm.darwin.arm64 import DarwinARM64
from puroboros.asm.register import Register


class TestDarwinARM64:
    def test_initial_output(self):
        asm = DarwinARM64()

        assert asm.output == ''

    def test_initial_registers(self):
        asm = DarwinARM64()
        registers = [reg.name for reg in asm.registers.pool]

        assert registers == ['x8', 'x9', 'x10', 'x11']

    def test_preamble(self):
        asm = DarwinARM64()
        asm.preamble()

        assert asm.output == (
            '.global _start\n'
            '.align 4\n'
            '_start:\n'
        )

    def test_postamble(self):
        asm = DarwinARM64()
        asm.postamble()

        assert asm.output == (
            'mov x0, #0\n'
            'mov x16, #1\n'
            'svc #0x80\n'
        )

    def test_load(self):
        asm = DarwinARM64()
        asm.load(5)

        assert asm.output == 'mov x8, #5\n'

    def test_add(self):
        asm = DarwinARM64()
        r1 = Register('x0', False)
        r2 = Register('x1', False)
        asm.add(r1, r2)

        assert asm.output == 'add x0, x0, x1\n'
        
    def test_sub(self):
        asm = DarwinARM64()
        r1 = Register('x0', False)
        r2 = Register('x1', False)
        asm.sub(r1, r2)

        assert asm.output == 'sub x0, x0, x1\n'

    def test_mul(self):
        asm = DarwinARM64()
        r1 = Register('x0', False)
        r2 = Register('x1', False)
        asm.mul(r1, r2)

        assert asm.output == 'mul x0, x0, x1\n'

    def test_div(self):
        asm = DarwinARM64()
        r1 = Register('x0', False)
        r2 = Register('x1', False)
        asm.div(r1, r2)

        assert asm.output == 'sdiv x0, x0, x1\n'
