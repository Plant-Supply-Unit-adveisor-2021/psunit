#!/bin/sh

PURP='\033[0;35m'
RED='\033[0;31m'
NC='\033[0m'

printf "${RED}This scripts needs to be run with root priviledges!${NC}\n"
printf "${PURP}Adding measuring, pushing and watering to cron ...${NC}\n" 

echo "\n# psunit stuff" >> /etc/crontab
echo "0,15,30,45 * * * * pi   /usr/bin/python3 ${PWD}/measure.py > ${PWD}/../psunit_data/measure.log 2>&1" >> /etc/crontab
echo "2,17,32,47 * * * * pi   /usr/bin/python3 ${PWD}/push.py > ${PWD}/../psunit_data/push.log 2>&1" >> /etc/crontab
echo "* * * * * pi   /usr/bin/python3 ${PWD}/water.py > ${PWD}/../psunit_data/water.log 2>&1" >> /etc/crontab

printf "${PURP}Adding GUI service ...${NC}\n"

echo "[Unit]\nDescription=Service to host the GUI of the Plant Supply Unit" > /etc/systemd/system/psunit_gui.service
echo "[Service]\nType=simple\nUser=pi" >> /etc/systemd/system/psunit_gui.service
echo "ExecStart=/usr/bin/python3 ${PWD}/userinterface.py" >> /etc/systemd/system/psunit_gui.service
echo "[Install]\nWantedBy=multi-user.target" >> /etc/systemd/system/psunit_gui.service

printf "${PURP}Enabling and Starting GUI service (psunit_gui.service) ...${NC}\n"

systemctl enable psunit_gui.service
systemctl start psunit_gui.service
