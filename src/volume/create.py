import subprocess
import re

def create(voldef={},remotehost="localhost"):
    """
Create a volume

If ``remotehost`` is set, volume info will be retrieved from the remote host.
"""
    brickdiv = 1

    if not "name"   in list(voldef.keys()):
        raise KeyError("Volume must have a name")
    if not "bricks" in list(voldef.keys()):
        raise KeyError("Volume must have bricks")

    program = ["/usr/sbin/gluster", 
            "--remote-host=%s" % remotehost, 
            "volume", 
            "create",
            voldef["name"],
            ]
    if "stripe" in list(voldef.keys()):
        stripe = int(voldef["stripe"])
        program.append("stripe")
        program.append(str(stripe))
        brickdiv = stripe
    if "replica" in list(voldef.keys()):
        replica = int(voldef["replica"])
        program.append("replica")
        program.append(str(replica))
        brickdiv = brickdiv * replica
    if "transport" in list(voldef.keys()):
        transport = voldef["transport"] if voldef["transport"] in ("tcp","rdma","tcp,rdma","rdma,tcp") else "tcp"
        program.append("transport")
        program.append(transport)
    if len(voldef["bricks"]) % brickdiv:
        raise KeyError("Invalid brick count. Bricks must be in multiples of %d" % brickdiv)
    [ program.append(x) for x in voldef["bricks"] ]

    response = str(subprocess.check_output(program), encoding="utf8").split("\n")
    success = "Creation of volume %s has been successful. Please start the volume to access data." % voldef["name"]
    if not success in response:
        raise RuntimeError(response)

    return True
