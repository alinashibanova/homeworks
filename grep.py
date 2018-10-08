import argparse

import re

import sys


def check(lines, line, i, params, tmp, tmp2, buff, contextsize, flag):
    if params.count:

        output(str(i + 1))

    else:

        if params.context:

            count = contextsize
            if ("{}-".format(str(i + 1)) + line) in tmp2:
                tmp2.remove(("{}-".format(str(i + 1)) + line))
                tmp2.append(("{}:".format(str(i + 1)) + line))
            for c in buff:

                if c not in tmp and params.line_number:
                    tmp2.append("{}-".format(str(i + 1 - count)) + c)
                    tmp.append(c)
                else:
                    if c not in tmp:
                        tmp2.append(c)
                        tmp.append(c)
                if count > 0:
                    count = count - 1
            if params.line_number and line not in tmp:
                tmp2.append("{}:".format(str(i + 1)) + line)
                tmp.append(line)
            else:
                if line not in tmp:
                    tmp2.append(line)
                    tmp.append(line)
            flag[0] = contextsize
            tmp.extend(buff)
        elif params.before_context:
            count = contextsize
            for c in buff:
                if c not in tmp and params.line_number:
                    tmp2.append("{}-".format(str(i - count)) + c)
                else:
                    if c not in tmp:
                        tmp2.append(c)
                if count > 0:
                    count = count - 1

                tmp.extend(buff)

            if params.line_number:

                tmp2.append("{}-".format(str(i)) + line)

            else:

                tmp2.append(line)

        elif params.after_context:

            if params.line_number:

                tmp2.append("{}-".format(str(i)) + line)

            else:

                tmp2.append(line)

            flag[0] = contextsize

        else:

            if params.line_number:

                tmp2.append("{}:".format(str(i + 1)) + line)

            else:

                tmp2.append(line)


def output(line):
    return line


def grep(lines, params):
    tmp = []
    flag = [0, ]
    tmp2 = []
    buff = []
    contextsize = 0
    if params.context:
        contextsize = params.context
    if params.before_context:
        contextsize = params.before_context
    if params.after_context:
        contextsize = params.after_context
    i = 0

    for line in lines:

        line = line.rstrip()
        if flag[0] > 0 and line not in tmp:
            if params.line_number:

                tmp2.append("{}-".format(str(i + 1)) + line)
                tmp.append(line)
            else:

                tmp2.append(line)
                tmp.append(line)
            if flag[0] > 0:
                flag[0] = flag[0] - 1

        a = params.pattern

        if "*" in str(params.pattern):
            a = a.replace("*", '\\w*')

        if "?" in str(params.pattern):
            a = a.replace("?", '\\w')

        if params.ignore_case:

            b = line.lower()

            a = a.lower()

            result = re.findall(a, b)

            if result:
                output(lines[i])

            i = i + 1

            continue

        if params.invert:

            result = re.findall(a, line)

            if len(result) == 0:
                check(lines, line, i, params, tmp, tmp2, buff, contextsize, flag)




        else:

            result = re.findall(a, line)

            if len(result) != 0:
                check(lines, line, i, params, tmp, tmp2, buff, contextsize, flag)

        i = i + 1

        if contextsize > 0:
            if len(buff) == contextsize:
                buff = []
            if len(buff) < contextsize:
                buff.append(line)

    for f in tmp2:
        output(f)


def parse_args(args):
    parser = argparse.ArgumentParser(description='This is a simple grep on python')

    parser.add_argument(

        '-v', action="store_true", dest="invert", default=False, help='Selected lines are those not matching pattern.')

    parser.add_argument(

        '-i', action="store_true", dest="ignore_case", default=False, help='Perform case insensitive matching.')

    parser.add_argument(

        '-c',

        action="store_true",

        dest="count",

        default=False,

        help='Only a count of selected lines is written to standard output.')

    parser.add_argument(

        '-n',

        action="store_true",

        dest="line_number",

        default=False,

        help='Each output line is preceded by its relative line number in the file, starting at line 1.')

    parser.add_argument(

        '-C',

        action="store",

        dest="context",

        type=int,

        default=0,

        help='Print num lines of leading and trailing context surrounding each match.')

    parser.add_argument(

        '-B',

        action="store",

        dest="before_context",

        type=int,

        default=0,

        help='Print num lines of trailing context after each match')

    parser.add_argument(

        '-A',

        action="store",

        dest="after_context",

        type=int,

        default=0,

        help='Print num lines of leading context before each match.')

    parser.add_argument('pattern', action="store", help='Search pattern. Can contain magic symbols: ?*')

    return parser.parse_args(args)


def main():
    params = parse_args(sys.argv[1:])

    grep(sys.stdin.readlines(), params)


if __name__ == '__main__':
    main()
