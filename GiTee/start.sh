# 打印到日志文件中，文件名为log+时间戳.log
# 用法：./start.sh
# 作者：leigao6
# 解开main.py第三行、第四行的注释
sed -i '3,4s/^# //' main.py
# 211行IP替换为Linux服务器IP
sed -i 's/127.0.0.1/172.30.94.147/g' main.py
# 后台运行，输出到日志文件中
nohup python3 -u main.py > log`date +%s`.log 2>&1 &