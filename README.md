# Geosoftware II Project of the Group "A²HL²", WWU <!-- omit in toc -->

[Aysel Tandik](https://github.com/atlanta11950), [Anika Graupner](https://github.com/Anika2), [Henry Fock](https://github.com/HenFo), [Lia Kirsch](https://github.com/cherry13579), [Lukas Jahnich](https://github.com/lukasjah)

**Project order:** This project will close the gap between geospatial data formats and repositories respectively geospatial metadata catalogues and similarity measurements. Project groups will extend an existing Free and Open Source Software (FOSS) project with the functionality to retrieve and view similar records. This comprises both the API and UI, namely providing an HTTP endpoint to retrieve an ordered list of records based on a provided record and displaying/linking similar records in a detail view of a record respectively.

## Table of Contents <!-- omit in toc -->
- [Using the CLI-Tools](#using-the-cli-tools)
    - [Installed using the code](#installed-using-the-code)
    - [Installed using pip](#installed-using-pip)
  - [Examples](#examples)
- [Using the CLI-Tools with PyCSW](#using-the-cli-tools-with-pycsw)
  - [Usage](#usage)
- [Map based search of records](#map-based-search-of-records)

  
## Using the CLI-Tools
First you need to install the CLI-Tools. An installation guide is in the README inside the CLI Tools folder
#### Installed using the code

 Open the commandline and navigate to the CLI Tools folder in our project folder `$ cd CLI Tools` and type `$ python masterExtract.py --help` to show the options you can chose from.

#### Installed using pip
If pip is installed:
- `$ pip install geodataExtent`
- If GDAL won't install, try method above
- download ogr2ogr as described above

type `$ extract-extent --help`

```bat
Options:
  --path TEXT  Path to Folder containing Geofiles
  -c, --clear  Clear screen before showing results
  -t, --time   execute time extraction for one file
  -s, --space  execute boundingbox extraction for one file
  -h, --hull   execute convex-hull extraction for one file
  --help       Show this message and exit.
```
Those are **only** options, you do not have to use them. However, if you do not choos any of the execution flags `(-t / -s / -h)`, the folderextraction will be triggered and gives you the spatial and temporal extent of each of your Geofiles within the chosen folder in addition to the full spatial and temporal extent of the folder.

You are not limeted to choose only one option but all of them at once except for `--help`.

If you do not use `--path`, the path will be prompted. That means it is a shortcut only.

### Examples

```
$ python masterExtract.py -t -s -h  'OR' extract-extent -t -s -h
Pleas enter path to Folder: <path>
Pleas enter filename: <filename>

Timeextent:
['1935/01/01 00:00:00 GMT+0', '2014/01/01 00:00:00 GMT+0', 365.253164556962]


Spatialextent:
[-179.5, -89.5, 179.5, 89.5]


Spatialextent as Convex Hull:
[(-179.5, -89.5), (-179.5, 89.5), (179.5, 89.5), (179.5, -89.5)]
```

The Timeextent starts with the beginning and ends with the end date as ISO8601 standard. the last number is the average intervall in which measurements have been taken.

The spatial extent is shown as a boundingbox. `[minX/minLong, minY/minLat, maxX/maxLong, maxY/maxLat]`

For more percission the `-h / --hull` flag gives you the spatial exnent as a convex hull. That means from all the points of a dataset the outer most points are beeing calculated and returned in correct order.

#### Folderextraction <!-- omit in toc -->

If you want to extract your hole folder, the `-c / --clear` flag is recommended because a long list of processing outputs is generated before the final output appears.
```
$ python masterExtract.py -c --path "<folder path>"
$ extract-extent -c --path "<folder path>"
```

## Using the CLI-Tools with PyCSW
PyCSW has to run!

#### Installed using Code: <!-- omit in toc -->
In the command prompt
- run `$ cd CLI Tools`
- and use `$ python sendToPyCSW.py --help`

#### Installed using pip: <!-- omit in toc -->
- in command prompt run `extract2pycsw --help`

### Usage
First of all you need to have some data in pycsw because the CLI-Tool is a support tool **only**.

**It can extract the spatial and temporal extent of your Geodata but needs to have a place in the database to send it to!**

```
$ extract2pycsw --help

Usage: extract2pycsw [OPTIONS]

  CLI-Tool for extracting the spatial and temporal extant of a selected
  Geodile and sends the results to the corrosponding ID in PyCSW to update
  the entery.

       Returns the XML Response of PyCSW after the update in the consloe

Options:
  --path TEXT     Path to Folder containing Geofiles
  --name TEXT     Filename with extension
  -i, --id TEXT   PyCSW ID of corrosponding file
  -u, --url TEXT  If you have a different URL to your pycsw, you can change it
                  using this option
  --help          Show this message and exit.
```

- `--path` option specifies the folder in which your Geodata is located
- `--name` option is the full name of your file you want to work with
- `-i / --id` option is the repository specific ID/primary key under which the corrosponding recordcan be found in pycsw
- `-u / --url` option can be used if your pycsw runs on a different port than 8000 or cannot be accessed via localhost. If that's the case, you will have to specify the correct URL. The default is `http://localhost:8000/csw`

**Example using all options:**
```
$ extract2pycsw --path "C:/User/Desptop/Geodatafolder" --name "features.geojson" -i "aga" -u "http://localhost:3000/csw"
```
If you missed any important options they will be prompted, so don't worry you missed something
```
$ extract2pycsw
Please enter path to Folder: <path>
File name: <filename>
Please enter correct file ID for PyCSW: <ID>
```
will give a response like
```xml
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!-- pycsw 2.3.dev0 -->
<csw:TransactionResponse xmlns:csw="http://www.opengis.net/cat/csw/2.0.2" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dct="http://purl.org/dc/terms/" xmlns:gmd="http://www.isotc211.org/2005/gmd" xmlns:gml="http://www.opengis.net/gml" xmlns:ows="http://www.opengis.net/ows" xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" version="2.0.2" xsi:schemaLocation="http://www.opengis.net/cat/csw/2.0.2 http://schemas.opengis.net/csw/2.0.2/CSW-publication.xsd">
    <csw:TransactionSummary>
        <csw:totalInserted>0</csw:totalInserted>
        <csw:totalUpdated>5</csw:totalUpdated>
        <csw:totalDeleted>0</csw:totalDeleted>
    </csw:TransactionSummary>
</csw:TransactionResponse>
```
If something like that appears, your dataset has successfully been updated in spatial and temporal extent and the similaritie to all other datasets has been calculated.

Similar records can be viewed using the links descriebed in: [Test our additional features:](#test-our-additional-features).

## Map based search of records
If you want to finde records from pycsw and use spatial filters on a map, you can use our map feature.

The map can only be used if you have downloaded the project, it doesn't work using the Docker image from DockerHub.

**On Windows:**
You can double-click the bootCode.bat file located in the project folder. That will open up two windows. First of all a command window and a PowerShell window. You only need the cmd window for the map, the PowerShell window can be closed.

**On other operating systems that cannot start a batch file:**
Open a command window and navigate to the project folder and into the MapSearch folder.
```
$ python webmap.py
```

Those options will start the map service. If not, try to run the requirements.txt file using pip `$ pip install -r requirements.txt`. That will install Flask to your Python-Modules.
Now retry!

If the file started correctly, go in your Browser and to [localhost:5000](http://localhost:5000/). A map should appear and you can choose from two options:
- get all records within your map section
  - zoom to a location where you want to have records from and hit the button *"get Geodata in Viewport"*
- get all records within drawn polygons
  - draw polygons over the locations you want your records from and hit the button *"get Geodata within Polygons"*

You will get a table with all found records and a boundingbox drawn on the map.
You can get a GeoJSON representation of a boundingbox if you click on that boundingbox in the table.




