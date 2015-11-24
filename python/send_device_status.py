import logging

import config
import portal.device_status

#logging.basicConfig(filename=config.log_dir+'/send_device_status.log',level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

data = portal.device_status.get_device_status(config.uuid,config.version_image,config.version_soft)
portal.device_status.send_device_status(config.portal_url_api_device_status,data)
