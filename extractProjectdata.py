#!python3
# extractProjectdata.py
# ------------------------------------------------------------------------------
# File          extractProjectdata.py
# Date          26-03-2020
# Author        Stefan Niedermayr
# Version       1.0.0
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
srcPath = "C:\\Xilinx\\vivprj\\ARTY_A7_Sys01"
dstPath = "C:\\Users\\Stefan\\Temp\\"
fileTypes = (".xpr", ".bd", ".tcl", ".vhd", ".v", ".sv", ".xdc", ".xci")

# String that a folder inside srcPath must contain, that will also be searched
# for files and further subdirectories. Rest will be ignored.
srcPathSubdirContains = ".srcs"

# Backup directory name
creationTime = datetime.date.today().strftime("%y%y%m%d")
backupDirName = creationTime + "_XilProj_Backup"
backupPath = ""


# ------------------------------------------------------------------------------
# FUNCTION DECLARATIONS
# ------------------------------------------------------------------------------
## printLine()
#  Function to print a line in the console at a constant length.
def printLine():
    print(72 * "-")
# END printLine

## printHeader()
#  Function to print header of script.
def printHeader():
    printLine()
    print("extractProjectdata.py")
    printLine()
# END printHeader

## printHelpMsg()
#  Function to print help message when the script is called with a help argument
#  or without any arguments.
def printHelpMsg():
    print("This script may be used to extract data from project directories " +
          "of your\nchoice. You can define a source path, from where the " + 
          "script should look\nfor files from the predefined file extension " +
          "list. The structure of the\ndirectory is kept identical. The " +
          "directories including the found files\nare then backed up in " +
          "the destination location of your choice.\n\n")
    # Description of the possible parameters
    print("-help\t\tLists all possible commands for this script.\n")
    print("-start\t\tStarts the data extraction process.\n")
    printLine()
# END printHelpMsg

## createMainBackupDir(dstFilePath, backupDirName)
#  Function to create the main directory where the project file structure will
#  be copied to.
#
#  param srcFilePath    Absolute file path to the source directory to copy from.
#  param dstFilePath    Absolute file path to the destination directory, where
#                       the project file structure is copied to.
#  return               Absoulte file path of the created subdirectory.     
def createMainBackupDir(dstFilePath=None, backupDirName=None):
    # Start check of function parameters
    if dstFilePath == None:
        raise Exception("createMainBackupDir: Function called without " +
                        "dstFilePath parameter.")

    if backupDirName == None:
        raise Exception("createMainBackupDir: Function called without " + 
                        "backupDirName parameter.")
    # End check of function parameters                           

    try:
        # Change to destination path.
        os.chdir(dstFilePath)
        # Check if directory does NOT already exist.
        if not os.path.isdir(backupDirName):
            # Create backup directory.
            os.mkdir(backupDirName)
            # Store and return the absolute path to the created directory.
            backupPath = os.path.join(dstPath, backupDirName)
            return backupPath
        else:
            # Abort if project directory already exists, in order to prevent
            # unwanted file corruption!
            print("createMainBackupDir: Directory already exists. Please " + 
                  "either remove backup directory or\nchange the name for " + 
                  "it in the script.")
            print("Exit script.")
    except OSError:
        print("createMainBackupDir: Backup Folder could not be created. " +
              "Check if destination path is valid!")
        print("Exit script.")
        return
# END createMainBackupDir

## createBackupSubDir(srcFilePath, dstFilePath)
#  This function is used to create subdirectories from the source file path in
#  the backup / destination file path. The file structure will be copied 1:1.
# 
#  param srcFilePath    Absolute file path to the source directory to copy from.
#  param dstFilePath    Absolute file path to the destination directory, where
#                       the project file structure is copied to.
#  return               Absoulte file path of the created subdirectory.
def createBackupSubDir(srcFilePath=None, dstFilePath=None):
    # Start check of function parameters
    if srcFilePath == None:
        raise Exception("createBackupSubDir: Function called without " + 
                        "srcFilePath parameter.")

    if dstFilePath == None:
        raise Exception("createBackupSubDir: Function called without " +
                        "dstFilePath parameter.")
    # End check of function parameters 

    # Extract the directory name from the absolute source file path.
    srcDirName = os.path.split(srcFilePath)[-1]
    
    try:
        # Change to destionation path.
        os.chdir(dstFilePath)
        # Check if directory does NOT already exist.
        if not os.path.isdir(os.path.join(dstFilePath, srcDirName)):
            # Create backup directory.
            os.mkdir(srcDirName)
            # Store and return the absolute path to the created directory.
            backupPath = os.path.join(dstFilePath, srcDirName)
            return backupPath
    except OSError:
        print("createBackupSubDir: Could not create subdir in backup folder.")
        print("Exit script.")
        return
# END createBackupSubDir

