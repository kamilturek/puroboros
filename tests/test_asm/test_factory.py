import pytest

from puroboros.asm.darwin.arm64 import DarwinARM64
from puroboros.asm.factory import AssemblyFactory
from puroboros.exceptions import CodeGenerationError


class TestAssemblyFactory:
    def test_create_darwin_arm64(self):
        asm = AssemblyFactory.create('Darwin', 'arm64')

        assert isinstance(asm, DarwinARM64)

    def test_create_unknown(self):
        with pytest.raises(CodeGenerationError) as e:
            AssemblyFactory.create('X', 'Y')
        
        assert str(e.value) == ('Could not determine assembly '
                                'engine for X Y platform')
