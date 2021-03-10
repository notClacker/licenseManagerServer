mkdir -p /tmp/license
kill -9 $(cat /tmp/license/save_pid.txt)

cd ./server_license_manager
nohup python3 main.py &
echo $! > /tmp/license/save_pid.txt
cd ..

