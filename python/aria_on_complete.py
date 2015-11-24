#!/usr/bin/python

import os
import sys
import logging

import config
import store.download

logging.basicConfig(filename=config.log_dir+'/aria_on_complete.log',level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

print sys.argv

if len(sys.argv) < 4:
    print "Not enough command line params! Exiting.."
    logging.debug('Not enough command line params! Exiting..')
    sys.exit(1)

GID=sys.argv[1]
filepath=sys.argv[3]
filename=os.path.basename(filepath)
filepath_ready=config.download_dir_ready+"/"+ filename
store.download.on_complete(filepath,filepath_ready)