## searchForFiles(srcFilePath, fileExtensions)
#  Function to search a source directory for files with certain file extensions.
#  If a file has a extension from the fileExtensions parameter (TUPLE!), its
#  name will be stored in a list. If files with a wanted extension were found, a
#  list with the filenames (filename.extension) is returned.
#  If NO files with a wanted extension were found, or no files at all than the
#  function returns 1.
#
#  param srcFilePath        Absoulte filepath where the search is conducted.
#  param fileExtensions     Tuple of file extensions to look for.
#  return                   If files found with wanted extensions, list with
#                           filenames+extension returned.
#                           if no files or no files with wanted extensions,
#                           return 1.
def searchForFiles(srcFilePath=None, fileExtensions=None):
    # Start check of function parameters
    if srcFilePath == None:
        raise Exception("searchForFiles: Function called without srcFilePath" +
                        " parameter.")

    if fileExtensions == None:
        raise Exception("searchForFiles: Function called without " + 
                        "fileExtensions parameter.")
    # End check of function parameters 

    # Retrieve directory list.
    dirList = os.listdir(srcFilePath)

    # Check if directory is empty (== no files, no directories)
    if len(dirList) == 0:
        # No content in directory, return.
        return 1

    # Create empty list to store filenames.
    fileNames = []

    # Otherwise iterate through directory content.
    for data in dirList:
        # Check if directory content is a file.
        if os.path.isfile(os.path.join(srcFilePath, data)):
            # Check if it has a desired file extension.
            if(data.endswith(fileExtensions)):
                # Store filenames with wanted extension in list.
                fileNames.append(data)

    if len(fileNames) == 0:
        # No files with a wanted file extension were found.
        return 1
    else:
        # At least one file with a wanted file extension was found.
        return fileNames
# END searchForFiles

## searchForDirectories(srcFilePath)
#  Function to search if the file path contains directories.
#
#  param srcFilePath    Absolute file path where the search is conducted.
#  return               If file path contains directories, return a list with
#                       all the directories.
#                       If there are NO directories in the file path, return 1.
def searchForDirectories(srcFilePath=None):
    # Start check of function parameters
    if srcFilePath == None:
        raise Exception("searchForDirectories: Function called without " +
                        "srcFilePath parameter.")
    # End check of function parameters

    # Retrieve directory list.
    dirList = os.listdir(srcFilePath)

    # Check if directory is empty (== no files, no directories)
    if len(dirList) == 0:
        # No content in directory, return.
        return 1

    # Create empty list to store names of subdirectories.
    subDirs = [] 

    for data in dirList:
        # Check if directory content is a directory.
        if os.path.isdir(os.path.join(srcFilePath, data)):
            subDirs.append(data)

    if len(subDirs) == 0:
        # No subdirectories were found.
        return 1
    else:
        # At least one subdirectory was found.
        return subDirs  
# END searchForDirectories

## extractFiles(srcFilePath, dstFilePath, fileList)
#  Extracts files provided in the fileList, from a given source file path to 
#  the given destination file path.
# 
#  param srcFilePath    Absolute filepath where files are copied from. 
#  param dstFilePath    Absolute filepath where files are copied to.
#  param fileList       List of filenames (including file extensions) that
#                       must be located in the srcFilePath directory.
def extractFiles(srcFilePath=None, dstFilePath=None, fileList=None):
    # Start check of function parameters
    if srcFilePath == None:
        raise Exception("extractFiles: Function called without " + 
                        "srcFilePath parameter.")

    if dstFilePath == None:
        raise Exception("extractFiles: Function called without " +
                        "dstFilePath parameter.")

    if fileList == None:
        raise Exception("extractFiles: Function called without " + 
                        "fileList parameter.")
    # End check of function parameters 

    if fileList != 1:
        # fileList exists and has at least one filename.
        for fname in fileList:
            # Create source path including filename.
            srcPath = os.path.join(srcFilePath, fname)
            # TODO: Add a verbose switch.
            print("Copy file: " + fname + " from source path: " + srcPath +
                  " to destination path " + dstFilePath)
            # Copy file from source to destination.
            shutil.copy(srcPath, dstFilePath)
    else:
        # No files were found. Nothing to extract.
        return 1
# END extractFiles

