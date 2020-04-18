# extractProjectdata.py

This script may be used to extract data from project directories of your choice.
It is explicitly designed to extract certain file types out of Xilinx Vivado
projects and retaining the underlying directory structure. Empty folders
(= contain no folders or files) in the destination directory are deleted.

## Usage

Copy this script in a folder, from where you can execute it. You can configure a
default source and destination directory as well as filetypes to search for in
the script itself. Arguments for source- and destination-paths as well as
filetypes override the default values.

**WARNING:** Since the script deletes empty folders in the destination
directory, make sure that the destination path is correctly defined.

Print help for possible arguments to pass.

```sh
python extractProjectdata.py --help
```

Extract projectdata from source-path, copy it to destination path. Only
the passed filetypes are extracted. Non-Verbose mode.

```sh
python extractProjectdata.py -src "/home/User/ProjectDir/Proj" -dst "/home/User/Temp" --filetypes ".v, .xdc, .vhd, .bd, .tcl"
```

Extract projectdata from source-path, copy it to destination path. Only
the passed filetypes are extracted. Verbose mode.

```sh
python extractProjectdata.py -src "/home/User/ProjectDir/Proj" -dst "/home/User/Temp" --filetypes ".v, .xdc, .vhd, .bd, .tcl" -v
```

## Release History

* 1.0.0
  * First proper release.
