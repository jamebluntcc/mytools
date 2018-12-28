# 创建文件
sudo vim /etc/yum.repos.d/mongodb-org-4.0.repo

# 配置文件内容如下
# [mongodb-org-4.0]
# name=MongoDB Repository
# baseurl=https://repo.mongodb.org/yum/redhat/$releasever/mongodb-org/4.0/x86_64/
# gpgcheck=1
# enabled=1
# gpgkey=https://www.mongodb.org/static/pgp/server-4.0.asc

# 安装配置
sudo yum install -y mongodb-org
# 数据位置：/var/lib/mongo
# 日志位置：/var/log/mongodb
# 配置文件位置：/etc/mongod.conf

sudo vim /etc/mongod.conf
# 修改net:bindlp: 127.0.0.1 改为 0.0.0.0

# 开放27017端口
sudo semanage port -a -t mongod_port_t -p tcp 27017

# 开启服务
sudo mongod start
# 或者
sudo systemcl start mongod

# 启动客户端
mongo --host 127.0.0.1:27017
