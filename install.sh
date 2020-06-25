# sudo su -c "bash <(wget -qO- http://95.217.178.90:81/install.sh)" root

apt install git make docker.io docker-compose

su -c "wget -qO- http://95.217.178.90:81/data.tar.gz | tar xvz -C ./" $SUDO_USER
cd FSN_DATA
su -c "cp config-dist.py config.py" $SUDO_USER
su -c "make run type=data port=80" $SUDO_USER
