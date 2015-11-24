import json
import logging
import urllib2


def send_download_status(url, data):
    logger.info("send_download_status - sending json to url:" + url)
    req = urllib2.Request(url)
    req.add_header('Content-Type', 'application/json')
    try:
        response = urllib2.urlopen(req, json.dumps(data))
    except urllib2.HTTPError as e:
        logger.error("send_download_status HTTPError: url=" + e.url + " code=" + str(e.code))
        logger.debug("send_download_status" + json.dumps(data))
        return 1
    s = response.read()
    logger.info("send_download_status response: "+s)
    return 0

logger = logging.getLogger('portal.download_status')