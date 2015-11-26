import os
import json
import time
import re
import logging
import urllib2
import subprocess


def uptime():
    u=0
    try:
        with open( "/proc/uptime" ) as f :
            s=f.readline().split()[0]
            u=int(float(s))
            logging.debug("uptime - uptime_seconds="+str(u))
    except EnvironmentError as e:
        logger.warning("uptime - can't read uptime from /proc/uptime: "+str(e.strerror))
    return u


def get_mem_info():
    mem=[0,0]
    try:
        with open( "/proc/meminfo" ) as f :
            meminfo = f.read()
            matched = re.search(r'^MemTotal:\s+(\d+)', meminfo,re.MULTILINE)
            if matched:
                mem[0]=int(matched.groups()[0])*1024
            matched = re.search(r'^MemFree:\s+(\d+)', meminfo,re.MULTILINE)
            if matched:
                mem[1]=int(matched.groups()[0])*1024
    except:
        logger.warning("get_mem_info - can't read mem info from /proc/meminfo")
    return mem


def get_ip():
    ips=""
    try:
        raw = subprocess.check_output(['/sbin/ip', 'addr', 'show'])
        matched=re.findall(r'inet\s+([\d|\.]+)\/', raw,re.MULTILINE)
        if matched:
            for ip in matched:
                if ip != '127.0.0.1':
                    if ip.find('10.8.') == 0:
                        ips=ips+' vpn:'+ip
                    else:
                        ips=ips+' '+ip
    except:
        logger.warning("get_tap_ip - can't get tap1 ip")
    return str.strip(ips)


def get_device_status(uuid, version_image, version_soft):
    rootfs_stat = os.statvfs("/")
    storagefs_stat = os.statvfs("/mnt/storage")
    mem_stat = get_mem_info()

    data = {
        'systeminfo': {
            'device_uuid': uuid,
            'timestamp': int(time.time()),
            'uname': str(os.uname()),
            'uptime': uptime(),
            'loadaverage1m': int(os.getloadavg()[0] * 100),
            'ifconfig': get_ip(),
            'fs': {
                "root": {
                    "total": rootfs_stat.f_blocks * rootfs_stat.f_bsize,
                    "free": rootfs_stat.f_bavail * rootfs_stat.f_bsize
                },
                "storage": {
                    "total": storagefs_stat.f_blocks * storagefs_stat.f_bsize,
                    "free": storagefs_stat.f_bavail * storagefs_stat.f_bsize
                }

            },
            'mem': {
                "total": mem_stat[0],
                "used": mem_stat[0]-mem_stat[1],
                "free": mem_stat[1]
            }
        },
        "softinfo": {
            "version": {
                "image": version_image,
                "soft": version_soft}

        }
    }
    return data


def send_device_status(url,data):
    logger.debug("send_device_status - sending json to url=" + url)
    req = urllib2.Request(url)
    req.add_header('Content-Type', 'application/json')
    json_obj=json.dumps(data)
    logger.debug("send_device_status - json=" + json_obj)
    try:
        response = urllib2.urlopen(req, json_obj)
        s = response.read()
        json_obj=json.loads(s)
    except urllib2.HTTPError as e:
        logger.error("send_device_status - HTTPError: url=" + e.url + " code=" + str(e.code)+" message="+str(e.msg))
        return -1
    except ValueError as e:
        logger.error("send_device_status - ValueError: " + str(e.message))
        return -1
    else:
        if json_obj['result'] != 'successful':
            logger.warning("send_device_status - response: " + json_obj['message'])
            return -1
        logger.info("send_device_status completed succesfully")
    return 0

logger = logging.getLogger('portal.device_status')
