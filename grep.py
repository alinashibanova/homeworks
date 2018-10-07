import argparse
import re
import sys


def output(line):
    return line


def grep(lines, params):
    tmp = []
    tmp2 = []
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
                if params.count:
                    output(str(i + 1))
                else:

                    if params.context:
                        a = i - params.context
                        if a < 0:
                            a = 0
                        b = i + params.context
                        if b > len(lines) - 1:
                            b = len(lines) - 1
                        while a <= b:
                            if a == i and params.line_number:
                                if ("{}-".format(str(i + 1)) + line) in tmp2:
                                    tmp2.remove(("{}-".format(str(i + 1)) + line))
                                tmp2.append("{}:".format(str(i + 1)) + line)
                                
                                tmp.append(lines[a])
                                a = a + 1
                                continue

                            if lines[a] not in tmp and params.line_number:
                                
                                tmp2.append("{}-".format(str(a + 1)) + lines[a])
                            else:
                                if lines[a] not in tmp:
                                    
                                    tmp2.append(lines[a])
                            tmp.append(lines[a])
                            a = a + 1






                    elif params.before_context:

                        a = i - params.before_context
                        if a < 0:
                            a = 0
                        b = i
                        if b > len(lines) - 1:
                            b = len(lines) - 1
                        while a <= b:
                            if a != i:
                                if lines[a] not in tmp and params.line_number:
                                    
                                    tmp2.append("{}-".format(str(a + 1)) + lines[a])
                                else:
                                    if lines[a] not in tmp:
                                        
                                        tmp2.append(lines[a])
                            tmp.append(lines[a])
                            a = a + 1

                        if params.line_number:
                            
                            tmp2.append("{}-".format(str(a + 1)) + lines[a])
                        else:
                            tmp2.append(line)
                            
                    elif params.after_context:
                        if params.line_number:
                            
                            tmp2.append("{}-".format(str(a + 1)) + lines[a])

                        else:

                            
                            tmp2.append(line)
                        a = i

                        b = i + params.after_context
                        if b > len(lines) - 1:
                            b = len(lines) - 1
                        while a <= b:
                            if a != i:
                                if lines[a] not in tmp and params.line_number:
                                    
                                    tmp2.append("{}-".format(str(a + 1)) + lines[a])
                                else:
                                    if lines[a] not in tmp:
                                        
                                        tmp2.append(lines[a])
                            tmp.append(lines[a])
                            a = a + 1


                    else:
                        if params.line_number:
                            
                            tmp2.append("{}:".format(str(i + 1)) + line)
                        else:
                            tmp2.append(line)


        else:
            result = re.findall(a, line)
            if len(result) != 0:
                if params.count:
                    output(str(i + 1))
                else:

                    if params.context:

                        a = i - params.context
                        if a < 0:
                            a = 0
                        b = i + params.context
                        if b > len(lines) - 1:
                            b = len(lines) - 1
                        while a <= b:
                            if a == i and params.line_number:
                                if ("{}-".format(str(i + 1)) + line) in tmp2:
                                    tmp2.remove(("{}-".format(str(i + 1)) + line))
                                tmp2.append("{}:".format(str(i + 1)) + line)
                                
                                tmp.append(lines[a])
                                a = a + 1
                                continue

                            if lines[a] not in tmp and params.line_number:
                                
                                tmp2.append("{}-".format(str(a + 1)) + lines[a])
                            else:
                                if lines[a] not in tmp:
                                    
                                    tmp2.append(lines[a])
                            tmp.append(lines[a])
                            a = a + 1






                    elif params.before_context:

                        a = i - params.before_context
                        if a < 0:
                            a = 0
                        b = i
                        if b > len(lines) - 1:
                            b = len(lines) - 1
                        while a <= b:
                            if a != i:
                                if lines[a] not in tmp and params.line_number:
                                    
                                    tmp2.append("{}-".format(str(a + 1)) + lines[a])
                                else:
                                    if lines[a] not in tmp:
                                        
                                        tmp2.append(lines[a])
                            tmp.append(lines[a])
                            a = a + 1

                        if params.line_number:
                            
                            tmp2.append("{}-".format(str(a + 1)) + lines[a])
                        else:
                            tmp2.append(line)
                            
                    elif params.after_context:
                        if params.line_number:
                            
                            tmp2.append("{}-".format(str(a + 1)) + lines[a])

                        else:

                            
                            tmp2.append(line)
                        a = i

                        b = i + params.after_context
                        if b > len(lines) - 1:
                            b = len(lines) - 1
                        while a <= b:
                            if a != i:
                                if lines[a] not in tmp and params.line_number:
                                    
                                    tmp2.append("{}-".format(str(a + 1)) + lines[a])
                                else:
                                    if lines[a] not in tmp:
                                        
                                        tmp2.append(lines[a])
                            tmp.append(lines[a])
                            a = a + 1


                    else:
                        if params.line_number:
                            
                            tmp2.append("{}:".format(str(i + 1)) + line)
                        else:
                            tmp2.append(line)
        i = i + 1
        
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
