#!/usr/bin/env python3

import sys
import os
import boto3
import time

def check_kms(key: str):
    """Check for the existence of a KMS key. """

    check_key = KMS.describe_key(
        KeyId=key,
    )

    return check_key["KeyMetadata"]["KeyId"]

def check_database(database: str):
    """Check for the existence of the RDS instance. """

    check_instance = RDS.describe_db_instances(
    DBInstanceIdentifier=database,
    )

    return check_instance["DBInstances"][0]["DBInstanceIdentifier"]

def check_snapshot(instance: str):
    """ Check for the existence of a database snapshot. """

    check_rds = RDS.describe_db_snapshots(
    DBInstanceIdentifier=f"{instance}",
    DBSnapshotIdentifier=f"snapshot-{instance}",
    )

    return check_rds

def check_snapshot_state(snapshot: str, ):
    """Check the state of a snapshot. """

    check_state = RDS.describe_db_snapshots(
        DBInstanceIdentifier=f"{snapshot}",
        DBSnapshotIdentifier=f"snapshot-{snapshot}"
    )

    return check_state["DBSnapshots"][0]["Status"]

def check_encrypted_snapshot_state(snapshot: str, ):
    """Check the state of a snapshot. """

    check_state = RDS.describe_db_snapshots(
        DBInstanceIdentifier=f"{snapshot}",
        DBSnapshotIdentifier=f"encrypted-snapshot-{snapshot}"
    )

    return check_state["DBSnapshots"][0]["Status"]


def produce_snapshot(instance: str):
    """Create a snapshot of a desired RDS instance, name that snapshot. """

    # Check our snapshot does not already exist
    check = check_snapshot(instance)

    # If the snapshot does not already exist create it
    if check["DBSnapshots"] == []:
        snapshot = RDS.create_db_snapshot(
            DBSnapshotIdentifier=f"snapshot-{instance}",
            DBInstanceIdentifier=instance,
        )
        print(f"Creating snapshot - snapshot-{instance}")
    else:
        # If the snapshot exists notify the user and they can check their AWS snapshots for this
        # DB instance.
        print(f"Snapshot already exists at 'snapshot-{instance}'")
        return None


    # Return the snapshot name from the JSON object held by the snapshot variable
    return snapshot["DBSnapshot"]["DBSnapshotIdentifier"]

def encrypt_snapshot(source_snapshot: str, key: str):
    """Encrypt an existing RDS snapshot. """
        
    encrypt = RDS.copy_db_snapshot(
        SourceDBSnapshotIdentifier=f"{source_snapshot}",
        TargetDBSnapshotIdentifier=f"encrypted-{source_snapshot}",
        KmsKeyId=key,
    )

    print(f"Creating encrypted snapshot - encrypted-{source_snapshot}")

    return encrypt

if __name__ == "__main__":

    # Initialize our boto3 endpoints
    RDS = boto3.client('rds')
    KMS = boto3.client('kms')

    # Get the RDS_INSTANCE environment variable from the OS if it does not exist prompt the user to 
    # set it and return exit code 1
    RDS_INSTANCE = os.getenv('RDS_INSTANCE')
    if RDS_INSTANCE:
        rds_existence = check_database(RDS_INSTANCE)
        if rds_existence == None:
            print("Please set the 'RDS_INSTANCE' environment variable, see README.md")
            sys.exit(1)
    else:
        print("Please set the 'RDS_INSTANCE' environment variable, see README.md")


    # Get the KMS_KEY environment variable from the OS and check that the key exists
    kms_key = os.getenv('KMS_KEY')
    if kms_key:
        key_existence = check_kms(kms_key)
        if key_existence == None:
            print("Please set the 'KMS_KEY' environment variable, see README.md")
            sys.exit(1)
    else:
        print("Please set the 'KMS_KEY' environment variable, see README.md")

    # Create our initial snapshot
    SNAPSHOT_INSTANCE = produce_snapshot(RDS_INSTANCE)

    # Catch if SNAPSHOT_INSTANCE found the snapshot already existed
    if SNAPSHOT_INSTANCE is None:
        sys.exit(1)

    # Wait for our snapshot to come available
    base_snapshot_state = check_snapshot_state(RDS_INSTANCE)
    
    while base_snapshot_state == "creating":
        print("\t - Snapshot not ready...")
        time.sleep(20)
        base_snapshot_state = check_snapshot_state(RDS_INSTANCE)
    print("Snapshot finished")

    # Encrypt our snapshot by passing in our base snapshot and encryption key
    encrypt_snapshot(SNAPSHOT_INSTANCE, kms_key)

    # Wait for our encrypted snapshot to be created. 
    encrypted_snapshot_state = check_encrypted_snapshot_state(RDS_INSTANCE)
    while encrypted_snapshot_state == "creating":
        print("\t -Encrypted snapshot not ready...")
        time.sleep(20)
        encrypted_snapshot_state = check_encrypted_snapshot_state(RDS_INSTANCE)
    print("Snapshot finished")
    







