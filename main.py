#!/usr/bin/env python3
import sys

from puroboros.context import Context
from puroboros.expr import Parser
from puroboros.gen import CodeGenerator
from puroboros.scan import Scanner


if __name__ == '__main__':
    with open(sys.argv[1], 'rt') as fi:
        context = Context()
        context.infile = fi
        scanner = Scanner(context)
        parser = Parser(scanner)

        node, _ = parser.bin_expr()

    generator = CodeGenerator('darwin', 'arm64')
    generator.generate(node)
    print(generator.assembly.outstream.getvalue())
