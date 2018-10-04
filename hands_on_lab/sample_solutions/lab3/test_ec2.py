#!/bin/env python 
import sys 
import os
import boto3 
import botocore
from botocore.exceptions import ClientError
import string 
import moto 
from moto import mock_ec2

#working from ec2 user
ec2 = boto3.resource('ec2', 'us-west-2', aws_access_key_id="", aws_secret_access_key="")


#tests using moto from here


#tests making an ec2 instance with the make_instance function
@mock_ec2
def test_new_instance():
    make_instance()
    client = boto3.client('ec2',region_name='us-west-2')
    instances = client.describe_instances()['Reservations'][0]['Instances']
    assert len(instances) == 1
    instance1 = instances[0]
    assert instance1['ImageId'] == 'ami-4e700e36'


#tests whether an instance is terminated after calling terminate_instances
@mock_ec2
def test_delete_instance():
   #tempec2 = boto3.resource('ec2')
   
   print("==============")
   #because data is not persistent between moto tests, reimplement test_new_instance
   checkID = make_instance()

   list_instances()
   print("==============")
   print ("checking to see if checkID exists: " + checkID)
  
   terminate_instances(checkID)
   
   for instance1 in ec2.instances.all(): 
        if checkID == instance1.id:
            #wired together weirdly but it works kind of 
            stateChecker = str(instance1.state)
            print('instance state: ' + stateChecker)
            assert stateChecker == "{\'Code\': 48, \'Name\': \'terminated\'}" or stateChecker == "{\'Name\': \'terminated\', \'Code\': 48}"
