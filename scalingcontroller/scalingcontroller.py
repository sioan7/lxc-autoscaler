import os
import lxc
from pyhaproxy.parse import Parser
from pyhaproxy.render import Render
import pyhaproxy
import time

# sudo apt-get install python3-lxc
# pip3 install pyhaproxy

haproxy_config_path = "/srv/haproxyconfig/haproxy.cfg"
loadbalancer_container = lxc.Container("loadbalancer")

containers = []

def start_webapp_container():
    output = os.popen("lxc-copy -e -B overlay -n webapp").read()
    container = lxc.Container(output.split()[1])
    ipv4 = container.get_ips(timeout = 5000)[0]
    print(f"{container.name} at {ipv4}")
    return container

def refresh_loadbalancer():
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
    containers.append(first_container)
    refresh_loadbalancer()
    for container in containers:
        container.stop()
