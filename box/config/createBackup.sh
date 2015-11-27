#!/bin/sh
PATH=/usr/local/bin:/usr/bin:/bin
datepart=`date +%Y-%m-%d-%H-%M`
sqlfilename=/tmp/sqlbackup_$datepart.zip
mysqldump -u live_user -pykstr_thisislive_#$%_ --databases live_yeksatr | gzip > $sqlfilename
./send2gdrive.sh $sqlfilename
rm $sqlfilename
