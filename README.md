# Tamer: A sandbox for IoT malware analysis

## Summary

Tamer is a sandbox to execute a malware executable in a controlled environment and perform malware analysis.

## Components

- ```tamer.sh``` launches sandbox and execute a malware executables that are listed in an external config file.

- ```auto_interact.py``` is a tool to interact with QEMU using ```expect```. So, it requires ```pexpect```. The applicable usage of ```expect``` for our purpose is based on the demo in this [video link](https://youtu.be/kdWX0ZWo_8o).

- ```setup_network_config.py``` performs network settings to make a closed and controlled network environment adapted for malware analysis. (It uses ```iptables``` and make settings around linux virtual bridges using ```brctl``` and TUN/TAP interfaces.)

- ```malware_repo.py``` is a http server program where a sandbox requests and downloads a malware sample to be analyzed.



## Usage

To start analysis, execute as follows.

```
./tamer.sh analyzed_samples/mirai_md5.txt <IP-address of malware repository's server>
```

Note that the sandbox launches virtual machines on QEMU. Since the size of qcow2 images is large, contact [us](<mailto:yonamine.shun.yl6@is.naist.jp>) if request the images that we built. Note that the sandbox launches virtual machines on QEMU. Since the size of qcow2 images is large, contact us if request the images that we built. Of course, it will be okay to use your own qcow2 images and combine with ``auto_interact.py``.

## Use case 

### Case 1. Getting syscall logs for all samples in a dataset

This use case can be seen in the demo in this [video link](https://youtu.be/OfKhdMzeMpA).


As a simple use case, it automate to perform all steps (download samples, launch syscall monitoring, run malware) to perform dynamic malware analysis.

 As a result, it allows to perform analyzing invoked syscalls on a lot of samples in an automated manner.

![Perform dynamic analysis on Mirai](./docs/images/screen_01.png)



## Dataset

In ```analyzed_samples```, it will contain details and a list of md5 hash of malware samples that we analyzed as a dataset.
