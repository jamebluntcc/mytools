from dh.klicen.com/ops-base:v1.0
env wd=/data/ops-backend-eta
add . ${wd} 
workdir ${wd}
run rm -f conf.local.json && mkdir /etc/supervisor && mkdir -p /var/log/supervisor
volume /var/log/
copy conf/supervisor/ops-backend-eta-dev.conf /etc/supervisord.conf
entrypoint ["supervisord", "-n", "-c", "/etc/supervisord.conf"]




