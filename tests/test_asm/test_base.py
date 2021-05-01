from puroboros.asm.register import Register
from puroboros.asm.base import AssemblyBase


class TestAssemblyBase:
    def test_no_registers(self):
        class ASM(AssemblyBase):
            class Meta:
                registers = []
        asm = ASM()

        assert asm.registers.pool == []

    def test_registers(self):
        class ASM(AssemblyBase):
            class Meta:
                registers = ['x0', 'x1']
        asm = ASM()

        assert asm.registers.pool == [
            Register('x0'),
            Register('x1'),
        ]
