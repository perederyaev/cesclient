import sys
import json
import urllib2
import logging

def get_aria_token(s):
    if len(s)>0:
        return "token:"+s
    else:
        return "token:"


def send_command(aria_rpc_url, aria_rpc_command):
    req_aria = json.dumps(aria_rpc_command)
    logger.info("send_command - req_aria="+req_aria)
    resp_aria = None
    try:
        c = urllib2.urlopen(aria_rpc_url, req_aria)
        resp_aria = c.read()
    except urllib2.HTTPError as e:
        logger.error("send_command - HTTPError url=" + e.url + " code=" + str(e.code))
        resp_aria=None
    return resp_aria


def start_download(rpc_url,token,file_url,gid):
    token_str=get_aria_token(token)
    aria_add_cmd = {'jsonrpc': '2.0', 'id': 'qwer', 'method': 'aria2.addUri', 'params': [token_str,[file_url],{'gid':gid}]}
    logger.info("start_download - sending command to aria:"+str(aria_add_cmd))
    resp_aria = send_command(rpc_url, aria_add_cmd)
    if resp_aria is not None:
        logger.info("start_download - got response from aria:"+resp_aria)
        try:
            aria_add_resp = json.loads(resp_aria)
            aria_gid = aria_add_resp["result"]
        except ValueError as e:
            aria_gid=""
    else:
        aria_gid=""
    return aria_gid

def get_status(rpc_url,token,gid):
    token_str=get_aria_token(token)
    aria_cmd = {'jsonrpc': '2.0', 'id': 'qwer', 'method': 'aria2.tellStatus', 'params': [token_str,gid,['completedLength','status']]}
    logger.info("get_status - sending command to aria:"+str(aria_cmd))
    resp = send_command(rpc_url, aria_cmd)
    st={}
    completedLength=-1
    status=""
    if resp is not None:
        logger.info("get_status: got response from aria:"+resp)
        try:
            resp_json = json.loads(resp)
            completedLength = int(resp_json["result"]["completedLength"])
            status=resp_json["result"]["status"]
        except ValueError as e:
            completedLength=-1
            status=""
            logger.error("get_status - ValueError:"+e.message)
    logger.info("get_status - completedLength="+str(completedLength)+" status=" + status + " for gid="+gid)
    st['completedLength']=completedLength
    st['status']=status
    return st


def generate_gid(filename):
    gid=format((hash(filename) % ((sys.maxsize + 1) * 2)),'x')
    logger.info("generate_gid: generated gid="+gid+" for filename="+filename)
    return gid

logger=logging.getLogger("aria.rpc")
