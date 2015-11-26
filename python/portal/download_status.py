import json
import logging
import urllib2


def send_download_status(url, data):
    logger.info("send_download_status - sending json to url:" + url)
    req = urllib2.Request(url)
    req.add_header('Content-Type', 'application/json')
    try:
        response = urllib2.urlopen(req, json.dumps(data))
        s = response.read()
        json_obj=json.loads(s)
    except urllib2.HTTPError as e:
        logger.error("send_download_status - HTTPError: url=" + e.url + " code=" + str(e.code)+" message="+str(e.msg))
        return -1
    except ValueError as e:
        logger.error("send_download_status - ValueError: " + str(e.message))
        return -1
    else:
        if json_obj['result'] != 'successful':
            logger.warning("send_download_status - response: " + json_obj['message'])
            return -1
        logger.info("send_download_status completed succesfully")

    logger.debug("send_download_status response: "+s)
    return 0

logger = logging.getLogger('portal.download_status')