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
import sys, os, datetime, shutil, argparse
# ------------------------------------------------------------------------------
# GLOBAL VARIABLE DEFINITIONS
# ------------------------------------------------------------------------------
#srcPath = "C:\\Xilinx\\vivprj\\ARTY_A7_Sys01"
srcPath = "/home/stefan-e495/XilPrj/NF_MB_Basic"
#dstPath = "C:\\Users\\Stefan\\Temp\\"
dstPath = "/home/stefan-e495/Temp/"
fileTypes = (".xpr", ".bd", ".tcl", ".vhd", ".v", ".sv", ".xdc", ".xci")

# String that a folder inside srcPath must contain, that will also be searched
# for files and further subdirectories. Rest will be ignored.
srcPathSubdirContains = ".srcs"

# Backup directory name
CreationTime = datetime.date.today().strftime("%y%y%m%d")
BackupDirName = CreationTime + "_XilProj_Backup"
backupPath = ""

# Settings
VerboseMode = False # Print Logging Messages in Console

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

## conv2tuple(arg)
#  Function to allow parsing filetypes as string and converting them to a tuple.
#
#  param arg    String in the following format: ".v, .txt, .vhd"
#               Filetypes may be choosen as required.
#  return       Tuple made from input string.
def conv2tuple(arg):
    if(isinstance(arg, str)):
        return tuple(map(str, arg.split(', ')))
    else:
        raise Exception("conv2tuple: Parsed argument is not a string!")
# END conv2tuple

## createMainBackupDir(dstFilePath, BackupDirName)
#  Function to create the main directory where the project file structure will
#  be copied to.
#
#  param srcFilePath    Absolute file path to the source directory to copy from.
#  param dstFilePath    Absolute file path to the destination directory, where
#                       the project file structure is copied to.
#  return               Absoulte file path of the created subdirectory.     
def createMainBackupDir(dstFilePath=None, BackupDirName=None):
    # Start check of function parameters
    if dstFilePath == None:
        raise Exception("createMainBackupDir: Function called without " +
                        "dstFilePath parameter.")

    if BackupDirName == None:
        raise Exception("createMainBackupDir: Function called without " + 
                        "BackupDirName parameter.")
    # End check of function parameters                           

    try:
        # Change to destination path.
        os.chdir(dstFilePath)
        # Check if directory does NOT already exist.
        if not os.path.isdir(BackupDirName):
            # Create backup directory.
            os.mkdir(BackupDirName)
            # Store and return the absolute path to the created directory.
            backupPath = os.path.join(dstPath, BackupDirName)
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
        return 1
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
#                           If no files or no files with wanted extensions,
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
            # Print Logging-Message in Verbose-Mode.
            if(VerboseMode):
                print("Copy file: " + fname + " from source path: " + srcPath +
                    " to destination path " + dstFilePath)
            # Copy file from source to destination.
            shutil.copy(srcPath, dstFilePath)
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

    # Print Logging-Message in Verbose-Mode.
    if(VerboseMode):
        print("\nClean backup directory: " + dstFilePath)

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

        # Print Logging-Message in Verbose-Mode.
        if(VerboseMode):
            print("Name of directory to remove: " + dirName)

        # Remove the directory that does not contain files or further 
        # directories.
        os.rmdir(dstFilePath)

        # Print Logging-Message in Verbose-Mode.
        if(VerboseMode):
            print("Directory removed!")
    
    # If destination file path contains subdirectories...
    elif dirList != 1:
        # Go through each subdirectory...
        for directory in dirList:
            # Create a temporary absolute file path.
            temp_dstFilePath = os.path.join(dstFilePath, directory)
            # Run cleanBackupDir on this subdirectory.
            cleanBackupDir(temp_dstFilePath)
# END cleanBackupDir

# ------------------------------------------------------------------------------
# PARSER
# ------------------------------------------------------------------------------
parser = argparse.ArgumentParser(description=r'''extractProjectdata.py''',
                                 formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument("-src", "--src",
                    help="Parent path where data should be extracted from.",
                    type=str)
parser.add_argument("-dst", "--dst",
                    help='''Path where folder to store extracted data should be created.''', 
                    type=str)
parser.add_argument("-ft", "--filetypes", 
                    help='''String of file types that should be extracted from the src-path. Format: \".v, .bd, .tcl\"''', 
                    type=conv2tuple)
parser.add_argument("-v", "--verbose",
                    help='''Verbose-Mode. Prints logging-messages in the console.''',
                    action='store_true')  

args = parser.parse_args()

# Check if source-path is parsed.
if(args.src != None):
    if(os.path.isdir(args.src)):
        srcPath = args.src
        print("Source-Path: {0}".format(srcPath))
    else:
        print("Default source-path is used: {0}".format(srcPath))
else:
    print("Default source-path is used: {0}".format(srcPath))

# Check if destination-path is parsed.
if(args.dst != None):
    if(os.path.isdir(args.dst)):
        dstPath = args.dst
        print("Destination-Path: {0}".format(dstPath))
    else:
        print("Default destination-path is used: {0}".format(dstPath))
else:
        print("Default destination-path is used: {0}".format(dstPath))

# Check if filetypes are parsed.
if(args.filetypes != None):
    if isinstance(args.filetypes, tuple):
        fileTypes = args.filetypes
        print("Filetypes: {0}".format(fileTypes))
    else:
        print("Default filetypes are used: {0}".format(fileTypes))
else:
    print("Default filetypes are used: {0}".format(fileTypes))

# Check if verbose argument is parsed.
if(args.verbose != None):
    VerboseMode = args.verbose

# ------------------------------------------------------------------------------
# MAIN ROUTINE
# ------------------------------------------------------------------------------
# The main routine is composed to extract data of Xilinx Vivado Projects.
# From the project folder, only the files in the main directory and files 
# from the project.src needs to be extracted. Only required filetypes get 
# extracted to save space.
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    # Print Header
    printHeader()

    # Create backup directory.
    mainBackupPath = createMainBackupDir(dstPath, BackupDirName)

    # Create Subdirectory for project.
    projectbackupPath = createBackupSubDir(srcPath, mainBackupPath)

    # Search for files in source directory.
    fileList = searchForFiles(srcPath, fileTypes)

    # Extract files with certain file extensions from source directory.
    extractFiles(srcPath, projectbackupPath, fileList)

    # Check if a directory exists in source directory.
    dirList = searchForDirectories(srcPath)
    
    # Print Logging-Message in Verbose-Mode.
    if(VerboseMode):
        print(dirList)
    
    for directory in dirList:
        if srcPathSubdirContains in directory:
            srcPath = os.path.join(srcPath, directory)

    # Extract data from directory.
    extractProjectdata(srcPath, projectbackupPath, fileTypes)

    # Print Logging-Message in Verbose-Mode.
    if(VerboseMode):
        printLine()

    # Cleanup backup-directory from directories, that are empty.
    cleanBackupDir(mainBackupPath)

    # Print Logging-Message in Verbose-Mode.
    if(VerboseMode):
        printLine()