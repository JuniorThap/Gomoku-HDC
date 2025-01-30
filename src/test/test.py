import curses
import signal

def main(stdscr):
    # Clear the screen
    stdscr.clear()

    # Get the screen's height and width
    height, width = stdscr.getmaxyx()

    # Add text to the last line
    stdscr.addstr(height - 1, 0, "This is on the last line!")

    # Refresh to show text
    stdscr.refresh()

    # Handle Ctrl + C
    signal.signal(signal.SIGINT, signal.SIG_DFL)  # Default handling of Ctrl + C (no cleanup)

    # Wait for a key press or interruption
    try:
        stdscr.getkey()
    except KeyboardInterrupt:
        # When Ctrl + C is pressed, do not clear the screen
        pass

# Initialize curses and start the program
curses.wrapper(main)
