from utils import *
import sys

verbose = "verbose" in sys.argv
files = os.listdir()    
for f in files:
    if(f.startswith("test") and f.endswith(".py")):
        test_eq_console_output(f, verbose)