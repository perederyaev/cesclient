import logging
import logging.config

import config
import portal.device_status

logging.config.fileConfig(config.cesclient_log_config,defaults={'logfilename': config.cesclient_log_dir+'/send_device_status.log'},disable_existing_loggers=False)
data = portal.device_status.get_device_status(config.uuid,config.version_image,config.version_soft)
portal.device_status.send_device_status(config.portal_url_api_device_status,data)
