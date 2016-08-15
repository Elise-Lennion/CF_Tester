import os
import subprocess as sp
from bs4 import BeautifulSoup
import requests


class CodeTester:
    """
    Test executable with defined input and output files.

    Also fetch information at Codeforces and automatically
    creates input and output files.
    Supports manual addition of testcases.

    Change EXEC_NAME to correspond with the executable you're using
    """

    def __init__(self):

        self._URL = "http://codeforces.com"
        self._TYPE = ''
        self._NUMBER = '0'
        self._PROBLEM = 'A'
        self._FOLDER_INPUT = os.getcwd() + '/input/'
        self._FOLDER_OUTPUT = os.getcwd() + '/output/'

        self._EXEC_NAME = 'amethyst'

    def clear(self):
        """Removes all stored input and output files"""

        for file in os.listdir(self._FOLDER_INPUT):
            os.remove(self._FOLDER_INPUT + file)

        for file in os.listdir(self._FOLDER_OUTPUT):
            os.remove(self._FOLDER_OUTPUT + file)

    def full_url(self):
        """Returns full URL of problem"""

        return '/'.join(
            [self._URL, self._TYPE, self._NUMBER, 'problem', self._PROBLEM])

    def fetch(self, problem):
        """Fetchs input and output files from URL"""

        self._NUMBER = problem[:-1]
        self._PROBLEM = problem[-1]

        self.clear()  # Remove old testcases before fetching new ones

        try:
            request = requests.get(self.full_url(), allow_redirects=False)
            if request.text == '':
                print 'URL not found!'
                return

        except requests.exceptions.RequestException as e:
            print e
            return

        data = request.text
        soup = BeautifulSoup(data, 'lxml')

        for input in soup.find_all('div', {'class': 'input'}):
            for node in input.find_all('pre'):
                file = open(self._FOLDER_INPUT + 'in'
                            + str(len(os.listdir(self._FOLDER_INPUT))), 'w')
                file.write('\n'.join(node.findAll(text=True)))

        for output in soup.find_all('div', {'class': 'output'}):
            for node in output.find_all('pre'):
                file = open(self._FOLDER_OUTPUT + 'out'
                            + str(len(os.listdir(self._FOLDER_OUTPUT))), 'w')
                file.write('\n'.join(node.findAll(text=True)))

        print 'Success fetching testcases!'

    def add(self):
        """Add new testcase to input and output folders"""

        inp = ''
        out = ''
        amber = []

        print 'Insert Input:\n'

        while 1:
            try:
                amber.append(raw_input())
            except EOFError:
                inp = '\n'.join(amber)
                break

        file = open(self._FOLDER_INPUT + 'in'
                    + str(len(os.listdir(self._FOLDER_INPUT))), 'w')
        file.write(inp)

        print 'Insert Expected Output:\n'

        amber = []

        while 1:
            try:
                amber.append(raw_input())
            except EOFError:
                out = '\n'.join(amber)
                break

        file = open(self._FOLDER_OUTPUT + 'out'
                    + str(len(os.listdir(self._FOLDER_OUTPUT))), 'w')
        file.write(out)

    def remove_last(self):
        """Remove most recent added testcase"""

        inps = sorted(os.listdir(self._FOLDER_INPUT))
        outs = sorted(os.listdir(self._FOLDER_OUTPUT))

        if inps:
            os.remove('/'.join([self._FOLDER_INPUT, inps[-1]]))
        if outs:
            os.remove('/'.join([self._FOLDER_OUTPUT, outs[-1]]))

    def test(self):
        """Execute program and check correctness of output"""

        if self._EXEC_NAME not in os.listdir(os.getcwd()):
            print 'Executable not found'
            return

        outs = []
        inps = sorted(os.listdir(self._FOLDER_INPUT))
        expected = ''

        for i, inp in enumerate(inps):
            try:
                result = sp.check_output(
                    ['/'.join([os.getcwd(), self._EXEC_NAME])],
                    stdin=open(self._FOLDER_INPUT + inp))

                if result[-1] == '\n':
                    result = result[:-1]
            except:
                result = 'SEGMENTATION FAULT!'

            outs.append(result)

            with open(self._FOLDER_OUTPUT + 'out' + str(i), 'r') as exp:
                expected = exp.read()

            if result == 'SEGMENTATION FAULT!':
                print 'Test ' + str(i) + ' SEGMENTATION FAULT!'
                continue

            if result == expected:
                print 'Test ' + str(i) + ' ok!'
            else:
                print 'Test ' + str(i) + ' wrong!'
                print 'Your output:\n' + result \
                    + '\nExpected output:\n' + expected

    def set_type(self, type):
        """Set contest type"""

        self._TYPE = type
