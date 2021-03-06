# 2015-11-27

version_image=10
version_soft=3

uuid="498543d5-1f22-4682-a4fb-b1a42a1bcfff" #prod
#uuid="13cab633-7c94-471c-918a-2fa2991aa3fe"  #dev
token="0dcb49b33a09b9ddee431067c7d3b249"

cesclient_home_dir="/opt/cesclient"
cesclient_conf_dir=cesclient_home_dir+"/conf"
cesclient_cache_dir="/mnt/storage/cesclient-cache"
cesclient_log_dir=cesclient_cache_dir+"/logs"
cesclient_log_config=cesclient_conf_dir+"/logging.conf"

user_dir="/mnt/storage/cesbox/portal"
download_dir=cesclient_cache_dir+"/downloads"
download_dir_ready=download_dir + "/ready"

aria_bin="/opt/cesclient/aria2c"
aria_token="Qwerty12"
aria_conf_path=cesclient_conf_dir+"/aria2c.conf"
aria_daemon_on_complete=cesclient_home_dir+"/python/aria_on_complete.py"
aria_cmd = aria_bin +" --rpc-secret="+aria_token+" -d "+download_dir+" --on-download-complete="+aria_daemon_on_complete + " --conf-path="+aria_conf_path
aria_pidfile = cesclient_log_dir +'/aria2c.pid'
aria_rpc_url="http://localhost:6800/jsonrpc"

portal_url="http://terra-media.ru"
#portal_url="http://10.1.100.233"
portal_url_api_getqueue=portal_url+"/api/get_queue?uuid="+uuid+"&token="+token
portal_url_api_device_status=portal_url+"/api/set_device_status?uuid="+uuid+"&token="+token
portal_url_api_download_status=portal_url+"/api/set_download_status?uuid="+uuid+"&token="+token

