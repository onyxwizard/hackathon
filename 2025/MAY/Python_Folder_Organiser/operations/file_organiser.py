# file_organiser.py

from pathlib import Path
import shutil,os


class FileOrganizer:
    def __init__(self, wrk_dir=None, dst_dir=None, file_ext_list=None):
        """
        Initialize the FileOrganizer with working directory, destination directory,
        and list of file extensions to organize.
        
        Args:
            wrk_dir (str): Path to source directory
            dst_dir (str): Path to destination directory
            file_ext_list (list): List of file extensions to match
        """
        self.working_dirpath = Path(wrk_dir)
        self.destination_dirpath = Path(dst_dir)
        self.file_extension = file_ext_list

    def organize(self):
        """
        Move files in the current working directory (non-recursive).
        Only files matching the given extensions are moved.
        """
        moved_count = 0

        for file_path in self.working_dirpath.iterdir():
            if file_path.is_file() and any(
                file_path.name.lower().endswith(ext) for ext in self.file_extension
            ):
                dest_path = self.destination_dirpath / file_path.name
                try:
                    shutil.move(str(file_path), str(dest_path))
                    print(f"Moved: {file_path.name}")
                    moved_count += 1
                except Exception as e:
                    print(f"Error moving {file_path.name}: {e}")

        print(f"\n✅ Done! Moved {moved_count} file(s).")

    def organize_recursive(self):
        """
        Move files from all subdirectories recursively.
        Only files matching the given extensions are moved.
        """
        moved_count = 0

        for root, dirs, files in os.walk(self.working_dirpath):
            for file_name in files:
                file_path = Path(root) / file_name
                if any(file_name.lower().endswith(ext) for ext in self.file_extension):
                    dest_path = self.destination_dirpath / file_name
                    try:
                        shutil.move(str(file_path), str(dest_path))
                        print(f"Moved: {file_name}")
                        moved_count += 1
                    except Exception as e:
                        print(f"Error moving {file_name}: {e}")

        print(f"\n✅ Done! Moved {moved_count} file(s).")