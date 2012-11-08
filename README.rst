sixelterm
=========

Install
-------

via github ::

    $ git clone https://github.com/saitoha/sixelterm.git
    $ cd sixelterm
    $ python setup.py install

or via pip ::

    $ pip install sixelterm


Usage
-----

::

    $ sixelterm
    $ cat test.jpg 

    [imagefile] is expected to be a PNG/JPEG formatted image file.

* Options::

    -h, --help                  show this help message and exit
    --version                   show version

Dependency
----------
 - PySixel
   https://github.com/saitoha/PySixel

 - PySixel depends on Python Imaging Library (PIL)
   http://www.pythonware.com/products/pil/ 

 - TFF - Terminal Filter Framework
   https://github.com/saitoha/tff


Reference
---------
 - Gate One, Liftoff Software
   http://liftoffsoftware.com/Products/GateOne

 - Chris_F_Chiesa, 1990 : All About SIXELs
   ftp://ftp.cs.utk.edu/pub/shuford/terminal/all_about_sixels.txt

 - Netpbm http://netpbm.sourceforge.net/

   It includes ppmtosixel command
   http://netpbm.sourceforge.net/doc/ppmtosixel.html

 - vt100.net http://vt100.net/

   DECDLD
   http://vt100.net/docs/vt510-rm/DECDLD

