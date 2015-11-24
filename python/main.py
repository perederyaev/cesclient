import os
import sys
import config
import codecs
import logging
import logging.config

import aria.rpc
import aria.daemon
import portal.queue
import portal.download_status
import store.user
import store.download


def if_file_downloaded(filename, size):
    if os.path.isfile(filename):
        if os.path.getsize(filename) == size:
            return True
    return False


sys.stdout = codecs.getwriter('utf-8')(sys.stdout)

logging.config.fileConfig(config.cesclient_log_config,disable_existing_loggers=False)

logger = logging.getLogger()

logger.info('starting main script...')

aria.daemon.main(config.aria_cmd,config.aria_pidfile)

assets = portal.queue.get_queue(config.portal_url_api_getqueue)
if assets is None:
    logging.info("assets is None.")
    sys.exit(0)

assets_download_status = []
for asset in assets:
    asset_id_s = asset['id']
    asset_id = int(asset_id_s)
    asset_name = asset['asset_name']
    logging.info("asset_id:" + asset_id_s + " asset_name:" + asset_name)
    asset_downloaded_size = 0
    asset_total_size = 0
    asset_downloaded_files = 0
    asset_total_files = len(asset['files'])
    for asset_file in asset['files']:
        asset_file_src_name = asset_file['src_name']
        asset_file_size = int(asset_file['size'])
        asset_file_name = asset_file['file_name']
        asset_file_url = asset_file['url']
        logging.info("asset_file=" + asset_file_src_name + " " + str(asset_file_size) + " " + asset_file_name + " " + asset_file_url)
        asset_total_size = asset_total_size + asset_file_size
        if if_file_downloaded(config.download_dir_ready + "/" + asset_file_name, asset_file_size):
            asset_downloaded_size = asset_downloaded_size + asset_file_size
            asset_downloaded_files = asset_downloaded_files + 1
        else:
            gid=aria.rpc.generate_gid(asset_file_name)
            asset_file_st=aria.rpc.get_status(config.aria_rpc_url,config.aria_token,gid)
            asset_file_completed_size=asset_file_st['completedLength']
            asset_file_status=asset_file_st['status']
            if asset_file_status == 'complete':
                store.download.on_complete(config.download_dir+'/'+asset_file_name,config.download_dir_ready+'/'+asset_file_name)
            else:
                    if asset_file_completed_size > 0:
                        asset_downloaded_size=asset_downloaded_size + asset_file_completed_size
                    else:
                        gid2 = aria.rpc.start_download(config.aria_rpc_url,config.aria_token,asset_file_url,gid)
                        logging.info( "Starting download of file:" + asset_file_name + " gid:" + gid)

    if asset_downloaded_files == asset_total_files:
        logging.info( "asset is ready - asset_id:" + asset_id_s + " asset_name:" + asset_name)
        if store.user.publish_asset(asset,config.download_dir,config.user_dir) == 0:
            assets_download_status.append({"asset_id": asset_id, "received_bytes": asset_downloaded_size, "received_files": asset_downloaded_files,"downloaded":1})
    else:
        logging.info( "asset is not ready - asset_id:" + asset_id_s + " asset_name:" + asset_name + \
              " asset_downloaded_size:" + str(asset_downloaded_size) + \
              " asset_total_size:" + str(asset_total_size) + \
              " asset_downloaded_files:" + str(asset_downloaded_files) + \
              " asset_total_files:" + str(asset_total_files))
        assets_download_status.append({"asset_id": asset_id, "received_bytes": asset_downloaded_size, "received_files": asset_downloaded_files,"downloaded": 0})
        break


if len(assets_download_status) > 0:
    portal.download_status.send_download_status(config.portal_url_api_download_status, {"assets_download_status": assets_download_status})
