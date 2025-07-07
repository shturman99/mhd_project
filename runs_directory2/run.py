#!/usr/bin/env python3
"""
run_pencil_stable.py - Script to run Pencil Code simulations with stability enhancements
This script executes the pc_run command in simulation directories with
appropriate stability parameters and can adjust grid size.
"""
import os
import sys
import argparse
import glob
import re
import shutil
import subprocess
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

def print_command(command):
    """Print a command being executed."""
    print(f"{Colors.YELLOW}${Colors.NC} {command}")

def print_warning(message):
    """Print a warning message."""
    print(f"{Colors.YELLOW}⚠{Colors.NC} {message}")

def print_error(message):
    """Print an error message."""
    print(f"{Colors.RED}{message}{Colors.NC}")

def find_simulation_dirs():
    """Find all simulation directories."""
    return [d for d in glob.glob("*/") ]

def is_simulation_built(sim_dir):
    """Check if a simulation has already been built."""
    os.chdir(sim_dir)
    # Look for typical build artifacts - this may need to be adjusted 
    # based on what specific files indicate a successful build in Pencil Code
    built = os.path.exists("Makefile") and os.path.exists("src") and os.path.exists("bin")
    os.chdir("..")
    return built

def is_simulation_started(sim_dir):
    """Check if a simulation has already been started."""
    os.chdir(sim_dir)
    started = os.path.exists("data") and os.path.exists("data/var.dat")
    os.chdir("..")
    return started

def build_simulation(sim_dir, mesh_size=32, rebuild=False, skip_if_built=True):
    """Build a simulation directory."""
    if skip_if_built and is_simulation_built(sim_dir):
        print_status(f"Simulation in {sim_dir} is already built. Skipping build step.")
        return
        
    os.chdir(sim_dir)
    
    # Set the grid size if specified
    file_path = os.path.join("src", "cparam.local")
    
    # Check if the file exists
    if os.path.exists(file_path):
        # First read the file
        with open(file_path, "r") as f:
            lines = f.readlines()
            
        # Then modify and write back
        modified = False
        with open(file_path, "w") as f:
            for line in lines:
                if re.match(r"integer,\s*parameter\s*::\s*nxgrid", line):
                    # Replace the existing line with new mesh size
                    f.write(f"integer, parameter :: nxgrid={mesh_size},nygrid=nxgrid,nzgrid=nxgrid")
                    modified = True
                else:
                    f.write(line)
            
            # Add the line if it wasn't found
            if not modified:
                f.write(f"integer, parameter :: nxgrid={mesh_size},nygrid=nxgrid,nzgrid=nxgrid")
                
        print_status(f"Updated mesh size to {mesh_size} in {file_path}")
    else:
        print_warning(f"File {file_path} not found. Mesh size not updated.")
    # Build the simulation
    if rebuild:
        print_command("pc_build")
        subprocess.run(["pc_build"], check=True)
    else:
        print_command("pc_build -q")
        subprocess.run(["pc_build", "-q"], check=True)
        
    os.chdir("..")
    print_status(f"Simulation in {sim_dir} built successfully.")

def start_simulation(sim_dir, skip_if_started=True):
    """Start a simulation directory."""
    if skip_if_started and is_simulation_started(sim_dir):
        print_status(f"Simulation in {sim_dir} is already started. Skipping start step.")
        return

    os.chdir(sim_dir)
    print_command("pc_start")
    subprocess.run(["pc_start"], check=True)
    os.chdir("..")
    print_status(f"Simulation in {sim_dir} started successfully.")

def run_simulation(sim_dir):
    """Run a simulation directory."""
    os.chdir(sim_dir)
    print_command("pc_run")
    subprocess.run(["pc_run"], check=True)
    os.chdir("..")
    print_status(f"Simulation in {sim_dir} run successfully.")

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Run Pencil Code simulations with stability enhancements")
    parser.add_argument('--rebuild', action='store_true', help='Force rebuild all simulations')
    parser.add_argument('--skip-build', action='store_true', help='Skip building if already built')
    parser.add_argument('--skip-start', action='store_true', help='Skip starting if already started')
    parser.add_argument('--run-only', action='store_true', help='Only run the simulation (skip build and start)')
    parser.add_argument('--dry-run', action='store_true', help='Print commands without executing them')
    parser.add_argument('--dirs', nargs='+', help='Specify simulation directories to process')
    parser.add_argument('--mesh-size', type=int, default=32, help='Set the grid size for the simulation')
    return parser.parse_args()

def main():
    args = parse_arguments()
    
    # Find simulation directories
    if args.dirs:
        sims = args.dirs
    else:
        sims = find_simulation_dirs()
    
    print_section("Simulation Directories")
    print("\n".join(sims))
    
    # Process each simulation
    for sim in sims:
        print_section(f"Processing simulation: {sim}")
        
        if args.run_only:
            # Skip both build and start steps
            print_status(f"Run-only mode selected for {sim}")
            run_simulation(sim)
        else:
            # Build step (if not skipped)
            # Only pass mesh_size if it was specified
            build_kwargs = {
                'rebuild': args.rebuild,
                'skip_if_built': args.skip_build,
                'mesh_size': args.mesh_size
            }
            
                
            build_simulation(sim, **build_kwargs)
            
            # Start step (if not skipped)
            start_simulation(sim, skip_if_started=args.skip_start)
            
            # Run step
            run_simulation(sim)

if __name__ == "__main__":
    sys.exit(main())