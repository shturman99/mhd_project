#!/usr/bin/env bash
#
# run_pencil_simulations.sh - Batch runner for Pencil Code simulations
# 
# This script finds all simulation directories in the current directory,
# and executes Pencil Code commands in each one.
#
# Usage: ./run_pencil_simulations.sh [--dry-run]
#   --dry-run: Show what would be executed without actually running commands

# Colors for better readability
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# Function to print section headers
print_section() {
    echo -e "\n${BOLD}${BLUE}==== $1 ====${NC}\n"
}

# Function to print status messages
print_status() {
    echo -e "${GREEN}✓${NC} $1"
}

# Function to print commands being executed
print_command() {
    echo -e "${YELLOW}$${NC} $1"
}

# Check for dry run flag
DRY_RUN=false
if [[ "$1" == "--dry-run" ]]; then
    DRY_RUN=true
    print_status "Running in DRY RUN mode - no actual commands will be executed"
fi

# Find all directories in the current location 
# (excluding hidden directories starting with .)
print_section "Scanning for simulation directories"

# Using find to get only directories, one level deep
SIM_DIRS=$(find . -maxdepth 1 -mindepth 1 -type d -not -path '*/\.*' | sort)
SIM_COUNT=$(echo "$SIM_DIRS" | wc -l)

if [[ -z "$SIM_DIRS" ]]; then
    echo -e "${RED}No simulation directories found!${NC}"
    exit 1
fi

echo -e "Found ${BOLD}$SIM_COUNT${NC} simulation directories:"
for dir in $SIM_DIRS; do
    echo "  - $dir"
done

# Ask for confirmation if not in dry run mode
if [[ "$DRY_RUN" == "false" ]]; then
    echo ""
    read -p "Proceed with running Pencil Code in these directories? (y/n): " CONFIRM
    if [[ "$CONFIRM" != "y" && "$CONFIRM" != "Y" ]]; then
        echo "Aborted."
        exit 0
    fi
fi

# Start processing each directory
print_section "Processing Simulation Directories"

# Save the original directory to return to it later
ORIGINAL_DIR=$(pwd)

for dir in $SIM_DIRS; do
    print_section "Processing $(basename "$dir")"
    
    # Change to the simulation directory
    print_command "cd $dir"
    if [[ "$DRY_RUN" == "false" ]]; then
        cd "$dir" || { echo -e "${RED}Failed to change to directory $dir${NC}"; continue; }
    fi
    
    # Run pc_setupsrc
    print_command "pc_setupsrc"
    if [[ "$DRY_RUN" == "false" ]]; then
        pc_setupsrc
        if [[ $? -ne 0 ]]; then
            echo -e "${RED}pc_setupsrc failed in $dir${NC}"
            cd "$ORIGINAL_DIR"
            continue
        else
            print_status "pc_setupsrc completed successfully"
        fi
    fi
    
    # Run pc_build
    print_command "pc_build -f GNU-GCC_MPI"
    if [[ "$DRY_RUN" == "false" ]]; then
        pc_build -f GNU-GCC_MPI
        if [[ $? -ne 0 ]]; then
            echo -e "${RED}pc_build failed in $dir${NC}"
            cd "$ORIGINAL_DIR"
            continue
        else
            print_status "pc_build completed successfully"
        fi
    fi
    
    # Run pc_start
    print_command "pc_start"
    if [[ "$DRY_RUN" == "false" ]]; then
        pc_start
        if [[ $? -ne 0 ]]; then
            echo -e "${RED}pc_start failed in $dir${NC}"
            cd "$ORIGINAL_DIR"
            continue
        else
            print_status "pc_start completed successfully"
        fi
    fi
    
    # Run pc_run
    print_command "pc_run"
    if [[ "$DRY_RUN" == "false" ]]; then
        pc_run
        if [[ $? -ne 0 ]]; then
            echo -e "${RED}pc_run failed in $dir${NC}"
        else
            print_status "pc_run completed successfully"
        fi
    fi
    
    # Return to the original directory before processing the next one
    if [[ "$DRY_RUN" == "false" ]]; then
        cd "$ORIGINAL_DIR"
    fi
    
    print_status "Finished processing $(basename "$dir")"
    echo ""
done

print_section "Summary"
echo -e "Processed ${BOLD}$SIM_COUNT${NC} simulation directories."
if [[ "$DRY_RUN" == "true" ]]; then
    echo -e "${YELLOW}This was a dry run. No commands were actually executed.${NC}"
    echo -e "Run without the --dry-run flag to execute the commands."
fi

print_section "Done"
