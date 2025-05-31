# gui_launcher.py

import tkinter as tk
from tkinter import filedialog, messagebox
from operations.path_checker import PathFinder
from operations.file_selection import FileSelection
from operations.file_organiser import FileOrganizer


class FileOrganizerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("📁 File Organizer - CYBER MODE")
        self.root.geometry("750x600")
        self.root.resizable(False, False)

        # Set dark theme
        self.bg_color = "#1a1a1a"
        self.fg_color = "#00ffff"
        self.accent_color = "#ff0080"
        self.button_color = "#00bfff"

        self.root.configure(bg=self.bg_color)

        # Title
        tk.Label(root, text="File Organizer", font=("Courier", 20, "bold"), fg=self.fg_color, bg=self.bg_color).pack(pady=10)

        # Working Directory
        self.wrk_dir_var = tk.StringVar()
        self._create_browse_row("Working Directory:", self.wrk_dir_var, self.select_working_dir)

        # Destination Directory
        self.dst_dir_var = tk.StringVar()
        self._create_browse_row("Destination Directory:", self.dst_dir_var, self.select_destination_dir)

        # File Type Selection
        self.choice_var = tk.StringVar(value="2")
        tk.Label(root, text="Select File Type:", font=("Courier", 12), fg=self.fg_color, bg=self.bg_color).pack(anchor="w", padx=30)
        file_types = {
            "PDF": "1",
            "Images": "2",
            "Audio": "3",
            "Video": "4",
            "Docs": "5",
            "Code": "6"
        }
        for text, val in file_types.items():
            tk.Radiobutton(
                root,
                text=text,
                variable=self.choice_var,
                value=val,
                fg=self.accent_color,
                selectcolor=self.bg_color,
                bg=self.bg_color,
                font=("Courier", 10),
                indicatoron=0,
                width=10
            ).pack(anchor="w", padx=40, pady=2)

        # Recursive Mode
        self.recursive_var = tk.BooleanVar()
        tk.Checkbutton(
            root,
            text="Include Subfolders",
            variable=self.recursive_var,
            fg=self.fg_color,
            bg=self.bg_color,
            font=("Courier", 10)
        ).pack(pady=10)

        # OK Button
        tk.Button(
            root,
            text="✔️ OK - Confirm Settings",
            command=self.confirm_settings,
            bg=self.button_color,
            fg="black",
            font=("Courier", 10, "bold"),
            width=25
        ).pack(pady=10)

        # Run Button (Initially disabled until OK is clicked)
        self.run_button = tk.Button(
            root,
            text="🚀 Organize Files",
            command=self.run_organizer,
            bg=self.accent_color,
            fg="white",
            font=("Courier", 12, "bold"),
            state=tk.DISABLED
        )
        self.run_button.pack(pady=10)

        # Output Log
        self.log_text = tk.Text(
            root,
            height=10,
            width=80,
            bg="#111111",
            fg="#00FFAA",
            font=("Courier", 10),
            state='disabled'
        )
        self.log_text.pack(pady=10)

        # Internal flag
        self.settings_confirmed = False

    def _create_browse_row(self, label_text, var, callback):
        frame = tk.Frame(self.root, bg=self.bg_color)
        frame.pack(fill="x", padx=20, pady=5)

        tk.Label(
            frame,
            text=label_text,
            font=("Courier", 11),
            fg=self.fg_color,
            bg=self.bg_color
        ).pack(anchor="w")

        entry = tk.Entry(frame, textvariable=var, width=50, font=("Courier", 10))
        entry.pack(side="left", fill="x", expand=True)

        tk.Button(
            frame,
            text="📂",
            command=callback,
            width=5,
            bg=self.button_color,
            fg="black",
            font=("Courier", 10)
        ).pack(side="left", padx=5)

    def select_working_dir(self):
        folder = filedialog.askdirectory()
        if folder:
            self.wrk_dir_var.set(folder)

    def select_destination_dir(self):
        folder = filedialog.askdirectory()
        if folder:
            self.dst_dir_var.set(folder)

    def log(self, message):
        self.log_text.config(state='normal')
        self.log_text.insert(tk.END, f"> {message}\n")
        self.log_text.config(state='disabled')
        self.log_text.see(tk.END)

    def confirm_settings(self):
        wrk_dir = self.wrk_dir_var.get()
        dst_dir = self.dst_dir_var.get()

        if not wrk_dir or not dst_dir:
            messagebox.showwarning("⚠️ Input Error", "Please select both directories.")
            return

        try:
            # Just validate path existence
            PathFinder(wrk_dir, dst_dir)
            self.log(f"✅ Confirmed: \n   Source: {wrk_dir}\n   Target: {dst_dir}")
            self.settings_confirmed = True
            self.run_button.config(state=tk.NORMAL)
        except Exception as e:
            self.log(f"❌ Error confirming settings: {e}")
            messagebox.showerror("Error", str(e))

    def run_organizer(self):
        if not self.settings_confirmed:
            messagebox.showwarning("⚠️ Confirm First", "Click 'OK' to confirm settings before running.")
            return

        wrk_dir = self.wrk_dir_var.get()
        dst_dir = self.dst_dir_var.get()
        choice = self.choice_var.get()
        recursive = self.recursive_var.get()

        try:
            # Step 1: Validate paths
            path_handler = PathFinder(wrk_dir, dst_dir)

            # Step 2: Get file extensions
            selector = FileSelection(choice)

            # Step 3: Organize files
            organizer = FileOrganizer(
                path_handler.get_working_dir(),
                path_handler.get_destination_dir(),
                selector._file_ext_list
            )

            self.log(f"\n⚙️ Organizing files...")
            self.log(f"📁 Source: {wrk_dir}")
            self.log(f"💾 Target: {dst_dir}")
            self.log(f"🧬 Extensions: {', '.join(selector._file_ext_list)}")
            self.log(f"🔁 Recursive mode: {'On' if recursive else 'Off'}\n")

            if recursive:
                organizer.organize_recursive()
                self.log("🎉 Done! All matching files moved (recursive).")
            else:
                organizer.organize()
                self.log("🎉 Done! Files moved.")

        except Exception as e:
            self.log(f"💥 Error: {e}")
            messagebox.showerror("🚨 Error", str(e))

# ────────────────
# Start GUI
# ────────────────

if __name__ == "__main__":
    root = tk.Tk()
    app = FileOrganizerGUI(root)
    root.mainloop()