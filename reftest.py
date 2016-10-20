import tarfile # prace s archivy
import filecmp # porovnavani souboru
import os # volani operacnimu systemu
import subprocess # volani podprocesu
import argparse # parsovani argumentu
import shutil # shell utilities (konkretne mazani celeho file tree)
#import sys
#import time
#import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# predpripravene promenne
jmeno_slozky_archiv = 'extracted_archive'



# funkce overujici existenci souboru v argumentu
def is_valid_file(parser, arg):
    if not os.path.exists(arg):
        parser.error("The file %s does not exist!" % arg)
    else:
        return open(arg, 'r')

# handler ktery resi, jestli byl soubor zmenen
class MyHandler(FileSystemEventHandler):
    def __init__(self, jmenosouboru):
        self.jmenosouboru = jmenosouboru
    def on_modified(self, event):
        if event.src_path.endswith('/'+self.jmenosouboru):
            # print event.src_path+', '+event.event_type
            print self.jmenosouboru+' byl zmenen!'

# funkce vraci working directory
def pwd():
    return os.path.dirname(os.path.abspath(__file__))

# funkce vraci expandovane cesty
def relabscesta(nazev):
    return os.path.abspath(os.path.expanduser(nazev))
'''
class FullPaths(argparse.Action):
    """Expand user- and relative-paths"""
    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, os.path.abspath(os.path.expanduser(values)))
'''

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

# blok parsovani argumentu
# https://docs.python.org/2/library/argparse.html
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
# argument pro povoleni watchdog (sledovaciho) modu
parser.add_argument('-w', '--watchdog', help='Enables Watchdog mode',
                    action='store_true')

# argumenty, ktere budou pouzity, ale jsou vyple kvuli debugu
"""
# argument prijimajici cestu k zkompilovanemu programu
parser.add_argument("-e", '--executable', dest="executable", required=False,
                    help="executable file (default \"a.out\")", metavar="FILE.OUT",
                    type=lambda x: is_valid_file(parser, x),
                    default="a.out")
"""
# argument prijimajici cestu k archivu s referencnimi daty
parser.add_argument("-a", '--archive', dest="archive", required=False,
                    help=".tgz with ref. I/O (default \"sample.tgz\")",
                    metavar="FILE.TGZ",
                    type=lambda x: is_valid_file(parser, x),
                    default="sample.tgz")



# parsuje argumenty
args = parser.parse_args()

# expandovani relativni/absolutni cesty
archive_cesta = relabscesta(args.archive.name)

# blok WATCHDOG
# http://pythonhosted.org/watchdog/
# http://stackoverflow.com/questions/11883336/detect-file-creation-with-watchdog
# http://stackoverflow.com/questions/18599339/python-watchdog-monitoring-file-for-changes
# http://stackoverflow.com/questions/32313989/check-specific-file-has-been-modified-using-python-watchdog
if (args.watchdog == True):
    '''
    # to tu bylo z dokumentace
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    '''
    # adresar pro sledovani
    path = '.'
    # volim vlastni handler, ktery si vsima pouze jednoho souboru
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

# vlezeme do slozky pro extrakci
os.makedirs(jmeno_slozky_archiv)
os.chdir(jmeno_slozky_archiv)

# extrakce
tar = tarfile.open(archive_cesta)
tar.extractall()
tar.close()

# o slozku vys
os.chdir('..')

'''
TODO

postupne porovnani vsech vystupu s referencnimi
problematicke vstupy budou podrobne vypsany do terminalu (barevne)

'''

# uklidime
shutil.rmtree(jmeno_slozky_archiv)
