from puroboros.defs import ASTNode
from puroboros.codegen.darwin.arm64 import DarwinARM64CodeGenerator
from puroboros.exceptions import CodeGenerationError


class Generator:
    def __init__(self) -> None:
        # use some factory here to get proper generator
        self.generator = DarwinARM64CodeGenerator()

    def generate(self, node: ASTNode) -> None:
        self.generator.preamble()
        self._generate_ast(node)
        self.generator.postamble()

    def _generate_ast(self, node: ASTNode) -> None:
        if node.left:
            left_reg = self._generate_ast(node.left)
        if node.right:
            right_reg = self._generate_ast(node.right)

        match node.op:
            case ASTNode.Type.A_ADD:
                return self.generator.add(left_reg, right_reg)
            case ASTNode.Type.A_SUBTRACT:
                return self.generator.sub(left_reg, right_reg)
            case ASTNode.Type.A_MULTIPLY:
                return self.generator.mul(left_reg, right_reg)
            case ASTNode.Type.A_DIVIDE:
                return self.generator.div(left_reg, right_reg)
            case ASTNode.Type.A_INTLIT:
                return self.generator.load(node.intvalue)
            case _:
                msg = f'Unknown AST operator {node.op}'
                raise CodeGenerationError(msg)
            