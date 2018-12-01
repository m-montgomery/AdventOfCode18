#!/bin/bash
# -----------------------------------------------------------------------------
# AUTHOR: M. Montgomery
# DATE:   01/12/2018
# FILE:   start_day.sh
# -----------------------------------------------------------------------------
# PURPOSE: 
# Creates file for new advent prompt. Writes header template, grants permission,
# and opens the file. Includes variables for editing convenience.
#
# USAGE:
# ./start_day.sh filename  (include extension)
# -----------------------------------------------------------------------------

# VARIABLES               (for script flexibility)
author="M. Montgomery"
editor="emacs"
date=$(date +%m/%d/%Y)    # mm/dd/yyyy format
filename=$1
name=$(echo "$filename" | sed 's/.*\/\([^\/]\)/\1/')   # remove filepath

# CHECK ARGUMENT COUNT
if (( $# < 1 )); then
    echo -e "Error: Not enough arguments." >&2
    echo -e "Usage: ./start_day.sh filename  (include extension)\n" >&2
    exit 1
fi

# CHECK IF NAME AVAILABLE
if [ -f "$filename" ]; then
    echo -e "File $filename already exists in this directory."
    echo -e "Try again with a different name.\n"
    exit 1
    
else
    # CREATE NEW FILE

    # begin header comments
    if [[ "$name" =~ \.py$ ]]; then
	echo '"""' >> $filename
    else
	echo "/*" >> $filename
    fi

    # header comments
    echo -e "AUTHOR: $author \nDATE:   $date" >> $filename
    echo -e "FILE:   $name \n\nPROMPT: " >> $filename

    # end header comments
    if [[ "$name" =~ \.py$ ]]; then
	echo '"""' >> $filename
    else
	echo "*/" >> $filename
    fi

    # init java class
    day=$(echo "$name" | sed 's/\([^\.]*\)\..*/\1/')   # remove ext
    if [[ "$name" =~ \.java$ ]]; then
	echo -e "\npublic class $day {" >> $filename
	echo -e "    public static void main(String[] args) {" >> $filename
	echo -e "    \n    }\n}" >> $filename

    # init c++ skeleton
    elif [[ "$name" =~ \.cc$ ]]; then
	echo -e "\n#include <iostream>\n" >> $filename
	echo -e "int main() {\n  return 0;\n}" >> $filename

    # init Python main
    elif [[ "$name" =~ \.py$ ]]; then
	echo -e "\ndef main():\n    pass\n" >> $filename
	echo -e "if __name__ == \"__main__\":\n    main()" >> $filename
    fi

    # REPORT COMPLETION
    echo "File $filename created."

    # INITIALIZE INPUT FILE
    if [ ! -f "input/$day.txt" ]; then
	echo -n "" >> "input/$day.txt"
	echo "Input file $day.txt created in input/."
    fi

    # OPEN FILE
    $editor $filename &
fi
