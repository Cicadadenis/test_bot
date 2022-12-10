apt update -y
apt upgrade -y
apt install python3.9 -y
apt install python3-pip -y
apt install screen -y
pip3 install -r requirements.txt
screen -S bot ./start.sh
