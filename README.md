# tools
Share some tools to improve work effeciency.

>>分享一些常用工具，改善工作效率。

1.wol_tool.py

  This is for waking LAN PC that supports WOL feature.(How to config that? Plz google it.)

>>这个工具主要用来唤醒局域网内支持WOL功能的电脑，可以用一直工作的树莓派唤醒局域网内其他休眠的机器。

2.dns_ip_update.py
  这个是用来更新域名解析记录的工具，因为外网IP经常变化，需要定期更新域名。记得首先要安装tencent cloud python包。
  pip install qcloudapi-sdk-python
  可以简单的加到计划任务中，例如：
  1.sudo crontab -e
  2.选择vi
  3.30 12 * * * python /home/pi/workshop/tools/dns_ip_update.py
  每天12点30分更新一次ip,本地会cache一次ip地址，所以，如果地址没有变化，不会请求更新服务器，减少被服务器拒绝的可能。可以根据需要增加频率。
