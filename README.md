# About

`latlng2cc.py` is a simple Python script to find the ISO two-letter country code corresponding to a latitude-longitude coordinate. The script uses [Google's Reverse Geocoding API](https://developers.google.com/maps/documentation/geocoding/intro#reverse-example) to lookup the location corresponding to a latitude-longitude coordinate.


# Running

Invoking without any arguments shows the usage information.
```
$ ./latlng2cc.py
usage: latlng2cc.py [-h] [--version] [-v] [-o out-path] [--delim delimiter]
                    in-path
latlng2cc.py: error: the following arguments are required: in-path
```

Detailed help on the usage of the script can be obtained by invoking with `-h` or `--help` switch.
```
$ ./latlng2cc.py -h
usage: latlng2cc.py [-h] [--version] [-v] [-o out-path] [--delim delimiter]
                    in-path

Convert latitude-longitude coordinates to ISO two-letter country codes.

positional arguments:
  in-path               Absolute or relative path containing file containing
                        latitude-longitude coordinates.

optional arguments:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  -v, --verbose         Enable verbose output.
  -o out-path, --output out-path
                        Absolute or relative path of output file.
  --delim delimiter     Delimiter for parsing the latitude-longitude
                        coordinates in file..
```

The following shows a sample invocation with all the required arguments passed to the script.
```
$ ./latlng2cc.py latlng.txt

# After some time ...
$ wc -l latlng-cc.txt latlng.txt
     521 latlng-cc.txt
     521 latlng.txt
    1042 total
```
