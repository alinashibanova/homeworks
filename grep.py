import argparse

import re

import sys

flag = 0


def checkContexts(line, i, params, buff, befcontextsize, aftcontextsize):
    global flag
    prev=0
    if params.count:
        output(str(i + 1))
    else:
        if params.context:
            count = befcontextsize
            if len(buff) < befcontextsize:
                count = len(buff)
            for c in buff:
                if params.line_number:
                    output("{}-{}".format(str(i + 1 - count), c))
                else:
                    output(c)
                if count > 0:
                    count = count - 1
            if params.line_number and line not in buff:
                output("{}:{}".format(str(i + 1), line))
                # usedWords.append(line)
            else:
                if line not in buff:
                    output(line)
            flag = befcontextsize
            del buff[:]
        else:
            if params.before_context:
                count = befcontextsize
                if len(buff)<befcontextsize:
                    count=len(buff)
                for c in buff:
                    if params.line_number:
                        output("{}-{}".format(str(i - count + 1), c))
                    else:
                        output(c)
                    if count > 0:
                        count = count - 1
                if params.line_number and line not in buff:
                    output("{}:{}".format(str(i + 1), line))
                    prev=1
                else:
                    if line not in buff:
                        output(line)
                        prev = 1
                del buff[:]
            if params.after_context:
                del buff[:]
                if params.line_number  and prev==0:
                    output("{}:{}".format(str(i + 1), line))
                else:
                    if line not in buff  and prev==0:
                        output(line)
                flag = aftcontextsize
            if params.after_context == params.before_context == params.context == 0:
                if params.line_number:
                    output("{}:{}".format(str(i + 1), line))
                else:
                    output(line)


def output(line):
    print(line)


def grep(lines, params):
    global flag
    flag = 0
    buff = []
    befcontextsize = 0
    aftcontextsize = 0
    if params.context:
        befcontextsize = params.context
    if params.before_context:
        befcontextsize = params.before_context
    if params.after_context:
        aftcontextsize = params.after_context
    i = 0
    for line in lines:
        line = line.rstrip()
        a = params.pattern
        if "*" in str(params.pattern):
            a = a.replace("*", '\\w*')
        if "?" in str(params.pattern):
            a = a.replace("?", '\\w')
        if params.ignore_case:
            a = "(?i)" + a
        if params.invert:
            result = re.findall(a, line)
            if len(result) == 0:
                checkContexts(line, i, params, buff, befcontextsize, aftcontextsize)
            if len(result) != 0:
                flagCheck(params, line, i, buff, befcontextsize)
        else:
            result = re.findall(a, line)
            if len(result) != 0:
                checkContexts(line, i, params, buff, befcontextsize, aftcontextsize)
                if len(buff) == befcontextsize and len(buff)>0:
                    del buff[0]
            if len(result) == 0:
                flagCheck(params, line, i, buff, befcontextsize)

        i = i + 1


def flagCheck(params, line, i, buff,befcontextsize):
    global flag
    if flag > 0:
        if params.line_number:
            output("{}-".format(str(i + 1)) + line)
        else:
            output(line)
    if befcontextsize > 0 and flag == 0:
        if len(buff) == befcontextsize:
            del buff[0]
        if len(buff) < befcontextsize:
            buff.append(line)
    if flag > 0:
        flag = flag - 1


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