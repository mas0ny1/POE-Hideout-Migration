import json
import os
import argparse
from typing import Dict, List, Tuple

#Changes all objects X and Y coordinates by xRelative, YRelative 
#Credits to https://gist.github.com/CristenPerret/ea3da944c2e976408662b988ee07d9e6

def read_hideout_file(filepath: str) -> List[str]:
    """Read a hideout file and return its lines."""
    with open(filepath, errors="ignore") as f:
        lines = f.readlines()
        return [line.strip('\n') for line in lines]

def extract_language(lines: List[str]) -> str:
    """Extract the language setting from the hideout file."""
    for line in lines[:5]:  # Language is usually in the first few lines
        if '"language":' in line:
            return line.split(':')[1].strip().strip('",')
    return "Unknown"

def find_waypoint_coords(lines: List[str]) -> Tuple[int, int]:
    """Find the waypoint coordinates in a hideout file using hash."""
    WAYPOINT_HASH = "1224707366"
    in_waypoint = False
    x_coord = y_coord = None
    
    for line in lines:
        if f'"hash": {WAYPOINT_HASH}' in line:
            in_waypoint = True
            continue
        if in_waypoint and '"x":' in line:
            x_coord = int(line.split(':')[1].strip().strip(','))
        if in_waypoint and '"y":' in line:
            y_coord = int(line.split(':')[1].strip().strip(','))
            if x_coord is not None:  # Found both coordinates
                return x_coord, y_coord
        if in_waypoint and '}' in line:  # End of waypoint object
            in_waypoint = False
    
    raise ValueError("No waypoint found in hideout file")

def extract_hideout_info(lines: List[str]) -> Dict[str, str]:
    """Extract hideout name and hash from the file."""
    info = {}
    for line in lines[:10]:  # Check first 10 lines
        if '"hideout_name":' in line:
            info['name'] = line.split(':')[1].strip().strip('",')
        elif '"hideout_hash":' in line:
            info['hash'] = line.split(':')[1].strip().strip('",')
        elif '"language":' in line:
            info['language'] = line.split(':')[1].strip().strip('",')
    return info

def update_coordinates(lines: List[str], x_relative: int, y_relative: int) -> List[str]:
    """Update coordinates using the same logic as move.py"""
    output_file = []
    for line in lines:
        if '"x":' in line:
            coord = int(line.split(':')[1].rstrip(','))
            coord += x_relative
            line = '      "x": ' + str(coord) + ","
            output_file.append(line +'\n')
        elif '"y":' in line:
            coord = int(line.split(':')[1].rstrip(','))
            coord += y_relative
            line = '      "y": ' + str(coord) + ","
            output_file.append(line + '\n') 
        else:
            output_file.append(line + '\n')
    return output_file

def migrate_hideout(source_path: str, target_path: str, x_relative: int = None, y_relative: int = None, output_path: str = None):
    """
    Migrate a hideout design from one type to another using move.py's logic.
    If x_relative and y_relative are not provided, they will be calculated based on waypoint positions.
    """
    # Read both hideout files
    source_lines = read_hideout_file(source_path)
    target_lines = read_hideout_file(target_path)
    
    # Check languages match
    source_lang = extract_language(source_lines)
    target_lang = extract_language(target_lines)
    
    if source_lang != target_lang:
        raise ValueError(
            f"Language mismatch: Source hideout is in {source_lang}, "
            f"but target hideout is in {target_lang}. "
            "Please use hideout files with matching languages. \nThe easiest way to match the languages is by importing the downloaded hideout into your game, and exporting it without any changes, this will set the hideout file's language to your in game language (which I'm assuming to be english). Once you have done this, change the source hideout to the newly exported hideout file"
        )
    
    # If no offsets provided, calculate them based on waypoint positions
    if x_relative is None or y_relative is None:
        try:
            source_x, source_y = find_waypoint_coords(source_lines)
            target_x, target_y = find_waypoint_coords(target_lines)
            
            # Calculate the difference in positions
            x_relative = target_x - source_x if x_relative is None else x_relative
            y_relative = target_y - source_y if y_relative is None else y_relative
            
            print(f"Automatically calculated offsets based on waypoint positions:")
            print(f"X offset: {x_relative} (target: {target_x} - source: {source_x})")
            print(f"Y offset: {y_relative} (target: {target_y} - source: {source_y})")
        except ValueError as e:
            print(f"Warning: Could not automatically calculate offsets: {str(e)}")
            x_relative = x_relative if x_relative is not None else 0
            y_relative = y_relative if y_relative is not None else 0
    
    # Get the first 5 lines from target (contains hideout info)
    target_header = target_lines[:5]
    
    # Combine target header with source content
    output_lines = target_header + source_lines[5:]
    
    # Update coordinates
    final_lines = update_coordinates(output_lines, x_relative, y_relative)
    
    # Write the result using the same approach as move.py
    with open(output_path, 'w+', errors="ignore") as f:
        f.writelines(final_lines)
        
    return x_relative, y_relative  # Return the offsets used

def main():
    parser = argparse.ArgumentParser(description='Migrate POE hideout designs between different hideout types')
    parser.add_argument('source', help='Source hideout file (from hideoutshowcase.com)')
    parser.add_argument('target', help='Target hideout file (exported from game)')
    parser.add_argument('--x', type=int, default=0, help='X-axis offset (default: 0)')
    parser.add_argument('--y', type=int, default=0, help='Y-axis offset (default: 0)')
    parser.add_argument('-o', '--output', help='Output file path (default: migrated_hideout.hideout)',
                      default='migrated_hideout.hideout')
    
    args = parser.parse_args()
    
    try:
        migrate_hideout(args.source, args.target, args.x, args.y, args.output)
        print(f"Hideout successfully migrated to {args.output}")
        print(f"Applied offsets: X={args.x}, Y={args.y}")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()