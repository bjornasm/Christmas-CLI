#!/usr/bin/env python3
"""
Terminal Christmas Tree Animation - Version A (Classic Blinking)
Features: Blinking ornaments, pulsing star, colored decorations
"""

import time
import random
import os
import shutil  # For getting terminal size
import argparse


# ANSI Color codes
class Colors:
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"
    BOLD = "\033[1m"
    RESET = "\033[0m"


def setup_parser():
    parser = argparse.ArgumentParser(description="Animated Christmas tree")
    parser.add_argument(
        "-d",
        "--duration",
        help="How long to run animation (seconds). Default 30.",
        required=False,
    )
    parser.add_argument(
        "--fps",
        help="Frames per second (higher = smoother but more CPU). Default 4.",
        required=False,
    )
    return parser


def clear_screen():
    """Clear the terminal screen"""
    os.system("clear" if os.name == "posix" else "cls")


def draw_tree(blink_state, star_bright):
    """Draw the Christmas tree with ornaments and star"""

    # Get terminal width for centering
    try:
        terminal_width = shutil.get_terminal_size().columns
    except:
        terminal_width = 80  # Default if can't detect

    # Tree structure - each row has width and ornament positions
    tree_rows = [
        # (width, [ornament positions])
        (1, []),  # Star
        (3, [1]),  # Top tier
        (5, [1, 3]),
        (7, [2, 5]),  # Middle tier
        (9, [1, 4, 7]),
        (11, [2, 5, 8]),
        (13, [1, 6, 11]),  # Bottom tier
        (15, [3, 7, 12]),
        (17, [2, 8, 14]),
    ]

    trunk_rows = 2
    trunk_width = 1

    output = []

    # Calculate tree width for centering
    max_width = max(row[0] for row in tree_rows)

    # Extra padding to center the entire tree in the terminal
    left_margin = " " * max(0, (terminal_width - max_width) // 2)

    # Star
    star_color = Colors.YELLOW + Colors.BOLD if star_bright else Colors.YELLOW
    star = star_color + "★" + Colors.RESET
    padding = " " * ((max_width - 1) // 2)
    output.append(left_margin + padding + star)

    # Ornament colors to cycle through
    ornament_colors = [
        Colors.RED,
        Colors.BLUE,
        Colors.MAGENTA,
        Colors.CYAN,
        Colors.YELLOW,
    ]

    # Draw tree body
    for row_num, (width, ornament_positions) in enumerate(tree_rows[1:], 1):
        padding = " " * ((max_width - width) // 2)
        row = []

        for i in range(width):
            if i in ornament_positions:
                # Ornament - blink effect
                if (
                    blink_state and random.random() > 0.3
                ):  # 70% chance to light up when blinking
                    color = random.choice(ornament_colors)
                    row.append(color + "●" + Colors.RESET)
                else:
                    row.append(Colors.GREEN + "●" + Colors.RESET)
            else:
                # Regular tree foliage
                row.append(Colors.GREEN + "*" + Colors.RESET)

        output.append(left_margin + padding + "".join(row))

    # Trunk
    trunk_padding = " " * ((max_width - trunk_width) // 2)
    for _ in range(trunk_rows):
        output.append(
            left_margin
            + trunk_padding
            + Colors.YELLOW
            + "█" * trunk_width
            + Colors.RESET
        )

    # Add festive message
    output.append("")
    message = "Merry Christmas!"
    msg_padding = " " * ((max_width - len(message)) // 2)
    output.append(
        left_margin + msg_padding + Colors.BOLD + Colors.RED + message + Colors.RESET
    )

    return "\n".join(output)


def animate_tree(duration=30, fps=4):
    """
    Animate the Christmas tree

    Args:
        duration: How long to run animation (seconds)
        fps: Frames per second (higher = smoother but more CPU)
    """
    frame_delay = 1.0 / fps
    frames = int(duration * fps)

    try:
        for frame in range(frames):
            clear_screen()

            # Blink state changes every few frames
            blink_state = (frame // 2) % 2 == 0  # Toggle every 2 frames

            # Star pulse effect (slower than ornaments)
            star_bright = (frame // 4) % 2 == 0  # Toggle every 4 frames

            tree = draw_tree(blink_state, star_bright)
            print(tree)

            # Show frame counter (optional - remove for final video)
            print(f"\nFrame: {frame + 1}/{frames} | Press Ctrl+C to stop")

            time.sleep(frame_delay)

    except KeyboardInterrupt:
        clear_screen()
        print("\n🎄 Thanks for watching! Happy Holidays! 🎄\n")


def main():
    """Main function"""
    parser = setup_parser()
    args = vars(parser.parse_args())

    kwargs = {}

    if args.get("duration") is not None:
        kwargs["duration"] = int(args["duration"])

    if args.get("fps") is not None:
        kwargs["fps"] = int(args["fps"])

    clear_screen()
    print("Starting Christmas Tree Animation...")
    print("Press Ctrl+C to stop\n")
    time.sleep(2)

    # Run animation for 30 seconds at 4 FPS
    animate_tree(**kwargs)


if __name__ == "__main__":
    main()
