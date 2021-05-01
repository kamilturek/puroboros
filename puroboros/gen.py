from puroboros.defs import ASTNode
from puroboros.asm.darwin.arm64 import DarwinARM64
from puroboros.exceptions import CodeGenerationError


class CodeGenerator:
    def __init__(self) -> None:
        # use some factory here to get proper generator
        self.assembly = self._get_assembly()

    def generate(self, node: ASTNode) -> None:
        self.assembly.preamble()
        self._generate_ast(node)
        self.assembly.postamble()

    def _get_assembly(self):
        return DarwinARM64()

    def _generate_ast(self, node: ASTNode) -> None:
        if node.left:
            left_reg = self._generate_ast(node.left)
        if node.right:
            right_reg = self._generate_ast(node.right)

        match node.op:
            case ASTNode.Type.A_ADD:
                return self.assembly.add(left_reg, right_reg)
            case ASTNode.Type.A_SUBTRACT:
                return self.assembly.sub(left_reg, right_reg)
            case ASTNode.Type.A_MULTIPLY:
                return self.assembly.mul(left_reg, right_reg)
            case ASTNode.Type.A_DIVIDE:
                return self.assembly.div(left_reg, right_reg)
            case ASTNode.Type.A_INTLIT:
                return self.assembly.load(node.intvalue)
            case _:
                msg = f'Unknown AST operator {node.op}'
                raise CodeGenerationError(msg)
