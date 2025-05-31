# tests/test_operations.py

import unittest
from pathlib import Path
import os
import shutil

# Import your classes
from operations.path_checker import PathFinder
from operations.file_selection import FileSelection
from operations.file_organiser import FileOrganizer


class TestFileSelection(unittest.TestCase):
    def test_valid_choice(self):
        selector = FileSelection("2")
        self.assertEqual(selector.choice_selection, 2)
        self.assertIsInstance(selector._file_ext_list, set)

    def test_invalid_choice_out_of_range(self):
        with self.assertRaises(ValueError):
            FileSelection("7")

    def test_invalid_choice_not_a_number(self):
        with self.assertRaises(ValueError):
            FileSelection("abc")

    def test_get_list_returns_set(self):
        selector = FileSelection("3")
        self.assertTrue(isinstance(selector.get_list(), set))


class TestPathFinder(unittest.TestCase):
    def setUp(self):
        # Create dummy directories
        self.test_dir = Path("test_working_dir")
        self.test_dir.mkdir(exist_ok=True)

        self.test_dst = Path("test_destination_dir")

    def tearDown(self):
        # Clean up
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)
        if self.test_dst.exists():
            shutil.rmtree(self.test_dst)

    def test_valid_working_dir(self):
        pf = PathFinder(str(self.test_dir), None)
        self.assertEqual(pf.get_working_dir(), str(self.test_dir.resolve()))

    def test_invalid_working_dir(self):
        with self.assertRaises(ValueError):
            PathFinder("invalid_path", None)

    def test_create_destination_dir(self):
        with unittest.mock.patch('builtins.input', return_value='y'):
            pf = PathFinder(str(self.test_dir), str(self.test_dst))
            pf.destination_dir = str(self.test_dst)  # trigger setter
            self.assertTrue(self.test_dst.exists())

    def test_skip_create_destination(self):
        with unittest.mock.patch('builtins.input', return_value='n'):
            pf = PathFinder(str(self.test_dir), "non_existing_dir")
            pf.destination_dir = "non_existing_dir"  # trigger setter
            self.assertIsNone(pf.get_destination_dir())


class TestFileOrganizer(unittest.TestCase):
    def setUp(self):
        self.wrk_dir = "test_files"
        self.dst_dir = "test_output"
        self.ext_list = [".txt"]

        # Setup dummy directory structure
        os.makedirs(self.wrk_dir, exist_ok=True)
        with open(f"{self.wrk_dir}/test.txt", "w") as f:
            f.write("Test content")
        with open(f"{self.wrk_dir}/test.jpg", "w") as f:
            f.write("Test image")

    def tearDown(self):
        if os.path.exists(self.wrk_dir):
            shutil.rmtree(self.wrk_dir)
        if os.path.exists(self.dst_dir):
            shutil.rmtree(self.dst_dir)

    def test_filter_txt_file(self):
        organizer = FileOrganizer(self.wrk_dir, self.dst_dir, self.ext_list)
        matched = []
        for file_path in Path(organizer.working_dirpath).iterdir():
            if file_path.is_file() and any(file_path.name.lower().endswith(ext) for ext in organizer.file_extension):
                matched.append(file_path)
        self.assertEqual(len(matched), 1)
        self.assertTrue("test.txt" in str(matched[0]))

    def test_no_match_for_jpg(self):
        organizer = FileOrganizer(self.wrk_dir, self.dst_dir, [".pdf"])
        matched = []
        for file_path in Path(organizer.working_dirpath).iterdir():
            if file_path.is_file() and any(file_path.name.lower().endswith(ext) for ext in organizer.file_extension):
                matched.append(file_path)
        self.assertEqual(len(matched), 0)


if __name__ == "__main__":
    unittest.main()