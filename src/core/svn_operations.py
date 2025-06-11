import subprocess
import os
import re
import datetime
import time
import threading
from tkinter import messagebox
from src.utils.constants import TORTOISE_PROC_PATH, SVN_EXECUTABLE

class SVNOperations:
    def __init__(self):
        self.uncommitted_dirs = []
    def perform_checkout(self, repo_url, path_segment, working_copies_dir):
        try:
            repo_path_match = re.search(f".*?({re.escape(path_segment)}.*)", repo_url, re.IGNORECASE) 
            if repo_path_match:
                repo_subpath = repo_path_match.group(1) 
            else:
                messagebox.showerror("Checkout Error",
                                    f"Path segment '{path_segment}' not found in the Repository URL." 
                                    f"Please ensure it's part of the URL.") 
                return
            repo_subpath = repo_subpath.replace('/', os.sep).replace('\\', os.sep) 
            if repo_subpath.startswith(os.sep): 
                repo_subpath = repo_subpath[1:] 
            full_target_dir = os.path.join(working_copies_dir, repo_subpath) 
            os.makedirs(full_target_dir, exist_ok=True)
            checkout_command = [
                TORTOISE_PROC_PATH, 
                f'/command:checkout', 
                f'/path:"{full_target_dir}"',
                f'/url:"{repo_url}"',
                '/closeonend:1'
            ]
            messagebox.showinfo("SVN Checkout", f"Starting checkout to: {full_target_dir}\nThis may take a moment...")
            process = subprocess.run(" ".join(checkout_command), shell=True, capture_output=True, text=True)
            if process.returncode == 0:
                messagebox.showinfo("SVN Checkout Success", f"Checkout completed successfully to:\n{full_target_dir}")
                os.startfile(full_target_dir)
            elif process.returncode == 255 or process.returncode == -1 or process.returncode == 4294967295: # Common return codes for user cancellation
                messagebox.showinfo("SVN Checkout Cancelled", "The SVN checkout operation was cancelled by the user.")
            else:
                error_message = f"SVN Checkout failed with exit code {process.returncode}.\n" \
                                f"Command: {' '.join(checkout_command)}\n" \
                                f"Output:\n{process.stdout}\nError:\n{process.stderr}"
                messagebox.showerror("SVN Checkout Error", error_message)
        except FileNotFoundError:
            messagebox.showerror("Error", f"TortoiseProc.exe not found. "
                                            f"Please ensure TortoiseSVN is installed and {TORTOISE_PROC_PATH} is in your system's PATH.")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred during checkout: {e}")
    def schedule_commit_action(self, commit_type, commit_datetime, commit_message, repo_path):
        now = datetime.datetime.now()
        delay_seconds = (commit_datetime - now).total_seconds()
        if delay_seconds < 0:
            messagebox.showwarning("Invalid Date/Time", "The scheduled date and time has already passed. Please select a future date and time.")
            return
        messagebox.showinfo("Commit Scheduled",
                            f"Commit scheduled for {commit_datetime.strftime('%Y-%m-%d %H:%M')} "
                            f"({'Automatic' if commit_type == 'automatic' else 'Reminder'}).")
        threading.Thread(target=self._execute_scheduled_action,
                        args=(commit_type, commit_datetime, commit_message, delay_seconds, repo_path)).start()
    def _execute_scheduled_action(self, commit_type, commit_datetime, commit_message, delay_seconds, repo_path):
        time.sleep(delay_seconds) # Wait until the scheduled time
        if commit_type == "automatic":
            messagebox.showinfo("Automatic Commit Executed",
                                f"Automatic commit executed at {commit_datetime.strftime('%H:%M')}!\n"
                                f"Message: '{commit_message}'\n"
                                f"Opening TortoiseSVN commit dialog for: {repo_path}")
            self.open_tortoise_commit_dialog(repo_path)
        elif commit_type == "reminder":
            messagebox.showinfo("Commit Reminder",
                                f"Commit reminder at {commit_datetime.strftime('%H:%M')}!\n"
                                f"Message: '{commit_message}'\n"
                                f"It's time to perform your manual commit for: {repo_path}")
            self.open_tortoise_commit_dialog(repo_path)
    def scan_for_uncommitted_changes(self, base_dir):
        if not base_dir or not os.path.isdir(base_dir):
            messagebox.showwarning("Input Error", "Please specify a valid Working Copies Directory.")
            return []
        svn_dirs_with_changes = []
        for root, dirs, files in os.walk(base_dir):
            if '.svn' in dirs:
                try:
                    result = subprocess.run(
                        [SVN_EXECUTABLE, 'status'], 
                        cwd=root, 
                        capture_output=True, 
                        text=True,
                        creationflags=subprocess.CREATE_NO_WINDOW)
                    if result.stdout.strip():
                        svn_dirs_with_changes.append(root)
                except Exception as e:
                    print(f"Error checking {root}: {e}")
        self.uncommitted_dirs = svn_dirs_with_changes
        return svn_dirs_with_changes
    def open_tortoise_commit_dialog(self, path):
        try:
            status_command = f'{TORTOISE_PROC_PATH} /command:commit /path:"{path}" /closeonend:1'
            subprocess.Popen(status_command, shell=True)
        except Exception as e:
            messagebox.showerror("Error", f"Could not open TortoiseSVN for the selected folder:\n{e}")
    def export_changes_list(self, file_path):
        if not hasattr(self, 'uncommitted_dirs') or not self.uncommitted_dirs:
            messagebox.showinfo("No Data", "No uncommitted changes to export.")
            return
        if file_path:
            try:
                with open(file_path, 'w') as f:
                    for path in self.uncommitted_dirs:
                        f.write(path + '\n')
                messagebox.showinfo("Export Successful", f"List exported to:\n{file_path}")
            except Exception as e:
                messagebox.showerror("Export Error", f"Could not export the list:\n{e}")
    def view_uncommitted_changes_single_dir(self, working_dir):
        working_dir = working_dir.strip()
        if not working_dir:
            messagebox.showwarning("Input Error", "Working Directory for Status cannot be empty.")
            return
        normalized_working_dir = os.path.normpath(working_dir)
        if not os.path.isdir(normalized_working_dir):
            messagebox.showerror("Invalid Directory", f"The specified path '{normalized_working_dir}' is not a valid directory.")
            return
        if not os.path.exists(os.path.join(normalized_working_dir, ".svn")):
            messagebox.showwarning("Not a Working Copy",
                                    f"'{normalized_working_dir}' does not appear to be an SVN working copy."
                                    "TortoiseSVN status might not work as expected.")
        try:
            status_command = f'{TORTOISE_PROC_PATH} /command:commit /path:"{normalized_working_dir}" /closeonend:1'
            messagebox.showinfo("SVN Status", f"Opening TortoiseSVN commit dialog for:\n{normalized_working_dir}")
            subprocess.Popen(status_command, shell=True)
        except FileNotFoundError:
            messagebox.showerror("Error", f"TortoiseProc.exe not found. "
                                            f"Please ensure TortoiseSVN is installed and "
                                            f"{TORTOISE_PROC_PATH} is in your system's PATH.")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred viewing status: {e}")