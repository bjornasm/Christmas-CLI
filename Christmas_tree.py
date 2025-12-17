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
    print("\033[?25l", end="")  # Move cursor to home (0,0)


def draw_background(
    snow: bool, terminal_width: int, max_width: int, snow_probability=0.05
):
    length = max(0, (terminal_width - max_width) // 2)
    snow_symbols = ["*", "+", ".", "o", "•"]  # different snow symbols
    symbol_weights = [5, 2, 3, 1, 1]
    return (
        " "
        + "".join(
            random.choices(snow_symbols, weights=symbol_weights)[0]
            if (random.random() < snow_probability and snow)
            else " "
            for _ in range(length - 2)
        )
        + " "
    )


def create_tree(height):
    tree = []
    ornament_probability = 0.2
    for i in range(height):
        ornament_positions = []
        if i == 0:
            width = 1
        else:
            width = 1 + i * 2
            center = width // 2
            num_ornaments = max(1, int(width * ornament_probability))
            spacing = width // num_ornaments
            stagger = 1
            if i > 3:
                stagger = int(ornament_probability * 10)
            start = center
            spacing = (width - 1) // (num_ornaments + 1)
            if num_ornaments > 0:
                if i % 2 == 0:
                    start = start + stagger
                ornament_positions = list(range(start, width - 1, spacing))
                ornament_positions += list(range(start, 0, -spacing))
        tree.append((width, ornament_positions))

    return tree


def draw_tree(tree, blink_state, star_bright):
    """Draw the Christmas tree with ornaments and star"""

    # Get terminal width for centering
    try:
        terminal_width = shutil.get_terminal_size().columns
        terminal_height = shutil.get_terminal_size().lines
    except:
        terminal_width = 80  # Default if can't detect
        terminal_height = 80

    # Tree structure - each row has width and ornament positions

    trunk_rows = 2
    trunk_width = 1

    output = []

    # Calculate tree width for centering
    max_width = max(row[0] for row in tree)

    # Extra padding to center the entire tree in the terminal
    star_color = Colors.YELLOW + Colors.BOLD if star_bright else Colors.YELLOW
    star = star_color + "★" + Colors.RESET
    padding = " " * ((max_width - 1) // 2)
    output.append(padding + star)

    # Ornament colors to cycle through
    ornament_colors = [
        Colors.RED,
        Colors.BLUE,
        Colors.MAGENTA,
        Colors.CYAN,
        Colors.YELLOW,
    ]

    # Draw tree body
    for row_num, (width, ornament_positions) in enumerate(tree[1:], 1):
        padding = " " * ((max_width - width) // 2)
        row = []

        for i in range(width):
            if i in ornament_positions:
                # Ornament - blink effect
                if random.random() > 0.3:  # 70% chance to light up when blinking
                    color = random.choice(ornament_colors)
                    row.append(color + "●" + Colors.RESET)
                else:
                    row.append(Colors.GREEN + "●" + Colors.RESET)
            else:
                # Regular tree foliage
                row.append(Colors.GREEN + "*" + Colors.RESET)

        output.append(padding + "".join(row))

    # Trunk
    trunk_padding = " " * ((max_width - trunk_width) // 2)
    for _ in range(trunk_rows):
        output.append(trunk_padding + Colors.YELLOW + "█" * trunk_width + Colors.RESET)

    return (output, max_width, terminal_width, terminal_height)


def animate_tree(tree, duration=30, fps=4):
    """
    Animate the Christmas tree with padding and background

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
            blink_state = (frame // 5) % 2 == 0  # Toggle every 2 frames

            # Star pulse effect (slower than ornaments)
            star_bright = (frame // 4) % 2 == 0  # Toggle every 4 frames

            if blink_state or frame == 0:
                tree_drawing, max_width, terminal_width, terminal_height = draw_tree(
                    tree, blink_state, star_bright
                )

            # Add background and padding to each line
            drawing = []
            horison_size = int(0.8 * (terminal_height - (len(tree_drawing))))
            for i in range(0, horison_size):
                drawing.append(
                    draw_background(True, terminal_width, 0)
                    + draw_background(True, terminal_width, 0)
                )
            for i, line in enumerate(tree_drawing):
                # Determine if this line should have snow
                background = draw_background(True, terminal_width, max_width)
                drawing.append(background + line + background)

            # Add festive message with centering and background
            message_text = "Merry Christmas!"
            message_padding = " " * ((max_width - len(message_text)) // 2)
            background = draw_background(False, terminal_width, max_width)
            message = [
                background
                + message_padding
                + Colors.BOLD
                + Colors.RED
                + message_text
                + Colors.RESET
                + background
            ]

            print("\n".join(drawing + message))

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

    kwargs["tree"] = create_tree(17)
    clear_screen()

    animate_tree(**kwargs)


if __name__ == "__main__":
    main()
