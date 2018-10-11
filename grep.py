import argparse

import re

import sys

flag=0

def addtoprint(usedWords, line):
    output(line)
    usedWords.append(line)


def check(lines, line, i, params, usedWords, printWords, buff, contextsize):
    global flag
    if params.count:

        output(str(i + 1))

    else:

        if params.context:

            count = contextsize

            for c in buff:

                if c not in usedWords and params.line_number:
                    output("{}-{}".format(str(i + 1 - count), c))
                    usedWords.append(c)
                else:
                    if c not in usedWords:
                        addtoprint(usedWords,c)
                if count > 0:
                    count = count - 1
            if params.line_number and line not in usedWords:
                output("{}:{}".format(str(i + 1), line))
                usedWords.append(line)
            else:
                if line not in usedWords:
                    addtoprint( usedWords,line)
            flag = contextsize
            usedWords.extend(buff)

        elif params.before_context:
            count = contextsize
            for c in buff:
                if c not in usedWords and params.line_number:
                    output("{}-{}".format(str(i - count+1), c))
                else:
                    if c not in usedWords:
                        output(c)
                if count > 0:
                    count = count - 1

                    usedWords.extend(buff)

            if params.line_number and line not in usedWords:

                output("{}:{}".format(str(i+1), line))

            else:
                if line not in usedWords:
                    addtoprint( usedWords,line)

        elif params.after_context:

            if params.line_number and line not in usedWords:

                output("{}-{}".format(str(i+1), line))
                usedWords.append(line)

            else:
                if line not in usedWords:
                    addtoprint( usedWords,line)

            flag = contextsize

        else:

            if params.line_number:

                output("{}:{}".format(str(i + 1), line))

            else:

                output(line)


def output(line):
    print(line)


def grep(lines, params):
    usedWords = []
    global flag
    flag=0
    printWords = []
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
                check(lines, line, i, params, usedWords, printWords, buff, contextsize)




        else:

            result = re.findall(a, line)

            if len(result) != 0:
                check(lines, line, i, params, usedWords, printWords, buff, contextsize)
            if len(result)==0:
                if flag > 0 and line not in usedWords:
                    if params.line_number:

                        output("{}-".format(str(i + 1)) + line)
                        usedWords.append(line)
                    else:

                        addtoprint( usedWords, line)
                    if flag > 0:
                        flag = flag - 1

        i = i + 1

        if contextsize > 0:
            if len(buff) == contextsize:
                buff = []
            if len(buff) < contextsize:
                buff.append(line)

    # for f in printWords:
    #     output(f)


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
