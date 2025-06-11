import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkcalendar import Calendar

class MainWindow(ttk.Frame):
        def __init__(self, master):
                super().__init__(master, padding="20 20 20 20")
                self.grid(row=1, column=0, sticky="nsew")
                self.grid_columnconfigure(0, weight=1)
                self.grid_rowconfigure(0, weight=1)
                
                # Add a status label at the bottom of the window
                self.status_label = ttk.Label(master, text="Ready", anchor="w")
                self.status_label.grid(row=2, column=0, sticky="ew", padx=10, pady=5)
                # Styles
                style = ttk.Style()
                style.theme_use("clam")
                style.configure("TFrame", background="#f0f0f0")
                style.configure("TLabel", background="#f0f0f0", font=("Inter", 10))
                style.configure("TButton", font=("Inter", 10, "bold"), padding=8)
                style.map("TButton",
                        background=[('active', '#e0e0e0'), ('!disabled', '#007bff')],
                        foreground=[('active', 'black'), ('!disabled', 'white')])
                style.configure("TEntry", fieldbackground="white", font=("Inter", 10), padding=5)
                style.configure("TCalendar",
                                background="white",
                                selectbackground="#007bff",
                                normalbackground="white",
                                foreground="black",
                                headersbackground="#0056b3",
                                headersforeground="white")
                self.notebook = ttk.Notebook(self)
                self.notebook.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
                self.notebook.grid_columnconfigure(0, weight=1)
                self._create_checkout_tab()
                self._create_commit_tab()
                self._create_status_tab()
        def _create_checkout_tab(self):
                self.checkout_frame = ttk.Frame(self.notebook, padding="15 15 15 15")
                self.notebook.add(self.checkout_frame, text="SVN Checkout")
                self.checkout_frame.grid_columnconfigure(1, weight=1)
                ttk.Label(self.checkout_frame, text="Working Directory:").grid(row=0, column=0, sticky="w", pady=5)
                self.working_copies_dir_var = tk.StringVar()
                ttk.Entry(self.checkout_frame, textvariable=self.working_copies_dir_var, width=60).grid(row=0, column=1, sticky="ew", padx=5, pady=5)
                self.browse_wc_button = ttk.Button(self.checkout_frame, text="Browse...")
                self.browse_wc_button.grid(row=0, column=2, sticky="e", padx=5, pady=5)
                ttk.Label(self.checkout_frame, text="Repository URL:").grid(row=1, column=0, sticky="w", pady=5)
                self.repo_url_var = tk.StringVar()
                ttk.Entry(self.checkout_frame, textvariable=self.repo_url_var, width=60).grid(row=1, column=1, sticky="ew", padx=5, pady=5)
                ttk.Label(self.checkout_frame, text="Path Segment:").grid(row=2, column=0, sticky="w", pady=5)
                self.path_segment_var = tk.StringVar()
                ttk.Entry(self.checkout_frame, textvariable=self.path_segment_var, width=60).grid(row=2, column=1, sticky="ew", padx=5, pady=5)
                self.checkout_button = ttk.Button(self.checkout_frame, text="Perform SVN Checkout")
                self.checkout_button.grid(row=3, column=1, sticky="e", pady=10)
        def _create_commit_tab(self):
                self.commit_frame = ttk.Frame(self.notebook, padding="15 15 15 15")
                self.notebook.add(self.commit_frame, text="Scheduled Commit")
                self.commit_frame.grid_columnconfigure(1, weight=1) # Enable column for path entry
                # Radiobuttons for commit type
                self.commit_type = tk.StringVar(value="reminder") # Default value
                ttk.Radiobutton(self.commit_frame, text="Reminder", variable=self.commit_type, value="reminder").grid(row=0, column=0, sticky="w", pady=5)
                ttk.Radiobutton(self.commit_frame, text="Automatic Commit", variable=self.commit_type, value="automatic").grid(row=1, column=0, sticky="w", pady=5)
                # Calendar for date selection
                ttk.Label(self.commit_frame, text="Select Date:").grid(row=2, column=0, sticky="w", pady=(10,0))
                self.cal = Calendar(self.commit_frame, selectmode='day', date_pattern="yyyy-mm-dd")
                self.cal.grid(row=3, column=0, columnspan=2, pady=10, sticky="ew") # Spanning two columns
                # Entry for time
                ttk.Label(self.commit_frame, text="Time (HH:MM):").grid(row=4, column=0, sticky="w", pady=5)
                self.hour_entry = ttk.Entry(self.commit_frame, width=10)
                self.hour_entry.grid(row=4, column=1, sticky="w", padx=5, pady=5) # Place in column 1
                # New: Path for Scheduled Commit
                ttk.Label(self.commit_frame, text="Commit Path:").grid(row=5, column=0, sticky="w", pady=5)
                self.commit_path_var = tk.StringVar()
                ttk.Entry(self.commit_frame, textvariable=self.commit_path_var, width=60).grid(row=5, column=1, sticky="ew", padx=5, pady=5)
                self.browse_commit_path_button = ttk.Button(self.commit_frame, text="Browse...")
                self.browse_commit_path_button.grid(row=5, column=2, sticky="e", padx=5, pady=5)
                # Entry for commit message
                ttk.Label(self.commit_frame, text="Reminder Message:").grid(row=6, column=0, sticky="w", pady=5)
                self.message_entry = ttk.Entry(self.commit_frame, width=60) # Increased width
                self.message_entry.grid(row=6, column=1, columnspan=2, sticky="ew", padx=5, pady=5) # Spanning across columns
                # Button to schedule the commit
                self.schedule_commit_button = ttk.Button(self.commit_frame, text="Schedule Commit")
                self.schedule_commit_button.grid(row=7, column=1, sticky="e", pady=10) # Adjusted row/column
        def _create_status_tab(self):
                self.status_frame = ttk.Frame(self.notebook, padding="15 15 15 15")
                self.notebook.add(self.status_frame, text="Uncommitted Changes")
                self.status_frame.grid_columnconfigure(1, weight=1)
                ttk.Label(self.status_frame, text="Working Directory:").grid(row=0, column=0, sticky="w", pady=5)
                self.status_dir_var = tk.StringVar()
                ttk.Entry(self.status_frame, textvariable=self.status_dir_var, width=60).grid(row=0, column=1, sticky="ew", padx=5, pady=5)
                self.browse_status_button = ttk.Button(self.status_frame, text="Browse...")
                self.browse_status_button.grid(row=0, column=2, sticky="e", padx=5, pady=5)
                self.view_changes_button = ttk.Button(self.status_frame, text="View Uncommitted Changes")
                self.view_changes_button.grid(row=1, column=1, sticky="e", pady=10)
                ttk.Label(self.status_frame, text="Folders with Uncommitted Changes:").grid(row=2, column=0, sticky="w", pady=(10, 0))
                self.changes_listbox = tk.Listbox(self.status_frame, height=10, width=100)
                self.changes_listbox.grid(row=3, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
                scrollbar = ttk.Scrollbar(self.status_frame, orient="vertical", command=self.changes_listbox.yview)
                scrollbar.grid(row=3, column=2, sticky="ns")
                self.changes_listbox.config(yscrollcommand=scrollbar.set)
                self.open_selected_button = ttk.Button(self.status_frame, text="Open Selected in TortoiseSVN")
                self.open_selected_button.grid(row=4, column=1, sticky="e", pady=5)
                self.export_list_button = ttk.Button(self.status_frame, text="Export List to File")
                self.export_list_button.grid(row=4, column=0, sticky="w", pady=5)
        def _browse_working_copies_dir(self):
                directory = filedialog.askdirectory(title="Select Working Directory")
                if directory:
                        return directory
                return None
        def _browse_status_dir(self):
                directory = filedialog.askdirectory(title="Select Directory for Status Check")
                if directory:
                        return directory
                return None
        def update_changes_listbox(self, changes_list):
                self.changes_listbox.delete(0, tk.END)
                if changes_list:
                        for path in changes_list:
                                self.changes_listbox.insert(tk.END, path)
                else:
                        messagebox.showinfo("No Changes", "No uncommitted changes found in your working copies.")
        def _browse_commit_path_dir(self):
                directory = filedialog.askdirectory(title="Select Directory for Scheduled Commit")
                if directory:
                        return directory
                return None