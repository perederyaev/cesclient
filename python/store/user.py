import os
import logging


def publish_asset(asset,download_dir,user_dir):
    asset_name = asset['asset_name']
    d=user_dir+"/"+asset_name
    try:
        if not os.path.exists(d):
            os.makedirs(d)
            logger.info("publish_asset - creating dir="+d)
    except OSError as e:
        logger.info("publish_asset - OSError:  can't create dir="+d)
        return -1

    for asset_file in asset['files']:
        asset_file_src_name = asset_file['src_name']
        asset_file_name = asset_file['file_name']
        src=download_dir+"/"+asset_file_name
        dst=d+"/"+asset_file_src_name
        try:
            logger.debug("publish_asset - trying to link src="+src + " to "+dst)
            if os.path.exists(dst):
                os.remove(dst)
            os.link(src,dst)
        except OSError as e:
            logger.error("publish_asset - OSError:  can't link file src="+src + " to "+dst)
            return -1

    logger.info("publish_asset - all files were linked")

    return 0

logger=logging.getLogger("store.user")