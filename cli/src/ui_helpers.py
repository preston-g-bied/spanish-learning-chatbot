"""
Spanish Learning Chatbot - UI Helpers
This module provides functions for improving the user interface
"""

import os
import platform
import time

# Try to import colorama for colored text
try:
    from colorama import init, Fore, Back, Style
    colorama_available = True
    init()  # Initialize colorama
except ImportError:
    colorama_available = False

def clear_screen():
    """Clear the terminal screen based on OS"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header(text, width=60):
    """
    Print a centered header with decorative borders
    
    Args:
        text (str): Header text
        width (int, optional): Width of the header
    """
    if colorama_available:
        print(Fore.YELLOW + "=" * width + Style.RESET_ALL)
        print(Fore.YELLOW + text.center(width) + Style.RESET_ALL)
        print(Fore.YELLOW + "=" * width + Style.RESET_ALL)
    else:
        print("=" * width)
        print(text.center(width))
        print("=" * width)

def print_section(text, width=60):
    """
    Print a section header
    
    Args:
        text (str): Section text
        width (int, optional): Width of the section
    """
    if colorama_available:
        print(Fore.CYAN + "\n" + text + Style.RESET_ALL)
        print(Fore.CYAN + "-" * len(text) + Style.RESET_ALL)
    else:
        print("\n" + text)
        print("-" * len(text))

def print_success(text):
    """
    Print a success message
    
    Args:
        text (str): Success message
    """
    if colorama_available:
        print(Fore.GREEN + text + Style.RESET_ALL)
    else:
        print(text)

def print_error(text):
    """
    Print an error message
    
    Args:
        text (str): Error message
    """
    if colorama_available:
        print(Fore.RED + text + Style.RESET_ALL)
    else:
        print(text)

def print_warning(text):
    """
    Print a warning message
    
    Args:
        text (str): Warning message
    """
    if colorama_available:
        print(Fore.YELLOW + text + Style.RESET_ALL)
    else:
        print(text)

def print_info(text):
    """
    Print an info message
    
    Args:
        text (str): Info message
    """
    if colorama_available:
        print(Fore.CYAN + text + Style.RESET_ALL)
    else:
        print(text)

def print_highlight(text):
    """
    Print highlighted text
    
    Args:
        text (str): Text to highlight
    """
    if colorama_available:
        print(Fore.MAGENTA + text + Style.RESET_ALL)
    else:
        print(text)

def print_spanish(text):
    """
    Print Spanish text with special formatting
    
    Args:
        text (str): Spanish text
    """
    if colorama_available:
        print(Fore.YELLOW + "🇪🇸 " + text + Style.RESET_ALL)
    else:
        print("🇪🇸 " + text)

def print_english(text):
    """
    Print English text with special formatting
    
    Args:
        text (str): English text
    """
    if colorama_available:
        print(Fore.WHITE + "🇺🇸 " + text + Style.RESET_ALL)
    else:
        print("🇺🇸 " + text)

def print_menu_option(number, text):
    """
    Print a menu option
    
    Args:
        number (int): Option number
        text (str): Option text
    """
    if colorama_available:
        print(Fore.CYAN + str(number) + ". " + Style.RESET_ALL + text)
    else:
        print(f"{number}. {text}")

def print_progress(current, total, prefix='Progress:', suffix='Complete', length=50):
    """
    Print a progress bar
    
    Args:
        current (int): Current progress
        total (int): Total items
        prefix (str, optional): Prefix text
        suffix (str, optional): Suffix text
        length (int, optional): Progress bar length
    """
    percent = int(100 * (current / float(total)))
    filled_length = int(length * current // total)
    bar = '█' * filled_length + '░' * (length - filled_length)
    
    if colorama_available:
        progress_text = f"\r{prefix} |{Fore.GREEN}{bar}{Style.RESET_ALL}| {percent}% {suffix}"
    else:
        progress_text = f"\r{prefix} |{bar}| {percent}% {suffix}"
    
    print(progress_text, end='\r')
    
    # Print new line on complete
    if current == total:
        print()

def animate_text(text, delay=0.03):
    """
    Animate text by printing one character at a time
    
    Args:
        text (str): Text to animate
        delay (float, optional): Delay between characters
    """
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

def display_mastery(level, max_level=5):
    """
    Display mastery level with stars
    
    Args:
        level (int): Current mastery level
        max_level (int, optional): Maximum mastery level
        
    Returns:
        str: String representation of mastery level
    """
    if colorama_available:
        filled = Fore.YELLOW + "★" * level + Style.RESET_ALL
        empty = "☆" * (max_level - level)
    else:
        filled = "★" * level
        empty = "☆" * (max_level - level)
    
    return filled + empty

def get_terminal_size():
    """
    Get the terminal size
    
    Returns:
        tuple: (width, height) of terminal
    """
    try:
        from shutil import get_terminal_size
        columns, lines = get_terminal_size()
        return columns, lines
    except:
        return 80, 24  # Default size

def centered_box(text, width=None, padding=2):
    """
    Create a centered box around text
    
    Args:
        text (str): Text to put in box
        width (int, optional): Width of box, defaults to terminal width
        padding (int, optional): Padding inside box
        
    Returns:
        str: Box with text
    """
    if width is None:
        width, _ = get_terminal_size()
        width = min(width, 80)  # Limit width to 80 chars
    
    lines = text.split('\n')
    max_line_length = max(len(line) for line in lines)
    box_width = min(width, max_line_length + padding * 2)
    
    horizontal_border = "+" + "-" * (box_width - 2) + "+"
    empty_line = "|" + " " * (box_width - 2) + "|"
    
    result = [horizontal_border]
    result.append(empty_line)
    
    for line in lines:
        padding_left = (box_width - 2 - len(line)) // 2
        padding_right = box_width - 2 - len(line) - padding_left
        result.append("|" + " " * padding_left + line + " " * padding_right + "|")
    
    result.append(empty_line)
    result.append(horizontal_border)
    
    return "\n".join(result)

def play_sound(sound_type="success"):
    """
    Play a sound effect if platform supports it
    
    Args:
        sound_type (str, optional): Type of sound to play
    """
    if platform.system() == "Windows":
        try:
            import winsound
            if sound_type == "success":
                winsound.Beep(1000, 100)
                winsound.Beep(1500, 100)
            elif sound_type == "error":
                winsound.Beep(500, 300)
            elif sound_type == "warning":
                winsound.Beep(750, 200)
        except:
            pass  # Silently fail if winsound not available