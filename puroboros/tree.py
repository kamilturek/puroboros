from .defs import ASTNode, ASTNodeType


def mkastleaf(op: ASTNodeType, intvalue: int) -> ASTNode:
    return ASTNode(op=op, intvalue=intvalue)


def mkastunary(op: ASTNodeType, left: ASTNode, intvalue: int) -> ASTNode:
    return ASTNode(op=op, left=left, intvalue=intvalue)
