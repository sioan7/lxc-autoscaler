import lxc

for cname in lxc.list_containers():
    c = lxc.Container(cname)
    c.stop()
