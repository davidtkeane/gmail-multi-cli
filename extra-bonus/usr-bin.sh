#!/bin/bash

# Created by Ranger
# This script will enable you to run todoist from the command line anywhere inside the terminal. 
# This script copies, chmods, and moves a specified Python script to /usr/local/bin/
# To Run this script $ bash usr-bin.sh


# File and destination details
source_file="gmail_multi_usr_bin.py"
destination="/usr/local/bin/gmail"

# Check if the source file exists
if [ ! -f "$source_file" ]; then
    echo "Error: Source file $source_file does not exist."
    exit 1
fi

# Copy the file to /usr/local/bin with sudo
sudo cp "$source_file" "$destination"

# Check if the copy was successful
if [ $? -ne 0 ]; then
    echo "Error: Failed to copy $source_file to $destination."
    exit 1
fi

# Make the copied file executable
sudo chmod +x "$destination"

# Check if chmod was successful
if [ $? -ne 0 ]; then
    echo "Error: Failed to chmod $destination."
    exit 1
fi

echo "Successfully copied and made $destination executable."

# Sleep for 5 seconds
sleep 5

# Refresh the bash profile

# shellcheck source=/dev/null
source ~/.zshrc
# shellcheck source=/dev/null
source ~/.bashrc 