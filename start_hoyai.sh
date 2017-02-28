
#!/bin/bash
# Get a carriage return into `cr`

cr=`echo $'\n.'`
cr=${cr%.}
if [ "$#" -eq 0 ]; then
   echo "Usage: bash start_hoyai.sh <1,2,3>"
   echo "                  1 : start django"
   echo "                  2 : start postgres"
   echo "                  3 : restart postgres"
   echo "                  4 : stop postgres"
   exit 1
fi

type="$1"
if [ "$type" = "1" ]; then
  
  echo "Stoping Django"
  
  kill $(ps aux | grep 'manage.py'|grep -v grep| awk '{print $2}')

  echo "Starting Django"
  


   python /home/dev/hoyai/manage.py makemigrations 
   python /home/dev/hoyai/manage.py migrate 
   python /home/dev/hoyai/manage.py runserver $HOSTNAME:8888 &
fi
if [ "$type" = "2" ]; then
  echo "Starting postgres"
  sudo -u postgres /usr/lib/postgresql/9.6/bin/pg_ctl start -D /var/lib/postgresql/9.6/main
fi
if [ "$type" = "3" ]; then
  echo "restart postgres"
  sudo -u postgres /usr/lib/postgresql/9.6/bin/pg_ctl reload -D /var/lib/postgresql/9.6/main
fi
if [ "$type" = "4" ]; then
  echo "stop postgres"
  sudo -u postgres /usr/lib/postgresql/9.6/bin/pg_ctl stop -D /var/lib/postgresql/9.6/main
fi
