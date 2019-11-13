#!/bin/sh
echo 'Start webservice'
lxc-copy -e -B overlay -n webapp

echo 'Start loadbalancer'
lxc-start -n loadbalancer

echo 'Start scalingcontroller'
python3 ./scalingcontroller/scalingcontroller.py #Name has to be changed!!!

# The scalingcontroller should lookup the ip of the initial webapp,
# overwrite the haproxy.cfg and restart haproxy.
# I think this way we can best assure a good startup.