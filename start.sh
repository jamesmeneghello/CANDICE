sudo sh ./newset.sh
python redirect_server.py > redirect.log &
python content_server.py > content.log &
sudo twistd --logfile=http_server.log --pidfile=http_server.pid -ny http_server.py &
