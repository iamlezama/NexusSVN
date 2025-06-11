import os
import sys

DEFAULT_WORKING_COPIES_DIR = os.path.join(os.path.expanduser("~"), "SVNWorkingCopies")
CONFIG_FILE = "config.json"
TORTOISE_PROC_PATH = "TortoiseProc.exe"

def get_bundle_dir():
    if getattr(sys, 'frozen', False):
        return sys._MEIPASS
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

BUNDLE_ROOT = get_bundle_dir()
if getattr(sys, 'frozen', False):
    # Frozen: look for bin inside the extracted _MEIxxxx folder
    SVN_BUNDLE = os.path.join(BUNDLE_ROOT, 'bin', 'svn', 'Apache-Subversion-1.14.5-2', 'bin')
else:
    # Dev mode: go up from src/ to project root, then into bin
    SVN_BUNDLE = os.path.join(BUNDLE_ROOT, '..', 'bin', 'svn', 'Apache-Subversion-1.14.5-2', 'bin')
SVN_EXECUTABLE = os.path.abspath(os.path.join(SVN_BUNDLE, 'svn.exe'))

# --- Diagnostics (to file for both modes) ---
try:
    with open("diagnostics.txt", "w") as f:
        f.write("======== SVN Executable Diagnostics ========\n")
        f.write(f"sys.frozen: {getattr(sys, 'frozen', False)}\n")
        f.write(f"get_bundle_dir(): {BUNDLE_ROOT}\n")
        f.write(f"SVN_BUNDLE: {SVN_BUNDLE}\n")
        f.write(f"SVN_EXECUTABLE: {SVN_EXECUTABLE}\n")
        f.write(f"Exists: {os.path.exists(SVN_EXECUTABLE)}\n")
        f.write("===========================================\n")
        if not os.path.exists(SVN_EXECUTABLE):
            f.write("WARNING: svn.exe not found at the expected location above.\n")
except Exception as e:
    pass