#!/bin/bash

pip3 --user install -U instabot
wget "https://github.com/impshum/InstaSpam/archive/master.zip"
unzip master.zip
mkdir ~/data
mv -v ~/InstaSpam-master/* ~/
rm -r ~/InstaSpam-master/
rm ~/master.zip ~/install.sh
clear
echo "STEP #1 - Enter your InstaSpam login details"
python3 run.py -c
echo "STEP #2 - Enter all your posts into posts.txt"
echo "STEP #3 - Go back to the dashboard and set a task to run this script"
