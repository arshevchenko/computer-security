#!/usr/bin/python

import argparse
import sys

parser = argparse.ArgumentParser(description='I can hide file.')
command_parsers = parser.add_subparsers(help='Available commands', dest='command')
h = command_parsers.add_parser('hide', help='')
h.add_argument('file', type=str, help='Input file to hide')
h.add_argument('container', type=str, help='Container wherein file will be hidden')
h.add_argument('--output', type=str, help='Output filename')
r = command_parsers.add_parser('reveal', help='')
r.add_argument('input', type=str, help='Input file to reveal')
r.add_argument('--output', type=str, help='Output file')


def prepare_for_hide(lines):
    return map(lambda x: x.rstrip(), lines)


def prepare_for_reveal(lines):
    return map(lambda x: x.replace('\n', ''), lines)


def char_to_bin(c):
    bits = bin(ord(c))[2:]
    return '0' * (8 - len(bits)) + bits


def to_bits(data):
    return ''.join(map(char_to_bin, data))


def hide(bits, lines):
    return [lines[i] + (' ' if bits[i] == '1' else '') for i in range(len(bits))]


def reveal(lines):
    bits = ''.join(map(lambda x: '1' if len(x) and x[-1] == ' ' else '0', lines))
    return ''.join(map(lambda x: chr(int(x, 2)), [bits[i:i+8] for i in range(0, len(bits), 8)]))


if __name__ == "__main__":
    args = parser.parse_args(sys.argv[1:])

    try:
        if args.command == 'hide':
            with open(args.container, "r") as f:
                lines = prepare_for_hide(f.readlines())
            with open(args.file, "r") as f:
                bits = to_bits(f.read())

            if len(lines) < len(bits):
                print 'Container too small. It contains only %d lines, but %d needed' % (len(lines), len(bits))
                quit(1)

            hidden = hide(bits, lines)

            if args.output is None:
                for line in hidden:
                    print line
            else:
                with open(args.output, 'w') as f:
                    for line in hidden:
                        f.write(line + '\n')
        elif args.command == 'reveal':
            with open(args.input, 'r') as f:
                lines = prepare_for_reveal(f.readlines())
            revealed = reveal(lines)

            if args.output is None:
                print revealed
            else:
                with open(args.output, 'w') as f:
                    f.write(revealed)
    except Exception as e:
        print e.message, e.args
