#!/usr/bin/env python3

import sys
import random
import os
import boto3


def check_snapshot(instance: str):
    """ Check for the existence of a database snapshot"""
    check_rds = rds.describe_db_snapshots(
    DBInstanceIdentifier=f"{instance}",
    DBSnapshotIdentifier=f"snapshot-{instance}",
    )

    return check_rds

def check_kms (key: str):
    """Check for the existence of a KMS key"""

    return check_kms["KeyMetadata"]["KeyId"]

def create_kms_key(key: str):
    create_key = kms.create_key(
        Description='Auto Created key from rds-encrypt python script',
        KeyUsage='ENCRYPT_DECRYPT',
        KeySpec='RSA_4096',
        Origin='AWS_KMS',
        BypassPolicyLockoutSafetyCheck=False,
        Tags=[
            {
                'TagKey': 'CreatedBy',
                'TagValue': 'rds-encrypt'
            },
        ],
        MultiRegion=False
    )

    return create_key["KeyMetadata"]["KeyId"]

def assign_kms_key_alias(key_id: str, key):
    key_alias = kms.create_alias(
    AliasName='string',
    TargetKeyId='string'
)

def produce_snapshot(instance: str):
    """Create a snapshot of a desired RDS instance, name that snapshot"""

    # Check our snapshot does not already exist
    check = check_snapshot(instance)

    # If the snapshot does not already exist create it
    if check["DBSnapshots"] == []:
        snapshot = rds.create_db_snapshot(
            DBSnapshotIdentifier=f"snapshot-{instance}",
            DBInstanceIdentifier=instance,
        )
    else:
        # If the snapshot exists notify the user and they can check their AWS snapshots for this
        # DB instance.
        return f"Snapshot already exists at 'snapshot-{instance}'"

    # Return the snapshot name from the JSON object held by the snapshot variable
    return snapshot["DBSnapshot"]["DBSnapshotIdentifier"]


def encrypt_snapshot(source_snapshot: str, kms_key: str):
    """Encrypt a existing RDS snapshot"""
        
    encrypt = rds.copy_db_snapshot(
        SourceDBSnapshotIdentifier=source_snapshot,
        TargetDBSnapshotIdentifier=source_snapshot,
        KmsKeyId=,
        Tags=[
            {
                'Key': 'string',
                'Value': 'string'
            },
        ],
        TargetCustomAvailabilityZone='string',
        SourceRegion='string'
    )

    return "bob"


if __name__ == "__main__":
    # Convert the value of our OS level environment variables to python variables

    # Initialize our boto3 endpoints
    rds = boto3.client('rds')
    kms = boto3.client('kms')

    # Get the RDS_INSTANCE environment variable from the OS if it does not exist prompt the user to set it and
    # return exit code 1
    rds_instance = os.getenv('RDS_INSTANCE')
    if rds_instance == '':
        print("Please set the 'RDS_INSTANCE' environment variable, see README.md")
        sys.exit(1)

    # Get the KMS_KEY environment variable from the OS if it is not set, configure it to our default as 
    # specificed in README.md
    kms_key_alias = os.getenv('KMS_KEY_ALIAS')
    if kms_key_alias == '':
        key_alias_suffix =  random.randint(1000, 4000)
        kms_key_alias = f"auto-gen-rds-encrypt-{key_alias_suffix}"
    
    key_existence = check_kms(kms_key_alias)
    if key_existence == '':
        create_kms_key()
        kms_key = assign_kms_key_alias()



    snapshot_instance = produce_snapshot(rds_instance)

    encrypt_instance = encrypt_snapshot(snapshot_instance, kms_key)
