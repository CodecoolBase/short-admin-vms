#!/bin/sh -eux
apt-get -y install mininet openvswitch-testcontroller
systemctl stop openvswitch-testcontroller
systemctl disable openvswitch-testcontroller
systemctl enable openvswitch-switch
systemctl start openvswitch-switch
