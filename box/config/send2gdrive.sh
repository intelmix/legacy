#!/bin/sh
# based on https://gist.github.com/deanet/3427090
# usage: send2grdive /home/mahdi/file1 
#           will upload this file to my google drive
# useful $HOME/.gdrive.conf options:
#    curl_args="--limit-rate 500K --progress-bar"


browser="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36"
username="mahdix@gmail.com"
password="petwqdheaioruwth" #ghnixtobmwrjlnbs"  #app specific password
accountype="HOSTED"
destination_folder_id="0B8w8d54uQa8MQ3FaS0Y3NVZSLWc"

if [ -e $HOME/.gdrive.conf ]
then
    . $HOME/.gdrive.conf
fi

old_umask=`umask`
umask 0077

if [ -z "$username" ]
then
    read -p "username: " username
    unset token
    echo "username=$username" >> $HOME/.gdrive.conf
fi

if [ -z "$account_type" ]
then
    if expr "$username" : '^[^@]*$' > /dev/null || expr "$username" : '.*@gmail.com$' > /dev/null
    then
        account_type=GOOGLE
    else
        account_type=HOSTED
    fi
fi

if [ -z "$password$token" ]
then
    read -s -p "password: " password
    unset token
    echo
fi


if [ -z "$token" ]
then
    
    token=`curl --silent --data-urlencode Email=$username --data-urlencode Passwd="$password" --data accountType=$account_type --data service=writely --data source=cURL "https://www.google.com/accounts/ClientLogin" | sed -ne s/Auth=//p`
    sed -ie '/^token=/d' $HOME/.gdrive.conf
    echo "token=$token" >> $HOME/.gdrive.conf
fi
umask $old_umask

for file in "$@"
do
    slug=`basename "$file"`
    mime_type=`file --brief --mime-type "$file"`
    upload_link=`curl --silent --show-error --insecure --request POST --header "Content-Length: 0" --header "Authorization: GoogleLogin auth=${token}" --header "GData-Version: 3.0" --header "Content-Type: $mime_type" --header "Slug: $slug" "https://docs.google.com/feeds/upload/create-session/default/private/full${destination_folder_id+/folder:$destination_folder_id/contents}?convert=false" --dump-header - | sed -ne s/"Location: "//p | tr -d '\r\n'`
    
    echo "$file:"
    curl -g -v --request POST --output /dev/null --data-binary "@$file" --header "Authorization: GoogleLogin auth=${token}" --header "GData-Version: 3.0" --header "Content-Type: $mime_type" --header "Slug: $slug" "$upload_link"




        
done
