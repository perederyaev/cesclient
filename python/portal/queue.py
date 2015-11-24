import urllib2
import json
import logging


def get_queue(url):
    asset=None
    req = urllib2.Request(url)
    req.add_header('Content-Type', 'application/json')
    data = {}
    logger.debug("get_queue url="+url+" data="+str(data))
    try:
        resp = urllib2.urlopen(req, json.dumps(data))
        s = resp.read()
    except urllib2.HTTPError as e:
        logger.error("get_queue - HTTPError: url=" + e.url + " code=" + str(e.code)+" message="+str(e.msg))
    except IOError as e:
        logger.error("get_queue - I/O error({0}): {1}".format(e.errno, e.strerror))
    else:
        jsonobj = json.loads(s)
        asset = jsonobj['assets']
    return asset

logger=logging.getLogger("portal.queue")