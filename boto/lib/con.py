import boto
import os
import json
from configparser import ConfigParser
import time

from boto.ec2.connection import EC2Connection
from boto.ec2.regioninfo import *

class Con:
    def __init__(self):
        self.proj_prefix = os.environ['PROJECT_PREFIX']
        f = open(os.path.expanduser(os.environ["{}_AWS_KEY_FILE".format(self.proj_prefix)]), 'r')
        credentials = json.loads(f.read())
        f.close()
        region = None
        if os.environ['EC2_PROVIDER'] == 'AWS':
            region = RegionInfo(name="ap-southeast-2", endpoint="ec2.ap-southeast-2.amazonaws.com")
            self.conn = boto.connect_ec2(
                aws_access_key_id=credentials["access_key"],
                aws_secret_access_key=credentials["secret_key"],
                is_secure=True,
                region=region)
        else:
            region = RegionInfo(name="NeCTAR", endpoint="nova.rc.nectar.org.au")
            self.conn = boto.connect_ec2(
                aws_access_key_id=credentials["access_key"],
                aws_secret_access_key=credentials["secret_key"],
                port=8773,
                is_secure=True,
                path="/services/Cloud",
                region=region)

    # Print images with information
    def print_image_info(self):
        imgs = self.conn.get_all_images()
        for x in imgs:
            print(x.id)
            print(x.architecture)
            print(x.type)
            print(x.name)
            print(x.tags)
        print("-----------")


