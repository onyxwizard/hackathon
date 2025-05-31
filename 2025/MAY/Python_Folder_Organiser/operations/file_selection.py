# file_selection.py

from operations.config import Config


class FileSelection:
    def __init__(self, choice_selection):
        """
        Initialize with a file category selection.
        
        Args:
            choice_selection (str): User input for file category (1–6)
        """
        self._choice_selection = None
        self._file_ext_list = None
        if choice_selection is not None:
            self.choice_selection = choice_selection

    @property
    def choice_selection(self):
        """Return the selected file category number."""
        return self._choice_selection

    @choice_selection.setter
    def choice_selection(self, user_input):
        """
        Validate and set the file category based on user input.
        
        Args:
            user_input (str): Raw user input (should be int in string form)
        """
        try:
            val = int(user_input)
            if val not in range(1, 7):
                raise ValueError(f"Invalid selection: '{val}'. Must be between 1 and 6.")

            key = Config.CHOICE_SELECTION_NO[val]
            self._file_ext_list = set(Config.FILE_CATEGORIES[key])
            self._choice_selection = val
        except ValueError as ve:
            raise ValueError(f"Invalid input: '{user_input}' is not a valid number.") from ve
        except KeyError as ke:
            raise KeyError(f"Missing key in config: {ke}") from ke

    def get_list(self):
        """Return the list of extensions associated with the selected category."""
        return self._file_ext_list