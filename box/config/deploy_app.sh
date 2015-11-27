#!/bin/bash

#1 - backup live folder

svnc="$1" 
currentVersion=$(echo $svnc | grep -o -P "(?<=\().*(?=-)")
newVersion=$(echo $svnc | grep -o -P "(?<=>).*(?=\))")
filename=/srv/backup/live/$(echo $currentVersion)_src_backup.zip

zip -r $filename /srv/main/app/live/src
#==========================
#2 - Backup live db schema

export dbFile=/srv/backup/live/$(echo $currentVersion)_db_backup.zip
mysqldump -u root -pykstr_thisisroot_#$%_ --databases live_yeksatr | gzip > $dbFile
#=================================
#3 - tag svn 

svn copy --username mahdi --password 1198yeksatr_srv_svn --non-interactive  svn://107.150.21.195/dev/yeksatr svn://107.150.21.195/dev/tags/$(echo $newVersion) -m "Tag for $(echo $newVersion)"
#=================================
#4 - svn export on live folder

svn export svn://107.150.21.195/dev/yeksatr /srv/main/app/live/src/yeksatr --force
#=================================
#5 - reload uwsgi


uwsgi --reload /srv/main/app/live/src/yeksatr/pid_5678.pid
