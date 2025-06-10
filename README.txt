SVN Helper Tool
This lightweight tool helps SVN users with three key tasks:
1. Automated SVN Checkout:
  - Enter the full repo URL
  - Specify the path segment to start from
  - It creates the folder structure and runs the checkout using TortoiseSVN
2. Check Uncommitted Files:
  - Opens the TortoiseSVN Repostatus window for your working copies folder
3. Schedule a Commit:
  - Select a future date and time from a calendar
  - When the time comes, you’ll be prompted to confirm whether to proceed with the commit
SETUP:
- Requires TortoiseSVN installed (should include TortoiseProc.exe)
- Requires Python 3.x installed
- Install dependencies once with: `pip install tkcalendar`
USAGE:
- Open `main.py` with VS Code or double-click if Python is properly linked
- You can save your `working_copies` path to avoid retyping
SHARING:
- You can zip this folder and share via OneDrive or copy it to another corporate machine
- No need to install anything globally