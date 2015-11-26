import urllib2
import json
import logging


def get_queue(url):
    asset=None
    req = urllib2.Request(url)
    req.add_header('Content-Type', 'application/json')
    data = {}
    logger.debug("get_queue - url="+url+" data="+str(data))
    try:
        resp = urllib2.urlopen(req, json.dumps(data))
        s = resp.read()
        logger.debug("get_queue - response="+s)
        jsonobj = json.loads(s)
        if 'assets' in jsonobj:
            asset = jsonobj['assets']
    except urllib2.HTTPError as e:
        logger.error("get_queue - HTTPError: url=" + e.url + " code=" + str(e.code)+" message="+str(e.msg))
    except IOError as e:
        logger.error("get_queue - I/O error({0}): {1}".format(e.errno, e.strerror))
    except KeyError as e:
        logger.error("get_queue - KeyError:  assets not found in response  "+str(e.message))
    except Exception as e:
        logger.error("get_queue - Exception:  message="+str(e.message))
    return asset

logger=logging.getLogger("portal.queue")