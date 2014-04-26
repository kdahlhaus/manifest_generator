manifest_gen - a HTML5 application cache manifest generator
===========================================================
Copyright 2014 by Kevin Dahlhausen (kpd@powertwenty.com)




NOTE: ****** THIS IS NOT YET READY TO USE - the manifest format is not complete *************




Overview
--------
This package contains a utility to generate the HTML5 application cache manifest file.   Running it multiple times only changes the manifest if the manifest contents or contents of files listed in the cache change. 

License
-------
This software is licensed under the GNU GPL.  Please see the file 'LICENSE' for details.  Note that this license requires any software using this library to make source code available. 

Should you not wish to use the software under a different license, please contact Kevin Dahlhausen (kpd@powertwenty.com) to discuss alternative licensing.
 

Requires
--------
glob2


Usage
-----

manifest_gen -o offlinecache.manifest -c "js/**/*.js" -c "css/**/*" -e dontcache.js -n counter.html -f fallback.html

manifest_gen -h for help


Tests
-----
To run the unit tests (python >= 2.7):
    python -m unittest discover
