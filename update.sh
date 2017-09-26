#!/bin/bash

python update.py

/etc/init.d/apache2 stop
/etc/init.d/fusion stop

/etc/init.d/apache2 start
/etc/init.d/fusion start
