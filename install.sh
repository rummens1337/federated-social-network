# TEAM F Project Software Engineering
# Installs a dataserver
# Compatable with Linux
# Tested on ubuntu 18.04 and higher
# 
# To run directly: 
# sudo su -c "bash <(wget -qO- http://95.217.178.90:81/install.sh)" root

# Install dependencies
apt install git make docker.io docker-compose

# Download the data server
su -c "wget -qO- http://95.217.178.90:81/data.tar.gz | tar xvz -C ./" $SUDO_USER
cd FSN_DATA
su -c "cp config-dist.py config.py" $SUDO_USER

# Set the config.py with the chosen password
set_config() {
    su -c "sed -i 's/password/$1/g' config.py" $SUDO_USER;
}

# Let the user chooose a mysql password.
echo "Choose a mysql password:";
while true; do
    read -s -p "Password: " password;

    if [ "$password" = "" ]; then
        echo "Password can not be empty";
        continue;
    fi;

    echo "";
    read -s -p "Password again: " password2;
    echo "";
    if [ "$password" = "$password2" ]; then
        break;
    fi;
    echo "Passwords do not match";
done

set_config $password;

# Ask if the user wants to start the data server right away
while true; do
    read -p "Do you wish to start the dataserver?" yn
    case $yn in
        [Yy]* ) su -c "make run-prod type=data port=80" $SUDO_USER; break;;
        [Nn]* ) echo 'To start run: make run-prod type=data port=80'; echo '  in the FSN_DATA folder.'; exit;;
        * ) echo "Please answer yes or no.";;
    esac
done