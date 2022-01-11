#!/bin/sh


if [ -z "$1" ];then
        echo "Set first argument!!"
        exit 1
fi

MALWARE_LIST=$1


if [ -z "$2" ];then
        echo "Set IP address of Malware repository"
        exit 1
fi

MALWARE_REPO_ADDR=$2


ARCH=$3

#COMMAND_LIST="command_list.txt"
#QEMU_CONF="qemu_conf.txt"
QEMU_CONF="./config/qemu_conf_debug.txt"
COMMAND_LIST="./config/command_list_debug.txt"


if [ $ARCH = "ARM" ]; then
    QEMU_CONF="qemu_conf_ARM.txt"
fi


if [ $ARCH = "ARM_UCLIBC" ]; then
    QEMU_CONF="qemu_conf_ARM_uclibc.txt"
    COMMAND_LIST="command_arm_uclibc.txt"
fi

if [ $ARCH = "ARM_STRACE" ]; then
    QEMU_CONF="qemu_conf_ARM_strace.txt"
    COMMAND_LIST="command_list_strace.txt"
fi


if [ $ARCH = "DEBUG" ]; then
    QEMU_CONF="qemu_conf_debug.txt"
    COMMAND_LIST="command_list_debug.txt"
fi


python3 setup_network_config.py $MALWARE_REPO_ADDR


/home/shun/Tools/latest/work20181228/panda-re/build-panda/i386-softmmu/qemu-system-i386 -drive file=/home/shun/Tools/qcow_images/debian912_stretch_i386.qcow2 -m 1024 -monitor stdio -k en-us -netdev tap,ifname=vport2,script=no,downscript=no,id=testmynet0 -device e1000,netdev=testmynet0,mac=52:55:00:d1:55:24 -vnc :2 -loadvm backup_ram1024MB_Activate_CowrieFakedns_running_20210408 &



export HTTPD_PID=$!

sleep 10

python3 auto_interact.py $COMMAND_LIST $MALWARE_LIST 120 $QEMU_CONF $MALWARE_REPO_ADDR
sudo kill -KILL $HTTPD_PID


