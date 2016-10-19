import tarfile
import filecmp
import os
import subprocess
import argparse
import shutil

import sys
import time
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# funkce overujici existenci souboru v argumentu
def is_valid_file(parser, arg):
    if not os.path.exists(arg):
        parser.error("The file %s does not exist!" % arg)
    else:
        return open(arg, 'r')

# handler kterej resi, jestli byl soubor zmenen
class MyHandler(FileSystemEventHandler):
    def __init__(self, jmenosouboru):
        self.jmenosouboru = jmenosouboru
    def on_modified(self, event):
        if event.src_path.endswith('/'+self.jmenosouboru):
            # print event.src_path+', '+event.event_type
            print self.jmenosouboru+' byl zmenen!'

# barvickyyyyyy
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# print bcolors.WARNING + "Takhle se pouzivaji!" + bcolors.ENDC

parser = argparse.ArgumentParser(description="""Check if your PA1
                                             homework does what it should
                                             do!""")
# DEFAULT ARGUMENTY Z DOKUMENTACE
"""
parser.add_argument('integers', metavar='N', type=int, nargs='+',
                    help='an integer for the accumulator')
parser.add_argument('--sum', dest='accumulate', action='store_const',
                    const=sum, default=max,
                    help='sum the integers (default: find the max)')
"""

# argument pro povoleni vystupu
parser.add_argument('-v', '--verbose', help='Print output',
                    action='store_true')

parser.add_argument('-w', '--watchdog', help='Enables Watchdog mode',
                    action='store_true')

# ARGUMENTY KTERE BUDOU POUZITY ALE KVULI DEBUGU JSOU VYPLE
"""
# argument prijimajici cestu k zkompilovanemu programu
parser.add_argument("-e", '--executable', dest="executable", required=False,
                    help="executable file (default \"a.out\")", metavar="FILE.OUT",
                    type=lambda x: is_valid_file(parser, x),
                    default="a.out")

# argument prijimajici cestu k archivu s referencnimi daty
parser.add_argument("-a", '--archive', dest="archive", required=False,
                    help=".tar with ref. I/O (default \"sample.tar.gz\")",
                    metavar="FILE.TGZ",
                    type=lambda x: is_valid_file(parser, x),
                    default="sample.tar.gz")
"""


args = parser.parse_args()
#print(args.executable.name)
if (args.watchdog == True):
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = '.' #sys.argv[1] if len(sys.argv) > 1 else '.'
    event_handler = MyHandler('a.out')
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
#print args.accumulate(args.integers)
'''
os.makedirs('test')
os.chdir('test')

tar = tarfile.open("../sample.tgz")
tar.extractall()
tar.close()

os.chdir('..')
'''
#shutil.rmtree('test')



# print os.path.dirname(os.path.abspath(__file__))
