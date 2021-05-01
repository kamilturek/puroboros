from unittest.mock import Mock, call, patch

import pytest

from puroboros.defs import ASTNode
from puroboros.exceptions import CodeGenerationError
from puroboros.gen import CodeGenerator


@patch.object(CodeGenerator, '_get_assembly')
class TestGenerator:
    def test_get_generator_called(self, m_get_assembly):
        gen = CodeGenerator()

        assert m_get_assembly.call_count == 1

    @patch.object(CodeGenerator, '_generate_ast')
    def test_generate(self, m_generate_ast, m_get_assembly):
        gen = CodeGenerator()
        gen.generate(Mock())

        assert gen.assembly.preamble.call_count == 1
        assert gen.assembly.postamble.call_count == 1
        assert gen._generate_ast.call_count == 1

    @pytest.mark.parametrize('node_type,method_name', [
        (ASTNode.Type.A_ADD, 'add'),
        (ASTNode.Type.A_SUBTRACT, 'sub'),
        (ASTNode.Type.A_MULTIPLY, 'mul'),
        (ASTNode.Type.A_DIVIDE, 'div'),
    ])
    def test_generate_ast(self, m_get_assembly, node_type, method_name):
        node = ASTNode(
            op=node_type,
            left=ASTNode(
                op=ASTNode.Type.A_INTLIT,
                intvalue=1,
            ),
            right=ASTNode(
                op=ASTNode.Type.A_INTLIT,
                intvalue=2,
            ),
        )
        gen = CodeGenerator()
        gen.generate(node)

        assert getattr(gen.assembly, method_name).call_count == 1
        gen.assembly.load.assert_has_calls([
            call(1), call(2),
        ])

    def test_generate_ast_unknown_operator(self, m_get_assembly):
        node = Mock(op='mock', left=None, right=None)
        gen = CodeGenerator()
        with pytest.raises(CodeGenerationError) as e:
            gen.generate(node)

        assert str(e.value) == 'Unknown AST operator mock'
