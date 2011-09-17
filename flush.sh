rm -rf /home/james/mirror/*
rm -rf /home/james/tmpdev/courier/data/*
rm -rf /home/james/tmpdev/host/data/*

python manage.py reset handle --database default
python manage.py reset handle --database courier
