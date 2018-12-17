import boto
import os
import json
import sys, paramiko
from lib.con import Con
from lib.ec2 import Ec2

from boto.ec2.connection import EC2Connection
from boto.ec2.regioninfo import *
import asyncio

conn = Con().conn
ec2 = Ec2(conn)
instances = ec2.current_non_term_tagged_instances()
volumes = ec2.volumes()
proj_prefix = os.environ['PROJECT_PREFIX']

print("All instance :", instances)
print("All volumes :", volumes)

