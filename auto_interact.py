#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import pexpect
from time import sleep
from datetime import datetime

sendkey_key = {}


sendkey_key[48] = "0"
sendkey_key[49] = "1"
sendkey_key[50] = "2"
sendkey_key[51] = "3"
sendkey_key[52] = "4"
sendkey_key[53] = "5"
sendkey_key[54] = "6"
sendkey_key[55] = "7"
sendkey_key[56] = "8"
sendkey_key[57] = "9"
sendkey_key[65] = "shift-a"
sendkey_key[66] = "shift-b"
sendkey_key[67] = "shift-c"
sendkey_key[68] = "shift-d"
sendkey_key[69] = "shift-e"
sendkey_key[70] = "shift-f"
sendkey_key[71] = "shift-g"
sendkey_key[72] = "shift-h"
sendkey_key[73] = "shift-i"
sendkey_key[74] = "shift-j"
sendkey_key[75] = "shift-k"
sendkey_key[76] = "shift-l"
sendkey_key[77] = "shift-m"
sendkey_key[78] = "shift-n"
sendkey_key[79] = "shift-o"
sendkey_key[80] = "shift-p"
sendkey_key[81] = "shift-q"
sendkey_key[82] = "shift-r"
sendkey_key[83] = "shift-s"
sendkey_key[84] = "shift-t"
sendkey_key[85] = "shift-u"
sendkey_key[86] = "shift-v"
sendkey_key[87] = "shift-w"
sendkey_key[88] = "shift-x"
sendkey_key[89] = "shift-y"
sendkey_key[90] = "shift-z"
sendkey_key[97] = "a"
sendkey_key[98] = "b"
sendkey_key[99] = "c"
sendkey_key[100] = "d"
sendkey_key[101] = "e"
sendkey_key[102] = "f"
sendkey_key[103] = "g"
sendkey_key[104] = "h"
sendkey_key[105] = "i"
sendkey_key[106] = "j"
sendkey_key[107] = "k"
sendkey_key[108] = "l"
sendkey_key[109] = "m"
sendkey_key[110] = "n"
sendkey_key[111] = "o"
sendkey_key[112] = "p"
sendkey_key[113] = "q"
sendkey_key[114] = "r"
sendkey_key[115] = "s"
sendkey_key[116] = "t"
sendkey_key[117] = "u"
sendkey_key[118] = "v"
sendkey_key[119] = "w"
sendkey_key[120] = "x"
sendkey_key[121] = "y"
sendkey_key[122] = "z"
sendkey_key[33] = "shift-1"
sendkey_key[35] = "shift-3"
sendkey_key[34] = "shift-apostrophe"
sendkey_key[37] = "shift-5"
sendkey_key[36] = "shift-4"
sendkey_key[39] = "apostrophe"
sendkey_key[38] = "shift-7"
sendkey_key[41] = "shift-0"
sendkey_key[40] = "shift-9"
sendkey_key[43] = "shift-equal"
sendkey_key[42] = "shift-8"
sendkey_key[45] = "minus"
sendkey_key[44] = "comma"
sendkey_key[47] = "slash"
sendkey_key[46] = "dot"
sendkey_key[59] = "semicolon"
sendkey_key[58] = "shift-semicolon"
sendkey_key[61] = "equal"
sendkey_key[60] = "shift-comma"
sendkey_key[63] = "shift-slash"
sendkey_key[62] = "shift-dot"
sendkey_key[64] = "shift-2"
sendkey_key[91] = "bracket_left"
sendkey_key[93] = "bracket_right"
sendkey_key[92] = "backslash"
sendkey_key[95] = "shift-minus"
sendkey_key[94] = "shift-6"
sendkey_key[123] = "shift-bracket_left"
sendkey_key[125] = "shift-bracket_right"
sendkey_key[124] = "shift-backslash"
sendkey_key[32] = "spc"
#96 is shift-(childa)
sendkey_key[96] = "grave_accent"
#126 is ~ (childa)
sendkey_key[126] = "shift-grave_accent"


args = sys.argv

cmdfile = args[1]
malware_list = args[2]
record_duration = args[3]
qemu_conf = args[4]



cmds = []
with open(cmdfile, 'rb') as f:
    lines = f.readlines()
    lines = [x.rstrip() for x in lines]
    lines = [x.decode() for x in lines]
    for line in lines:
        cmds.append(line)

malsamples = []
with open(malware_list, 'rb') as f:
    lines = f.readlines()
    lines = [x.rstrip() for x in lines]
    lines = [x.decode() for x in lines]
    for line in lines:
        if line[0] == "#":
            continue
        malsamples.append(line)

qemu_conf_list = []
with open(qemu_conf, 'rb') as f:
    lines = f.readlines()
    lines = [x.rstrip() for x in lines]
    lines = [x.decode() for x in lines]
    for line in lines:
        qemu_conf_list.append(line)

qemu_cmdline = qemu_conf_list[0]
snapshot_name = qemu_conf_list[1]

child = pexpect.spawn(qemu_cmdline)
child.logfile_read = sys.stdout.buffer



def sendkey_os_command(cmd_str):

    for ch in cmd_str:
        child.expect("(qemu)")
        key = sendkey_key[ ord(ch) ]
        qemu_cmd_str = "sendkey {} 30\n".format(key)
        child.sendline(qemu_cmd_str)

    child.expect("(qemu)")
    child.sendline("sendkey kp_enter\n")




def loadvm_snapshot():
    print("loadvm snapshot!!")
    child.expect("(qemu)")
    sleep(2)
    child.sendline("loadvm {}".format(snapshot_name))




def run_procedures(malware_exec_filename):

    loadvm_snapshot()

    for cmd in cmds:
        if cmd[0] == "#":
            continue

        cmd = cmd.replace("<FILENAME>", malware_exec_filename)
        datetime_now = datetime.now().strftime("%Y%m%d_%I%M%S")
        cmd = cmd.replace("<DATETIME>", datetime_now)

        cmd_args = cmd.split(" ")
        cmd_arg0 = cmd_args[0]
        

        if cmd_arg0 == "begin_record":
            child.expect("(qemu)")
            child.sendline(cmd + "\n")
            child.sendline("\n")
        elif cmd_arg0 == "end_record":
            child.expect("(qemu)")
            sleep(int(record_duration))
            child.sendline(cmd + "\n")
            child.sendline("\n")
        elif cmd_arg0 == "quit":
            child.expect("(qemu)")
            child.sendline(cmd + "\n")
            child.sendline("\n")
        elif cmd_arg0 == "<WAIT>":
            child.expect("(qemu)")
            sleep(20)
            child.sendline("\n")
        else:
            child.expect("(qemu)")
            print("\nSleeping..\n")
            sleep(7)
            child.sendline("\n")
            sendkey_os_command(cmd)

def main():

    for mal in malsamples:
        sleep(2)
        run_procedures(mal)


    sleep(10)

    loadvm_snapshot()

    child.expect("(qemu)")
    sleep(2)
    child.sendline("quit\n")
    child.sendline("\n")



if __name__ == "__main__":
    pass
    main()

