#!/usr/bin/env python3
import os
import boto3

def produce_snapshot(instance):
    """Create a snapshot of a desired RDS instance, name that snapshot"""

    # Check our snapshot does not already exist


    # If the snapshot does not already exist create it
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


if __name__ == "__main__":
    
    # Convert the value of our OS level environment variables to python variables
    rds_instance = os.getenv('RDS_INSTANCE')
    user_kms_key = os.getenv('KMS_KEY')

    # Check the user has configured their environment variables
    if user_kms_key == "":
        user_kms_key = "SCRIPT-KEY"
    if rds_instance == "":
        print("Please set the environment variable $RDS_INSTANCE")
        

    # Initialize our boto3 endpoints
    rds = boto3.client('rds')
    kms = boto3.client('kms')

    produce_snapshot(rds_instance)



