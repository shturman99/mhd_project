#!/usr/bin/env python3
"""
update_pencil_params.py - Script to update parameters in Pencil Code configuration files

This script modifies parameters in Fortran namelist files run.in, start.in
used by Pencil Code simulations. It can update parameters in specific sections
and supports directory-specific parameter changes.

Examples:
  # Update a parameter in all simulation directories
  python update_pencil_params.py --param chiral_mhd_run_pars:gamma5=1e9
  
  # Update parameters in specific directories
  python update_pencil_params.py --dir sim1 --param chiral_mhd_run_pars:gamma5=1e9
  
  # Update multiple parameters
  python update_pencil_params.py --param chiral_mhd_run_pars:gamma5=1e9 run_pars:nt=500
  
  # Specify a different config file (default is run.in)
  python update_pencil_params.py --file start.in --param density_run_pars:idiff=2
"""
import os
import sys
import re
import glob
import argparse
from pathlib import Path

# ANSI color codes for better readability
class Colors:
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[0;33m'
    BLUE = '\033[0;34m'
    BOLD = '\033[1m'
    NC = '\033[0m'  # No Color

def print_section(title):
    """Print a formatted section header."""
    print(f"\n{Colors.BOLD}{Colors.BLUE}==== {title} ===={Colors.NC}\n")

def print_status(message):
    """Print a status message."""
    print(f"{Colors.GREEN}✓{Colors.NC} {message}")

def print_warning(message):
    """Print a warning message."""
    print(f"{Colors.YELLOW}⚠{Colors.NC} {message}")

def print_error(message):
    """Print an error message."""
    print(f"{Colors.RED}✗{Colors.NC} {message}")

def find_simulation_dirs():
    """Find all simulation directories."""
    return [d for d in glob.glob("*/") if os.path.isdir(d)]

def update_parameters(file_path, parameters):
    """
    Update parameters in a Fortran namelist file.
    
    Parameters:
    file_path (str): Path to the configuration file
    parameters (dict): Dictionary of parameters to update, organized by section
                      Example: {'chiral_mhd_run_pars': {'gamma5': '1e9'}}
    
    Returns:
    bool: True if successful, False otherwise
    """
    if not os.path.exists(file_path):
        print_error(f"File not found: {file_path}")
        return False
        
    try:
        # Read the file content
        with open(file_path, "r") as f:
            content = f.read()
            
        original_content = content  # Save for comparison
            
        # Process each section in the parameters dictionary
        for section_name, section_params in parameters.items():
            # Find the section in the file
            section_pattern = r"&" + section_name + r"\s+(.*?)\/"
            section_match = re.search(section_pattern, content, re.DOTALL)
            
            if section_match:
                section_content = section_match.group(1)
                new_section_content = section_content
                
                # Update each parameter in the section
                for param_name, param_value in section_params.items():
                    # Check if parameter already exists in the section
                    param_pattern = r"(\s*" + param_name + r"\s*=\s*[^,\n\/]+)"
                    param_match = re.search(param_pattern, new_section_content)
                    
                    if param_match:
                        # Replace existing parameter
                        old_param = param_match.group(1)
                        new_param = f" {param_name}={param_value}"
                        new_section_content = new_section_content.replace(old_param, new_param)
                        print_status(f"Updated parameter {param_name}={param_value} in section {section_name}")
                    else:
                        # Add new parameter at the end of the section
                        # First strip trailing whitespace
                        new_section_content = new_section_content.rstrip()
                        # Check if the section ends with a comma
                        if new_section_content.rstrip().endswith(','):
                            new_section_content += f" {param_name}={param_value},\n"
                        else:
                            # Add a comma to the last parameter
                            last_param_end = new_section_content.rfind('\n')
                            if last_param_end == -1:
                                # Single line section
                                new_section_content += f", {param_name}={param_value}"
                            else:
                                # Multi-line section, add comma to last line and add new parameter
                                last_line = new_section_content[last_param_end+1:]
                                if '=' in last_line and not last_line.strip().endswith(','):
                                    new_section_content = new_section_content[:last_param_end+1] + last_line.rstrip() + ",\n" + f"  {param_name}={param_value}"
                                else:
                                    new_section_content += f",\n  {param_name}={param_value}"
                        print_status(f"Added parameter {param_name}={param_value} to section {section_name}")
                
                # Replace the old section content with the new one
                content = content.replace(section_match.group(1), new_section_content)
            else:
                # Section not found, add it at the end of the file
                new_section = f"\n&{section_name}\n"
                for param_name, param_value in section_params.items():
                    new_section += f"  {param_name}={param_value},\n"
                new_section += "/\n"
                content += new_section
                print_status(f"Added new section {section_name} with parameter(s) {list(section_params.items())}")
        
        # Check if content was modified
        if content == original_content:
            print_warning(f"No changes made to {file_path}")
            return True
            
        # Write the updated content back to the file
        with open(file_path, "w") as f:
            f.write(content)
            
        print_status(f"Successfully updated {file_path}")
        return True
        
    except Exception as e:
        print_error(f"Error updating parameters in {file_path}: {str(e)}")
        return False

def parse_parameter_arg(param_str):
    """
    Parse a parameter string in the format 'section:name=value'.
    
    Returns:
    tuple: (section, name, value) or None if invalid
    """
    try:
        section_part, param_part = param_str.split(':', 1)
        param_name, param_value = param_part.split('=', 1)
        return (section_part.strip(), param_name.strip(), param_value.strip())
    except ValueError:
        print_error(f"Invalid parameter format: {param_str}. Expected format: 'section:name=value'")
        return None

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Update parameters in Pencil Code configuration files")
    parser.add_argument('--dir', '-d', nargs='+', help='Simulation directories to update (default: all)')
    parser.add_argument('--file', '-f', default='run.in', help='Configuration file to update (default: run.in)')
    parser.add_argument('--param', '-p', nargs='+', required=True, 
                        help='Parameters to update in format section:name=value (e.g., chiral_mhd_run_pars:gamma5=1e9)')
    parser.add_argument('--dry-run', action='store_true', help='Print changes without updating files')
    
    args = parser.parse_args()
    
    # Validate and process parameters
    params_dict = {}
    for param_str in args.param:
        parsed = parse_parameter_arg(param_str)
        if parsed:
            section, name, value = parsed
            if section not in params_dict:
                params_dict[section] = {}
            params_dict[section][name] = value
    
    if not params_dict:
        print_error("No valid parameters provided. Exiting.")
        sys.exit(1)
        
    return args, params_dict

def main():
    """Main function."""
    args, params_dict = parse_arguments()
    
    # Determine which directories to process
    if args.dir:
        sim_dirs = [d for d in args.dir]
        # Ensure directories end with slash
        sim_dirs = [d if d.endswith('/') else d + '/' for d in sim_dirs]
    else:
        sim_dirs = find_simulation_dirs()
    
    if not sim_dirs:
        print_error("No simulation directories found.")
        return 1
        
    print_section("Simulation Directories")
    print("\n".join(sim_dirs))
    
    print_section("Parameters to Update")
    for section, params in params_dict.items():
        print(f"{section}:")
        for name, value in params.items():
            print(f"  {name} = {value}")
    
    if args.dry_run:
        print_warning("Dry run mode - no files will be modified")
        return 0
        
    # Process each directory
    successful = 0
    for sim_dir in sim_dirs:
        file_path = os.path.join(sim_dir, args.file)
        print_section(f"Updating {file_path}")
        
        if update_parameters(file_path, params_dict):
            successful += 1
    
    print_section("Summary")
    print(f"Updated {successful} of {len(sim_dirs)} directories")
    
    return 0 if successful == len(sim_dirs) else 1

if __name__ == "__main__":
    sys.exit(main())