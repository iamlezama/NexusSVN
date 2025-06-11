import os
import sys

def get_bundle_dir():
    # for PyInstaller compatibility
    if getattr(sys, 'frozen', False):
        return sys._MEIPASS
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SVN_BUNDLE = os.path.join(get_bundle_dir(), '..', 'bin', 'svn', 'Apache-Subversion-1.14.5-2', 'bin')
SVN_EXECUTABLE = os.path.join(SVN_BUNDLE, 'svn.exe')

DEFAULT_WORKING_COPIES_DIR = os.path.join(os.path.expanduser("~"), "SVNWorkingCopies")
CONFIG_FILE = "config.json"
TORTOISE_PROC_PATH = "TortoiseProc.exe"