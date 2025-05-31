# main.py - Cyberpunk CLI Version

from pathlib import Path
from operations import PathFinder, FileSelection, FileOrganizer
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

def show_banner():
    """Prints a stylized banner in cyberpunk style."""
    cyber_banner = r"""
     ██████╗ ███╗   ██╗██╗   ██╗██╗  ██╗
    ██╔═══██╗████╗  ██║╚██╗ ██╔╝╚██╗██╔╝
    ██║   ██║██╔██╗ ██║ ╚████╔╝  ╚███╔╝ 
    ██║   ██║██║╚██╗██║  ╚██╔╝   ██╔██╗ 
    ╚██████╔╝██║ ╚████║   ██║   ██╔╝ ██╗
     ╚═════╝ ╚═╝  ╚═══╝   ╚═╝   ╚═╝  ╚═╝
     Welcome to the File Organizer 💻📁
    """
    print(Fore.RED + cyber_banner + Style.RESET_ALL)

def show_file_types():
    """Displays available file categories to user."""
    cyber_print("Select File Type:\n", Fore.YELLOW)
    file_types = {
        1: "PDF",
        2: "Images",
        3: "Audio",
        4: "Video",
        5: "Docs",
        6: "Code"
    }
    for key, name in file_types.items():
        cyber_print(f"[{key}] {name}", Fore.GREEN)
    print()

def cyber_print(text, color=Fore.CYAN):
    """Helper function to print styled text."""
    print(color + text + Style.RESET_ALL)


def main():
    """
    Main function to organize files based on user input.
    
    1. Gets working and destination directories from user
    2. Validates paths using PathFinder
    3. Gets file type selection from user
    4. Organizes files (optionally including subfolders)
    """
    try:
        show_banner()

        # Get working & destination dirs
        cyber_print("📁 Enter working directory: ", Fore.BLUE)
        wrk_dir = input(Fore.CYAN + " ➤ " + Style.RESET_ALL).strip()

        cyber_print("💾 Enter destination directory (optional):", Fore.BLUE)
        dst_dir = input(Fore.CYAN + " ➤ " + Style.RESET_ALL).strip() or None

        path_handler = PathFinder(wrk_dir, dst_dir)

        # Select file type
        show_file_types()
        cyber_print("🔢 Enter choice selection (1-6):", Fore.YELLOW)
        choice = input(Fore.CYAN + " ➤ " + Style.RESET_ALL).strip()

        selector = FileSelection(choice)

        # Ask if user wants to include subfolders
        cyber_print("\n🔁 Include subfolders? (y/n):", Fore.MAGENTA)
        recursive = input(Fore.CYAN + " ➤ " + Style.RESET_ALL).strip().lower()
        use_recursive = recursive == 'y'

        # Organize files
        cyber_print("\n⚙️ Starting file organization...", Fore.CYAN)

        organizer = FileOrganizer(
            path_handler.get_working_dir(),
            path_handler.get_destination_dir(),
            selector._file_ext_list
        )
        if use_recursive:
            organizer.organize_recursive()
        else:
            organizer.organize()

    except Exception as e:
        cyber_print(f"\n❌ Error: {e}", Fore.RED)


if __name__ == "__main__":
    main()