import shlex
import subprocess
import os
import sys
import time
import logging


def start_aria_daemon(cmd):
    args = shlex.split(cmd)
    try:
        subprocess.Popen(args, shell=False)
        time.sleep(1)
        pid = get_pid_by_name("aria2c")
    except OSError as e:
        logger.error("start_aria_daemon: " + e.message)
    return pid


def write_aria_pid(pid_file, pid):
    try:
        f = open(pid_file, 'w')
        f.write(str(pid))
    except IOError as e:
        logger.error("write_aria_pid: I/O error({0}): {1}".format(e.errno, e.strerror))
    except:
        logger.error("write_aria_pid: Unexpected error:", sys.exc_info()[0])
    finally:
        logger.info("write_aria_pid: " +  str(pid))
        f.close()


def read_aria_pid(pid_file):
    s=""
    try:
        f = open(pid_file, 'r')
        s = f.read()
        pid = int(s)
    except IOError as e:
        logger.error("read_aria_pid: I/O error({0}): {1}".format(e.errno, e.strerror))
    except:
        logger.error("read_aria_pid: Unexpected error:", sys.exc_info()[0])
    finally:
        logger.info("read_aria_pid: " + s)
        f.close()
    return pid


def if_aria_running(pid_file):
    if os.path.isfile(pid_file):
        pid = read_aria_pid(pid_file)
        if check_pid(pid):
            return pid
    return 0


def get_pid_by_name(name):
    pid = 0
    try:
        pid = int(subprocess.check_output(["pgrep", "-n", "-x", name]))
    except subprocess.CalledProcessError as e:
        logger.error("get_pid_by_name: subprocess.CalledProcessError: cmd="+str(e.cmd)+" code="+str(e.returncode))
    return pid


def check_pid(pid):
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    else:
        return True


def main(aria_cmd, aria_pidfile):
    aria_pid = if_aria_running(aria_pidfile)
    if aria_pid > 0:
        logger.info("aria2c is already running pid=" + str(aria_pid))
    else:
        logger.info( "aria2c is not running! Starting aria2c daemon: " + aria_cmd)
        aria_pid = start_aria_daemon(aria_cmd)
        logger.debug( "aria2c pid=" + str(aria_pid) + " in file: " + aria_pidfile)
        write_aria_pid(aria_pidfile, aria_pid)


if __name__ == "__main__":
    main()


logger = logging.getLogger('aria.daemon')
