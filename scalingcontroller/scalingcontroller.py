import os
import lxc
from pyhaproxy.parse import Parser
from pyhaproxy.render import Render
import pyhaproxy
import time
import requests

import monitor

# sudo apt-get install python3-lxc
# pip3 install pyhaproxy

haproxy_config_path = "/srv/haproxyconfig/haproxy.cfg"
loadbalancer_container = lxc.Container("loadbalancer")
loadbalancer_ip = loadbalancer_container.get_ips(timeout = 5000)[0]
print(f"{loadbalancer_container.name} @ {loadbalancer_ip}")

containers = []

def start_webapp_container():
    output = os.popen("lxc-copy -e -B overlay -n webapp").read()
    container = lxc.Container(output.split()[1])
    ipv4 = container.get_ips(timeout = 5000)[0]
    print(f"Starting {container.name} @ {ipv4}")
    containers.append(container)
    return container

def refresh_loadbalancer():
    print("Refreshing loadbalancer")
    haproxy_config = Parser(haproxy_config_path).build_configuration()
    webapp_backend = haproxy_config.backend("webapp")
    for server in webapp_backend.servers():
        webapp_backend.remove_server(server.name)
    for container in containers:
        webapp_backend.add_server(pyhaproxy.config.Server(
            name = container.name,
            host = container.get_ips(timeout = 5000)[0],
            port = "5000",
            attributes = ["check"]
        ))
    Render(haproxy_config).dumps_to(haproxy_config_path)
    loadbalancer_container.attach_wait(lxc.attach_run_command, ["/etc/init.d/haproxy", "restart"])


if __name__ == "__main__":
    first_container = start_webapp_container() 
    refresh_loadbalancer()
    while True:
        time.sleep(1)
        print("Wake up and scale...")
        stats = monitor.server_stats(loadbalancer_ip)
        modified = False
        if len(containers) > 1:
            for c in containers:
                if int(stats[c.name]["qcur"]) == 0:
                    print(f"Stopping container {c.name} @ {c.get_ips(timeout = 5000)[0]}")
                    c.stop()
        if int(stats["BACKEND"]["qcur"]) > 10:
            start_webapp_container()
        if modified:
            refresh_loadbalancer()
        
    
