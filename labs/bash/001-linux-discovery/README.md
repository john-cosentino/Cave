# Lab 001: Linux Discovery Commands

## Objective

Practice basic Linux commands used to identify where you are, what system you are on, and what resources are available.

This lab is meant to build the habit of observing a system before changing anything.

## Commands Practiced

- whoami
- hostname
- pwd
- ls -la
- uname -a
- cat /etc/os-release
- df -h
- free -h
- ip addr
- ip route
- ps aux

## Questions to Answer
### Answers can be found in results/linux-discovery-DATE-VER.txt files
- What user am I running as? vscode
- What system am I on? codespaces-cbc367
- What OS is this? Ubuntu 26.04 LTS
- What directory am I currently in? /workspaces/Cave/labs/bash/001-linux-discovery
- What storage is available? /workspaces has about 28g free
- What memory is available? 7.8g
- What network interfaces exist?
  - ``  ### ip addr
        1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
            link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
            inet 127.0.0.1/8 scope host lo
               valid_lft forever preferred_lft forever
            inet6 ::1/128 scope host 
               valid_lft forever preferred_lft forever
        2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP group default qlen 1000
            link/ether 00:22:48:1e:b2:9b brd ff:ff:ff:ff:ff:ff
            inet 10.0.1.33/16 metric 100 brd 10.0.255.255 scope global eth0
               valid_lft forever preferred_lft forever
            inet6 fe80::222:48ff:fe1e:b29b/64 scope link proto kernel_ll 
               valid_lft forever preferred_lft forever
        3: docker0: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc noqueue state DOWN group default 
            link/ether 02:42:1d:2d:69:7e brd ff:ff:ff:ff:ff:ff
            inet 172.17.0.1/16 brd 172.17.255.255 scope global docker0
               valid_lft forever preferred_lft forever
            inet6 fe80::42:1dff:fe2d:697e/64 scope link proto kernel_ll 
               valid_lft forever preferred_lft forever
        ``
- What is the default route?
  - ``  ### ip route
        default via 10.0.0.1 dev eth0 proto dhcp src 10.0.1.33 metric 100 
        10.0.0.0/16 dev eth0 proto kernel scope link src 10.0.1.33 metric 100 
        10.0.0.1 dev eth0 proto dhcp scope link src 10.0.1.33 metric 100 
        168.63.129.16 via 10.0.0.1 dev eth0 proto dhcp src 10.0.1.33 metric 100 
        169.254.169.254 via 10.0.0.1 dev eth0 proto dhcp src 10.0.1.33 metric 100 
        172.17.0.0/16 dev docker0 proto kernel scope link src 172.17.0.1 linkdown
    `` 
- What processes are running? vscode and other related subprocesses
- Which commands behave differently in Codespaces than they would on a full Linux server?

## Results Summary

Fill this in after running `run.sh`.

- User:
- Hostname:
- OS:
- Current directory:
- Available disk:
- Available memory:
- Network notes:
- Process notes:

## What I Learned

Write 3-5 bullets here after completing the lab.

## Follow-up Questions

Write any questions this lab raises.
