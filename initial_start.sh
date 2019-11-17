#!/bin/sh

echo 'First webapp will be started by the scalingcontroller!'

echo 'Start loadbalancer'
lxc-start -n loadbalancer

echo 'Start scalingcontroller'
python3 ./scalingcontroller/scalingcontroller.py