# path_checker.py

import os
from pathlib import Path


class PathFinder:
    @classmethod
    def show_current_dir(cls):
        """Return the current working directory."""
        return os.getcwd()

    def __init__(self, working_dir, destination_dir):
        """
        Initialize with working and destination directories.
        
        Args:
            working_dir (str): Source directory path
            destination_dir (str): Destination directory path
        """
        self._working_dir = None
        self._destination_dir = None

        self.working_dir = working_dir
        self.destination_dir = destination_dir

    @property
    def working_dir(self):
        """Return validated working directory path."""
        return self._working_dir

    @working_dir.setter
    def working_dir(self, wrk_dir_path):
        """
        Validate and set the working directory path.
        
        Args:
            wrk_dir_path (str): Path to validate and assign
        """
        path = Path(wrk_dir_path)
        if not path.is_dir():
            raise ValueError(f"The defined path '{wrk_dir_path}' does not exist")
        self._working_dir = str(path.resolve())

    @property
    def destination_dir(self):
        """Return validated destination directory path."""
        return self._destination_dir

    @destination_dir.setter
    def destination_dir(self, dst_dir):
        """
        Validate and set the destination directory path.
        If path doesn't exist, ask user whether to create it.
        
        Args:
            dst_dir (str): Path to validate or create
        """
        path = Path(dst_dir)
        if not path.is_dir():
            usr_input = input("Path does not exist.\nAre you willing to create a folder? (Y/n): ")
            if usr_input.lower() in ['y', 'yes']:
                try:
                    path.mkdir(parents=True, exist_ok=True)
                    self._destination_dir = str(path.resolve())
                except Exception as e:
                    raise RuntimeError(f"Could not create directory: {e}")
            else:
                print("No folder created. Destination set to None.")
                self._destination_dir = None
        else:
            self._destination_dir = str(path.resolve())

    def get_working_dir(self):
        """Return the validated working directory."""
        return self._working_dir

    def get_destination_dir(self):
        """Return the validated or created destination directory."""
        return self._destination_dir