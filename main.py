#!/usr/bin/env python3
import argparse
import platform

from puroboros.context import Context
from puroboros.expr import Parser
from puroboros.gen import CodeGenerator
from puroboros.scan import Scanner


def compile(args):
    with open(args.file, 'rt') as infile:
        context = Context()
        context.infile = infile
        scanner = Scanner(context)
        parser = Parser(scanner)
        node, _ = parser.bin_expr()

    generator = CodeGenerator(args.system, args.arch)
    generator.generate(node)

    with open(args.output, 'wt') as outfile:
        outfile.write(generator.assembly.output)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Puroboros C compiler')
    parser.add_argument('file', type=str, help='input path')
    parser.add_argument('-o', '--output', type=str, help='output path', default='a.out')
    parser.add_argument(
        '-s',
        '--system',
        type=str,
        help='operating system name',
        default=platform.system(),
    )
    parser.add_argument(
        '-a', '--arch', type=str, help='architecture type', default=platform.machine()
    )
    args = parser.parse_args()

    compile(args)
