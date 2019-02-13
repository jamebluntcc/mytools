sudo yum install -y python-setuptools
sudo easy_install pip
sudo pip install shadowsocks

sudo mkdir /etc/shadowsocks
sudo vim /etc/shadowsocks/config.json

sudo /bin/ssserver -c /etc/shadowsocks/config.json -d start # 启动
sudo /bin/ssserver -c /etc/shadowsocks/config.json -d stop # 关闭
sudo /bin/ssserver -c /etc/shadowsocks/config.json -d restart # 重启
