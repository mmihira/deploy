import boto
import os
import json
import sys, paramiko
from lib.con import Con
from lib.ec2 import Ec2

from boto.ec2.connection import EC2Connection
from boto.ec2.regioninfo import *
import asyncio
import concurrent.futures

conn = Con().conn
ec2 = Ec2(conn)
instances = ec2.current_non_term_tagged_instances()
proj_prefix = os.environ['PROJECT_PREFIX']

ssh_config = paramiko.SSHConfig()
user_config_file = os.path.expanduser(os.environ[ "{}_SEVERS_SSH_CONFIG".format(proj_prefix) ])
if os.path.exists(user_config_file):
    with open(user_config_file) as f:
        ssh_config.parse(f)

host_names = ssh_config.get_hostnames()
host_by_ip = {}
for host_name in host_names:
    host  = ssh_config.lookup(host_name)
    host_by_ip[host['hostname']] = host

loop = asyncio.get_event_loop()
executor = concurrent.futures.ThreadPoolExecutor(max_workers=30)

def client_work(inst):
    print("Waiting for initial installation for {}".format(inst))
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ip_address = None
    if os.environ['EC2_PROVIDER'] == 'AWS':
        ip_address =  inst.ip_address
    else:
        ip_address =  inst.private_ip_address

    client.connect(ip_address,
                   port=22,
                   username=host_by_ip[str(ip_address)]['user'],
                   key_filename=host_by_ip[str(ip_address)]['identityfile'][0])
    sftp = client.open_sftp()
    sftp.put('./scripts/init.sh', '/tmp/init.sh')
    sftp.close()
    stdin, stdout, stderr = client.exec_command('chmod u+x /tmp/init.sh')
    exit_status = stdout.channel.recv_exit_status()
    stdin, stdout, stderr = client.exec_command('/tmp/init.sh')
    exit_status = stdout.channel.recv_exit_status()
    print("Installation done : {}".format(inst))
    client.close()
    return client

async def init_install(inst):
    try:
        await loop.run_in_executor(executor, client_work, inst)
    except Exception as e:
        print("Exception! : {}".format(e))
        return await asyncio.sleep(0, result=False)

g = asyncio.gather(*[init_install(inst) for inst in instances])
loop.run_until_complete(g)
loop.close()
