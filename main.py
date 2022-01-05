#!/usr/bin/env python3

import sys
import os
import boto3
import time

def check_kms (key: str):
    """Check for the existence of a KMS key"""

    check_key = KMS.describe_key(
        KeyId=key,
    )

    return check_key["KeyMetadata"]["KeyId"]

def create_kms_key():
    """ Create a KMS CMK key and hand the ID back"""

    create_key = KMS.create_key(
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

def check_snapshot(instance: str):
    """ Check for the existence of a database snapshot"""
    check_rds = RDS.describe_db_snapshots(
    DBInstanceIdentifier=f"{instance}",
    DBSnapshotIdentifier=f"snapshot-{instance}",
    )

    return check_rds

def check_snapshot_state(snapshot: str):
    """ Check the state of a snapshot"""
    check_state = RDS.describe_db_snapshots(
        DBInstanceIdentifier=f"{snapshot}",
        DBSnapshotIdentifier=f"snapshot-{snapshot}"
    )

    return check_state["DBSnapshots"][0]["Status"]

def produce_snapshot(instance: str):
    """Create a snapshot of a desired RDS instance, name that snapshot"""

    # Check our snapshot does not already exist
    check = check_snapshot(instance)

    # If the snapshot does not already exist create it
    if check["DBSnapshots"] == []:
        snapshot = RDS.create_db_snapshot(
            DBSnapshotIdentifier=f"snapshot-{instance}",
            DBInstanceIdentifier=instance,
        )
        print("Created base snapshot")
    else:
        # If the snapshot exists notify the user and they can check their AWS snapshots for this
        # DB instance.
        print(f"Snapshot already exists at 'snapshot-{instance}'")
        return None


    # Return the snapshot name from the JSON object held by the snapshot variable
    return snapshot["DBSnapshot"]["DBSnapshotIdentifier"]

def encrypt_snapshot(source_snapshot: str, key: str):
    """Encrypt a existing RDS snapshot"""
        
    encrypt = RDS.copy_db_snapshot(
        SourceDBSnapshotIdentifier=f"{source_snapshot}",
        TargetDBSnapshotIdentifier=f"{source_snapshot}-encrypted",
        KmsKeyId=key,
    )

    print(f"Created encrypted snapshot - {source_snapshot}-encrypted")

    return encrypt

if __name__ == "__main__":
    # Convert the value of our OS level environment variables to python variables

    # Initialize our boto3 endpoints
    RDS = boto3.client('rds')
    KMS = boto3.client('kms')

    # Get the RDS_INSTANCE environment variable from the OS if it does not exist prompt the user to 
    # set it and return exit code 1
    RDS_INSTANCE = os.getenv('RDS_INSTANCE')
    if RDS_INSTANCE == '':
        print("Please set the 'RDS_INSTANCE' environment variable, see README.md")
        sys.exit(1)

    # Get the KMS_KEY environment variable from the OS if it is not set create key for the user
    kms_key = os.getenv('KMS_KEY')
    if kms_key:
        key_existence = check_kms(kms_key)
        if key_existence == '':
            print("Are you sure you have provided the correct key id?")
        else:
            # remove
            print ("I FOUND THE KEY")
    else:
        kms_key = create_kms_key()
        print (f"Created KMS CMK - {kms_key}")

    # Create our initial snapshot
    SNAPSHOT_INSTANCE = produce_snapshot(RDS_INSTANCE)

    # Catch if SNAPSHOT_INSTANCE found the snapshot already existed
    if SNAPSHOT_INSTANCE is None:
        sys.exit(1)

    # Wait for our snapshot to come available
    state = check_snapshot_state(RDS_INSTANCE)
    
    while state == "creating":
        print("Snapshot not ready...")
        time.sleep(20)
        state = check_snapshot_state(RDS_INSTANCE)
    
    ENCRYPT_INSTANCE = encrypt_snapshot(SNAPSHOT_INSTANCE, kms_key)
