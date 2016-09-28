import sys
import argparse
import codetester

parser = argparse.ArgumentParser(
    description='Code tester for Codeforces training')

parser.add_argument('-c',
                    '--clear',
                    help='Remove all stored inputs and outputs',
                    action='store_true')
parser.add_argument('-e',
                    '--execute',
                    help='Execute program using IO files',
                    action='store_true')
parser.add_argument('-s',
                    '--show',
                    help='Shows problem input',
                    action='store_true')
parser.add_argument('-r',
                    '--remove',
                    help='Remove most recent testcase',
                    action='store_true')
parser.add_argument('-f',
                    '--fetch',
                    metavar=('SITE'),
                    help='Clear and fetch inputs and outputs from site',
                    required=False)
parser.add_argument('-t',
                    '--type',
                    default='contest',
                    help='Type of contest URL (e.g. gym, contest, etc.)',
                    required=False)
parser.add_argument('-a',
                    '--add',
                    metavar=('NUMBER'),
                    help='Add NUMBER testcases to collection',
                    required=False)


args = parser.parse_args()
tester = codetester.CodeTester()

if args.clear:
    tester.clear()

if args.type:
    tester.set_type(args.type)

if args.remove:
    tester.remove_last()

if args.fetch:
    if int(args.fetch[:-1]) >= 0 \
       and args.fetch[-1] >= 'A' and args.fetch[-1] <= 'Z':
        tester.fetch(args.fetch)
    else:
        print 'Invalid contest number or problem letter'

if args.add:
    if(int(args.add) < 0):
        print 'Invalid number of additions'
        sys.exit(1)

    for i in range(int(args.add)):
        tester.add()

if args.show:
    tester.show_input()

if args.execute:
    tester.test()
