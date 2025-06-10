import tkinter as tk
import datetime
import os
from tkinter import messagebox, filedialog
from src.ui.main_window import MainWindow
from src.core.config_manager import ConfigManager
from src.core.svn_operations import SVNOperations
from src.utils.constants import DEFAULT_WORKING_COPIES_DIR

class NexusSVNApp:
    def __init__(self, master):
            self.master = master
            master.title("Nexus SVN")
            master.geometry("800x600")
            master.resizable(True, True)
            master.grid_columnconfigure(0, weight=1)
            master.grid_rowconfigure(0, weight=0)
            master.grid_rowconfigure(1, weight=1)
            self.config_manager = ConfigManager()
            self.svn_operations = SVNOperations()
            self.main_window = MainWindow(master)
            self._set_initial_ui_values()
            self._bind_ui_actions()
    def _set_initial_ui_values(self):
            self.main_window.working_copies_dir_var.set(self.config_manager.get("working_copies_dir", DEFAULT_WORKING_COPIES_DIR))
            self.main_window.repo_url_var.set(self.config_manager.get("repo_url", ""))
            self.main_window.path_segment_var.set(self.config_manager.get("path_segment", ""))
            self.main_window.status_dir_var.set(self.config_manager.get("working_copies_dir", DEFAULT_WORKING_COPIES_DIR))
            self.main_window.commit_path_var.set(self.config_manager.get("working_copies_dir", DEFAULT_WORKING_COPIES_DIR))
    def _bind_ui_actions(self):
            self.main_window.browse_wc_button.config(command=self._handle_browse_working_copies_dir)
            self.main_window.checkout_button.config(command=self._handle_perform_checkout)
            self.main_window.browse_status_button.config(command=self._handle_browse_status_dir)
            self.main_window.view_changes_button.config(command=self._handle_scan_for_uncommitted_changes)
            self.main_window.open_selected_button.config(command=self._handle_open_selected_change)
            self.main_window.export_list_button.config(command=self._handle_export_changes_list)
            self.main_window.browse_commit_path_button.config(command=self._handle_browse_commit_path_dir)
            self.main_window.schedule_commit_button.config(command=self._handle_schedule_commit)
    def _handle_browse_working_copies_dir(self):
            directory = self.main_window._browse_working_copies_dir() # Call UI method
            if directory:
                self.main_window.working_copies_dir_var.set(directory)
                self.config_manager.set("working_copies_dir", directory)
                self.main_window.status_dir_var.set(directory)
    def _handle_browse_status_dir(self):
            directory = self.main_window._browse_status_dir() # Call UI method
            if directory:
                self.main_window.status_dir_var.set(directory)
    def _handle_perform_checkout(self):
            repo_url = self.main_window.repo_url_var.get().strip()
            path_segment = self.main_window.path_segment_var.get().strip()
            working_copies_dir = self.main_window.working_copies_dir_var.get().strip()
            if not repo_url:
                messagebox.showwarning("Input Error", "Repository URL cannot be empty.")
                return
            if not working_copies_dir:
                messagebox.showwarning("Input Error", "Working Copies Directory cannot be empty.")
                return
            self.config_manager.set("repo_url", repo_url)
            self.config_manager.set("path_segment", path_segment)
            self.config_manager.set("working_copies_dir", working_copies_dir)
            self.svn_operations.perform_checkout(repo_url, path_segment, working_copies_dir)
    def _handle_browse_commit_path_dir(self):
        directory = self.main_window._browse_commit_path_dir()
        if directory:
            self.main_window.commit_path_var.set(directory)
    def _handle_schedule_commit(self):
        commit_type = self.main_window.commit_type.get()
        selected_date = self.main_window.cal.selection_get()
        hour_str = self.main_window.hour_entry.get().strip()
        commit_message = self.main_window.message_entry.get().strip()
        repo_path = self.main_window.commit_path_var.get().strip()
        # Input validation for scheduling
        if not selected_date:
            messagebox.showwarning("Input Error", "Please select a date for the scheduled commit.")
            return
        if not hour_str:
            messagebox.showwarning("Input Error", "Please enter a time for the scheduled commit (HH:MM).")
            return
        if not commit_message:
            messagebox.showwarning("Input Error", "Please enter a commit message.")
            return
        if not repo_path:
            messagebox.showwarning("Input Error", "Please specify a directory for the scheduled commit.")
            return
        if not os.path.isdir(repo_path): # Basic path validation
            messagebox.showerror("Invalid Path", f"The specified commit path '{repo_path}' is not a valid directory.")
            return
        if not os.path.exists(os.path.join(repo_path, ".svn")):
                messagebox.showwarning("Not an SVN Working Copy", f"'{repo_path}' does not appear to be an SVN working copy. Scheduled commit might not work as expected.")

        # Combine date and time
        try:
            commit_time_obj = datetime.datetime.strptime(f"{selected_date.year}-{selected_date.month}-{selected_date.day} {hour_str}", "%Y-%m-%d %H:%M")
        except ValueError:
            messagebox.showerror("Input Error", "Invalid time format. Use HH:MM (e.g., 14:30).")
            return
        # Call the core SVN operation for scheduling
        self.svn_operations.schedule_commit_action(
            commit_type,
            commit_time_obj,
            commit_message,
            repo_path
        )
    def _handle_scan_for_uncommitted_changes(self):
            base_dir = self.main_window.working_copies_dir_var.get().strip()
            # It's better for core logic to return data, and UI to display it.
            # messagebox calls were moved to core, but ideally, core returns result/error, and app handles messagebox
            changes = self.svn_operations.scan_for_uncommitted_changes(base_dir)
            self.main_window.update_changes_listbox(changes)
    def _handle_open_selected_change(self):
            selection = self.main_window.changes_listbox.curselection()
            if not selection:
                messagebox.showwarning("No Selection", "Please select a folder from the list.")
                return
            selected_path = self.main_window.changes_listbox.get(selection[0])
            self.svn_operations.open_tortoise_commit_dialog(selected_path)
    def _handle_export_changes_list(self):
            file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                            filetypes=[("Text Files", "*.txt")],
                                                                title="Save List As")
            if file_path:
                self.svn_operations.export_changes_list(file_path)