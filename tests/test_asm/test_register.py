from attr import has
import pytest

from puroboros.asm.register import Register, RegisterManager, RegisterMeta
from puroboros.exceptions import RegisterError


class TestRegister:
    def test_str(self):
        register = Register('x0')

        assert str(register) == 'x0'

    def test_free_by_default(self):
        register = Register('x0')

        assert register.free is True
 

class TestRegisterManager:
    def test_init(self):
        manager = RegisterManager(['x0', 'x1'])

        assert manager.registers == [
            Register('x0'),
            Register('x1'),
        ]

    def test_init_blank(self):
        manager = RegisterManager([])

        assert manager.registers == []

    def test_init_duplicated_register(self):
        manager = RegisterManager(['x0', 'x0'])

        assert manager.registers == [Register('x0')]

    def test_init_registesr_order(self):
        manager = RegisterManager(['x3', 'x3', 'x1'])

        assert manager.registers == [
            Register('x3'),
            Register('x1'),
        ]

    def test_free_register(self):
        manager = RegisterManager(['x0'])
        register = manager.registers[0]
        register.free = False
        manager.free(register)
        
        assert register.free is True

    def test_already_free_register(self):
        manager = RegisterManager(['x0'])
        register = manager.registers[0]
        with pytest.raises(RegisterError) as e:
            manager.free(register)

        assert str(e.value) == 'Register x0 is already free'

    def test_free_all(self):
        manager = RegisterManager(['x0', 'x1'])
        for register in manager.registers:
            register.free = True
        manager.free_all()

        return all(
            register.free is True
            for register in manager.registers
        )

    def test_allocate(self):
        manager = RegisterManager(['x0'])
        register = manager.allocate()

        assert register.free is False

    def test_allocate_order(self):
        manager = RegisterManager(['x0', 'x1'])
        register_1 = manager.allocate()
        register_2 = manager.allocate()

        assert register_1.name == 'x0'
        assert register_1.free is False
        assert register_2.name == 'x1'
        assert register_2.free is False

    def test_out_of_registers(self):
        manager = RegisterManager([])
        with pytest.raises(RegisterError) as e:
            manager.allocate()

        assert str(e.value) == 'Out of registers'



class TestRegisterMeta:
    def test_no_meta(self):
        class Class(metaclass=RegisterMeta):
            pass
        
        assert hasattr(Class, 'registers') is False

    def test_blank_meta(self):
        class Class(metaclass=RegisterMeta):
            class Meta:
                pass
        
        assert hasattr(Class, 'registers') is False

    def test_meta_with_blank_registers(self):
        class Class(metaclass=RegisterMeta):
            class Meta:
                registers = []
        
        assert isinstance(Class.registers, RegisterManager)
        assert Class.registers.registers == []

    def test_meta_with_registers(self):
        class Class(metaclass=RegisterMeta):
            class Meta:
                registers = ['x0', 'x1']
        
        assert isinstance(Class.registers, RegisterManager)
        assert Class.registers.registers == [
            Register('x0'),
            Register('x1'),
        ]
