#!/usr/bin/env python3
import os
import boto3

rds_instance = os.getenv('RDS_INSTANCE')
user_kms_key = os.getenv('KMS_KEY')

if user_kms_key == "":
    user_kms_key = " bla bla bla"
    

if rds_instance == "":
    print("Please set the enviroment variable $RDS_INSTANCE")
    

rds = boto3.client('rds')
kms = boto3.client('kms')

def produce_snapshot(instance):
    """Create a snapshot of a desired RDS instance, name that snapshot"""

    snapshot = rds.create_db_snapshot(
        DBSnapshotIdentifier=f"snapshot-{instance}",
        DBInstanceIdentifier= instance,
    )

    return snapshot


def encrypt_snapshot(source_snapshot):
    """Encrypt a existing RDS snapshot"""

    encrypt = rds.copy_db_snapshot(
        SourceDBSnapshotIdentifier=source_snapshot,
        TargetDBSnapshotIdentifier=f"encrypted-{source_snapshot}",
        KmsKeyId="",
        CopyTags=True,
        OptionGroupName='string',
        TargetCustomAvailabilityZone='string',
        SourceRegion='string',
    )
    
    return encrypt