## extractProjectdata(srcFilePath, dstFilePath, fileExtensions)
#  Function to start the data extraction process. Copies a project directory
#  from the source file path to the destination file path. Directory structure
#  is kept. Only files with the defined file extensions are copied. 
#  Note that also empty folders are copied. Therefore, if the user does not
#  want empty folders to backup, the cleanBackupDir function must be called
#  after extractProjectdata is complete!
#  Function calls itself recursivly!
#
#  param srcFilePath        Absolute filepath where files are copied from. 
#  param dstFilePath        Absolute filepath where files are copied to.
#  param fileExtensions     Tuple of file extensions to look for.
def extractProjectdata(srcFilePath=None, dstFilePath=None, fileExtensions=None):
    # Start check of function parameters
    if srcFilePath == None:
        raise Exception("extractProjectdata: Function called without " + 
                        "srcFilePath parameter.")

    if dstFilePath == None:
        raise Exception("extractProjectdata: Function called without " +
                        "dstFilePath parameter.")

    if fileExtensions == None:
        raise Exception("extractProjectdata: Function called without " + 
                        "fileExtensions parameter.")
    # End check of function parameters 

    # Create a subdirectory folder in the destination file path.
    dstFilePath = createBackupSubDir(srcFilePath, dstFilePath)

    # Search for files in source directory that match defined file extensions.
    fileList = searchForFiles(srcFilePath, fileExtensions)

    # Extract files with defined file extensions from source directory.
    extractFiles(srcFilePath, dstFilePath, fileList)

    # Search if source directory contains subdirectories
    dirList = searchForDirectories(srcFilePath)

    # If there are subdirectories...
    if dirList != 1:
        # Go through each of the subdirectories...
        for directory in dirList:
            # Create a temporary absoulte source file path of the subdirectory.
            temp_srcFilePath = os.path.join(srcFilePath, directory)
            # Call extractProjectdata in the subdirectory!
            extractProjectdata(temp_srcFilePath, dstFilePath, fileTypes)

# END extractProjectdata

## cleanBackupDir(dstFilePath)
#  Search through the given filepath downwards and remove empty folders.
#  If a folder contains no files and no further subdirectories, the folder will
#  be removed. Function is recursively called, until all folders are checked and
#  or removed.
#
#  WARNING: BE CAREFUL WHICH FILEPATH YOU ENTER. IT MIGHT DELETE UNWANTED 
#           DIRECTORIES. USE AT YOUR OWN RISK!
#
#  param dstFilePath    Absoulte filepath from where the cleanup will start. 
#                       
def cleanBackupDir(dstFilePath=None):
    # Start check of function parameters
    if dstFilePath == None:
        raise Exception("extractProjectdata: Function called without " +
                        "dstFilePath parameter.")
    # End check of function parameters 

    print("\nStart cleanBackupDir at path: " + dstFilePath)

    # Change directory to destination file path.
    os.chdir(dstFilePath)
    # Search destination file path for subdirectories.
    dirList = searchForDirectories(dstFilePath)
    # Search destination file path for files.
    fileList = searchForFiles(dstFilePath, fileTypes)

    # If destination file path does not contain subdirectories or files...
    if fileList == 1 and dirList == 1:
        # Change one directory level up.
        os.chdir("..")
        # Retrieve directory name, which does not contain files or further 
        # directories.
        dirName = os.path.split(dstFilePath)[-1]
        print("Name of directory to remove: " + dirName)
        # Remove the directory that does not contain files or further 
        # directories.
        os.rmdir(dstFilePath)
        print("Directory removed!")
    # If destination file path contains subdirectories...
    elif dirList != 1:
        # Go through each subdirectory...
        for directory in dirList:
            # Create a temperorary absolute file path.
            temp_dstFilePath = os.path.join(dstFilePath, directory)
            #print("Search for dir to remove in: " + temp_dstFilePath)
            # Run cleanBackupDir on this subdirectory.
            cleanBackupDir(temp_dstFilePath)
# END cleanBackupDir

# ------------------------------------------------------------------------------
# MAIN ROUTINE
# ------------------------------------------------------------------------------
# The main routine is composed to extract data of Xilinx Vivado Projects.
# From the project folder only the files in the main directory and files 
# from the project.src needs to be extracted. File extensions reduce the data
# copied down to the essentials.
# ------------------------------------------------------------------------------
# Header
printHeader()

# Get number of arguments
argCnt = len(sys.argv)

if argCnt < 2:
    # No arguments, print help message.
    printHelpMsg()
elif (argCnt < 3) and (sys.argv[1] == "-start" or sys.argv[1] == "start"):
    # 1 argument, either "-start" or "start".

    # --- Start Xilinx Vivado Specific Routine ---
    # Try to create backup directory
    mainBackupPath = createMainBackupDir(dstPath, backupDirName)
    # Create Subdirectory for project
    projectbackupPath = createBackupSubDir(srcPath, mainBackupPath)
    # # Search for files in source directory
    fileList = searchForFiles(srcPath, fileTypes)
    # Extract files with certain file extensions from source directory.
    extractFiles(srcPath, projectbackupPath, fileList)
    # Check if a directory exists in source directory.
    dirList = searchForDirectories(srcPath)
    print(dirList) # debug
    for directory in dirList:
        if srcPathSubdirContains in directory:
            print(directory) # debug
            srcPath = os.path.join(srcPath, directory)
            print(srcPath) # debug
    # --- End Xilinx Vivado Specific Routine ---

    # Extract data from the <projectname>.srcs folder
    extractProjectdata(srcPath, projectbackupPath, fileTypes)
    printLine()

    # Cleanup backup dir from directories, that are empty.
    cleanBackupDir(mainBackupPath)
    printLine()

elif (argCnt < 3) or (sys.argv[1] == "-help") or (sys.argv[1] == "help"):
    # 1 argument, either "-help" or "help"
    printHelpMsg()