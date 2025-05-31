# config.py

class Config:
    """
    Configuration class containing file categories and their extensions.
    Used by FileSelection to filter file types.
    """

    CHOICE_SELECTION_NO = {
        1: 'pdf',
        2: 'images',
        3: 'audio',
        4: 'video',
        5: 'docs',
        6: 'code'
    }

    FILE_CATEGORIES = {
        'images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'],
        'pdf': ['.pdf'],
        'docs': ['.docx', '.xlsx', '.pptx', '.txt', '.csv', '.xls', '.rtf'],
        'code': ['.py', '.js', '.java', '.cpp', '.html', '.css', '.php', '.rb', '.go'],
        'audio': ['.mp3', '.wav', '.aac', '.flac', '.ogg'],
        'video': ['.mp4', '.mkv', '.avi', '.mov', '.wmv', '.flv']
    }

    __all__ = [FILE_CATEGORIES, CHOICE_SELECTION_NO]