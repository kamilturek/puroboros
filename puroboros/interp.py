from .defs import ASTNode, ASTNodeType
from .exceptions import ParserError


def interpret_ast(node: ASTNode) -> int:
    if node.left:
        lval = interpret_ast(node.left)
    if node.right:
        rval = interpret_ast(node.right)

    match node.op:
        case ASTNodeType.A_ADD:
            return lval + rval
        case ASTNodeType.A_SUBTRACT:
            return lval - rval
        case ASTNodeType.A_MULTIPLY:
            return lval * rval
        case ASTNodeType.A_DIVIDE:
            return lval / rval
        case ASTNodeType.A_INTLIT:
            return node.intvalue
        case _:
            raise ParserError(f'Unknown AST operator {node.op}')
