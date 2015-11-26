#!/usr/bin/python

import os
import sys
import logging

import config
import store.download

logging.config.fileConfig(config.cesclient_log_config,defaults={'logfilename': config.cesclient_log_dir+'/aria_on_complete.log'},disable_existing_loggers=False)


print sys.argv

if len(sys.argv) < 4:
    logging.debug('Not enough command line params! Exiting..')
    sys.exit(1)

GID=sys.argv[1]
filepath=sys.argv[3]
filename=os.path.basename(filepath)
filepath_ready=config.download_dir_ready+"/"+ filename
store.download.on_complete(filepath,filepath_ready)

