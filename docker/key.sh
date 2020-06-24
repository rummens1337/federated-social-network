if [ ! -e "jwtRS256.key" ]; then
       ssh-keygen -t rsa -b 4096 -m PEM -f jwtRS256.key -q -N ""
       openssl rsa -in jwtRS256.key -pubout -outform PEM -out jwtRS256.key.pub
fi