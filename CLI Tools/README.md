# How to install the CLI-Tools
First, make sure you installed Python and pip. 
Most importatnly you need to know where you installed it to.

## Install from code
- in main folder run console and type `$ pip install -r requirements.txt`
  - that should install allmost all nessecary modules.
  
### Install GDAL

**On Windows:**
- try `$ pip install gdal` however that probably won't work
  - ignore the rest if it worked
- head over to [this site](https://www.lfd.uci.edu/~gohlke/pythonlibs/#gdal) and download a GDAL file. The "cp" in the filename stands for a Python version i.e. ...cp37... means Python3.7
  - save to a folder of your favor
- run `$ pip install <path to .whl file>`
- If it doesn't work, try a different file

**On MacOS:**
- Install Anaconda
- In terminal run `$ conda install gdal`

### Install ogr2ogr
- head over to [this site](http://svn.osgeo.org/gdal/trunk/gdal/swig/python/samples/ogr2ogr.py), than hit <kbd>CTRL</kbd>+<kbd>s</kbd> on your keybord to save ogr2ogr
- save the file to your site-packages
  - site-packages is located in your Python installation folder
  - i.e. \Program Files (x86)\Python37-32\Lib\site-packages
    - often PYthon is installed to the "appdata" folder. To get there hit <kbd>WIN</kbd>+<kbd>r</kbd> on Windows and type "%appdata%"

Now, everything should work.

## Install from PyPi
- In your command window, run `$ pip install geodataextent`
- Install GDAL and ogr2ogr the same way as above except for the site-packages folder, the folder in question is now in the installation folder of Anaconda

