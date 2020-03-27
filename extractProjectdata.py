#!python3
# extractProjectdata.py
# ------------------------------------------------------------------------------
# File          extractProjectdata.py
# Date          26-03-2020
# Author        Stefan Niedermayr
# Version       0.0.0
# Python-Ver.   3.8.1
# Description   This script may be used to extract data from project directories
#               of your choice. You can define a source path, from where the 
#               script should look for files from the predefined file extension
#               list. The structure of the directory is kept identical. The 
#               directories including the found files are then backed up in
#               the destination location of your choice.
#
#               The main purpose of this script is to extract important data
#               from Xilinx Vivado Projects to make it easier to version control
#               those files.
#
#               In order to successfully backup a Vivado project, the following
#               file need to be saved:
#
#               (1) Project .xpr file
#               (2) Created .tcl script (from write_project_tcl)
#               (3) Constraint files .xdc
#               (4) Board files .bd
#
# Arguments:
#
#   -help           Lists all possible command options for this script.
#
#   -start          Starts extraction of project data.
#
#
# ------------------------------------------------------------------------------
import sys, os, datetime, shutil
# ------------------------------------------------------------------------------
# GLOBAL VARIABLE DEFINITIONS
# ------------------------------------------------------------------------------
creationTime = datetime.date.today().strftime("%y%y%m%d")
srcPath = "C:\\Xilinx\\"
dstPath = "C:\\Users\\Stefan\\Temp\\"
fileTypes = (".xpr", ".bd", ".tcl", ".vhd", ".v", ".sv", ".xdc")

backupDirName = creationTime + "_XilProj_Backup"

# ------------------------------------------------------------------------------
# FUNCTION DECLARATIONS
# ------------------------------------------------------------------------------
def printHeader():
    print(72*"-")
    print("extractProjectdata.py")
    print(72*"-")

def printHelpMsg():
    print("""This script may be used to extract data from project directories
of your choice. You can define a source path, from where the 
script should look for files from the predefined file extension
list. The structure of the directory is kept identical. The 
directories including the found files are then backed up in
the destination location of your choice.\n\n""")
    # Description of the possible parameters
    print("""-help\t\tLists all possible commands for this script.\n""")
    print("""-start\t\tStarts the extraction process.\n""")
    print(72*"-")

def extractProjectdata():
    pass

# ------------------------------------------------------------------------------
# MAIN ROUTINE
# ------------------------------------------------------------------------------
# Header
printHeader()

# Get number of arguments
argCnt = len(sys.argv)

if argCnt < 2:
    # No arguments
    printHelpMsg()
elif (argCnt < 3) and (sys.argv[1] == "-start" or sys.argv[1] == "start"):
    # 1 argument, either "-start" or "start"
    # Start extraction of data. 
    print("Do smth -> start")
elif (argCnt < 3) or (sys.argv[1] == "-help") or (sys.argv[1] == "help"):
    # 1 argument, either "-help" or "help"
    printHelpMsg()