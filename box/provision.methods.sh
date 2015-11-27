#TODO: store everything in SVN/GIT and just a simple one line script to checkout 
#and run the provisioning bootstrapper script
#!/usr/bin/env bash
SVN_IP=107.150.21.195
HOST_DOMAIN=yeksatr.io
CFG_PATH="/vagrant" #by default config files are stored in vagrant shared directory
IS_STANDALONE=0
IS_VERBOSE=0

function echo_start {
    echo "> $1...Starting"
}

function echo_done {
    echo "> $1...Done"
}

function echo_section {
    echo ">>> $1"
}

function cleanup_system {
    echo_start "clean-up"
    apt-get -q -y autoclean > /dev/null
    apt-get -q -y autoremove > /dev/null
    echo_done "clean-up"
}

function init_system {
    echo_start "init"
    printf "nameserver 4.2.2.4\nnameserver 10.0.2.3\n" > /etc/resolv.conf
    export DEBIAN_FRONTEND=noninteractive
    echo "deb http://ftp.au.debian.org/debian testing main contrib" >> /etc/apt/sources.list
    
    #repeat three times due to some network issues 
    if [[ $IS_VERBOSE == 0 ]] 
    then
        apt-get update > /dev/null
        apt-get update > /dev/null
        apt-get update --fix-missing > /dev/null
    else
        apt-get update
        apt-get update
        apt-get update --fix-missing
    fi
     
    echo_done "init"
}

function install_py_packages {
    pip3_install  uWSGI 2.0.9
    pip_install supervisor 3.1.3
    pip3_install PyMySQL 0.6.2
    pip3_install Chameleon 2.16
    pip3_install pyramid 1.5.1
    pip3_install pyramid-chameleon 0.3
    pip3_install pyramid-debugtoolbar 2.2
    pip3_install MarkupSafe 0.23
    pip3_install PasteDeploy 1.5.2
    pip3_install beautifulsoup4 4.3.2
    #pip3_install feedparser 5.1.3    
    pip3_install html5lib 0.999
    pip3_install peewee 2.3.3
    pip3_install requests 2.4.3
    pip3_install six 1.8.0
    pip3_install pygments 2.0.1
    pip3_install WebOb 1.4    
    #pip3_install mysql-python 1.2.5 has no py3 version
}

function install_sys_packages {
    apt_get_install bsdutils
    apt_get_install chkconfig
    apt_get_install lynx
    apt_get_install curl
    #pip sometimes complains about crypto??.so
    apt_get_install libssl1.0.0
    #apt_get_install -q -y emacs24-nox > /dev/null
    apt_get_install gcc
    apt_get_install g++
    apt_get_install build-essential    
    apt_get_install nginx
    apt_get_install mysql-server
    apt_get_install python3.4
    apt_get_install python3.4-dev
    apt_get_install python3-pip
    apt_get_install python2.7
    apt_get_install python-pip
    apt_get_install ufw
    apt_get_install mytop
}

function svn_checkout {
    echo_start "svn checkout"
    mkdir -p /srv/main
    cd /srv/main
        
    #do not checkout svn in a standalone (non-vagrant) server
    #we will handle the deployment using out svn web tool
    if [[ $IS_STANDALONE == 0 ]]
    then
        apt_get_install subversion
        svn checkout svn://$SVN_IP/dev/yeksatr
        echo_done "svn checkout"
    else
        echo "svn checkout ignored in standalone mode"
    fi
    
    
}

function setup_firewall {
    echo_start "firewall setup"
    ufw default deny incoming
    ufw default allow outgoing
    ufw allow 22   #ssh
    ufw allow 6915
    ufw allow 80   #nginx
    ufw allow 9001 #supervisord
    ufw allow 3306 #mysql
    ufw --force enable
    echo_done "firewall setup"
}

function start_services {
    echo_start "service start"
    service cron restart
    service nginx restart
    service mysql restart
    service supervisord start
    echo_done "service start"
}

function config_system {
    echo_start "configure system"

    cd ~
    ln -s -f $CFG_PATH/config/.bashrc .bashrc
    ln -s -f $CFG_PATH/config/.bashrc .bash_profile

    cd /etc/ssh
    ln -s -f $CFG_PATH/config/sshd_config

    cd /etc
    ln -s -f $CFG_PATH/config/supervisord.conf

    cd /etc/init.d
    ln -s -f $CFG_PATH/config/supervisord
    chmod +x /etc/init.d/supervisord
    sudo update-rc.d supervisord defaults
    
    cd /etc/nginx
    ln -s -f $CFG_PATH/config/nginx.conf nginx.conf
    ln -s -f $CFG_PATH/config/htpasswd htpasswd
    
    cd /etc/nginx/sites-enabled
    ln -s -f $CFG_PATH/config/yeksatr.site.conf yeksatr.site.conf
    rm default
    service nginx stop
    chkconfig nginx off
    rm /etc/init.d/mysql
    mkdir -p /var/run/mysqld
    chown mysql:mysql /var/run/mysqld
    
    mkdir /var/log/yeksatr
    mkdir /var/uwsgi

    svn_checkout
    
    cd /srv/main/yeksatr
    python3 setup.py develop

    cd /etc/mysql
    ln -s -f $CFG_PATH/config/my.cnf
    
    mysqladmin -u root password 123456
    mysql --user=root --password=123456 < $CFG_PATH/config/database.sql
    service mysql stop
    chkconfig mysql off
    rm /etc/init.d/mysql

    cd /var/spool/cron/crontabs
    ln -s -f $CFG_PATH/config/root.crontab root
    
    if [[ $IS_STANDALONE == 0 ]]
    then
        setup_php
        setup_adminer
    fi
    
    echo_done "configure system"
}

function apt_get_install {
    if [[ $IS_VERBOSE == 0 ]] 
    then
        apt-get install -q -y $1 > /dev/null
    else
        apt-get install -y $1
    fi 
    
    echo_done $1
}

function pip3_install {
    if [[ $IS_VERBOSE == 0 ]] 
    then
        pip3 install -q --download-cache $CFG_PATH/config/cache $1==$2 > /dev/null
    else
        pip3 install --download-cache $CFG_PATH/config/cache $1==$2
    fi 
    
    echo_done $1
}

function pip_install {
    pip install -q --download-cache $CFG_PATH/config/cache $1==$2
    echo_done $1
}

function setup_php() {
    apt_get_install php5-fpm
    apt_get_install php5-mysql
}

function setup_traq() {
    mkdir -p /srv/main/nginx/traq
    cd /tmp
    wget --quiet http://sourceforge.net/projects/traq/files/3.x/traq-3.5.2.tar.gz
    tar xf traq-3.5.2.tar.gz
    cp upload/* /srv/main/nginx/traq -r
    
    cd /etc/nginx/sites-enabled
    ln -s -f $CFG_PATH/config/traq.site.conf
    sed -i "s/yeksatr.io/$HOST_DOMAIN/" traq.site.conf 
}

function setup_adminer() {
    mkdir -p /srv/main/nginx/adminer
    cd /srv/main/nginx/adminer
    
    ln -s -f $CFG_PATH/config/adminer.php adminer.php
    ln -s -f $CFG_PATH/config/adminer.css adminer.css
    
    cd /etc/nginx/sites-enabled
    ln -s -f $CFG_PATH/config/adminer.site.conf
    sed -i "s/yeksatr.io/$HOST_DOMAIN/" adminer.site.conf 
}

function setup_backup_schedule() {
    echo "A"
}
