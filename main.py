#!/usr/bin/env python3

""" A tool used for encrypting RDS instances that were previously created in an unencrypted state"""

import time
import random
import sys
import os
import boto3

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

def remove_db(instance: str):
    """Removes a DB instance based on identifier"""
    RDS.delete_db_instance(
        DBInstanceIdentifier=instance,
        SkipFinalSnapshot=True|False,
        DeleteAutomatedBackups=False
    )

def check_database_encryption(database: str):
    """Checks if an RDS instance has encrypted storage. """

    check_instance = RDS.describe_db_instances(
        DBInstanceIdentifier=database,
    )

    return check_instance["DBInstances"][0]["StorageEncrypted"]

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
    check = check_snapshot(instance)

    if check["DBSnapshots"] == []:
        snapshot = RDS.create_db_snapshot(
            DBSnapshotIdentifier=f"snapshot-{instance}",
            DBInstanceIdentifier=instance,
        )
        print(f"Creating snapshot - snapshot-{instance}")
    else:
        print(f"Snapshot already exists at 'snapshot-{instance}'")
        return None

    return snapshot["DBSnapshot"]["DBSnapshotIdentifier"]

def encrypt_snapshot(source_snapshot: str, key: str):
    """Encrypt an existing RDS snapshot. """

    encrypt = RDS.copy_db_snapshot(
        SourceDBSnapshotIdentifier=f"{source_snapshot}",
        TargetDBSnapshotIdentifier=f"encrypted-{source_snapshot}",
        KmsKeyId=key,
    )

    print(f"Creating encrypted snapshot - encrypted-{source_snapshot}")
    return encrypt["DBSnapshot"]["DBSnapshotIdentifier"]

def rename_instance(instance: str):
    """Will rename your RDS instance to have a prefix of rds-old-xxxx"""
    random_prefix_int = random.randint(1000, 9999)
    instance_new = f"rds-old-{random_prefix_int}-instance"

    print(f"Renaming instance - {instance_new}")
    rename = RDS.modify_db_instance(
        DBInstanceIdentifier=instance,
        NewDBInstanceIdentifier=instance_new,
        ApplyImmediately=True,
    )

    if rename["DBInstance"]["PendingModifiedValues"]["DBInstanceIdentifier"] != instance_new:
        print(f"Could not rename RDS instance {instance} to {instance_new}")

    update_check = None
    while update_check != instance_new:
        try:
            update_check = check_database(instance_new)
        except:
            print("\t - Rename not complete")
        time.sleep(10)

    print("Rename complete")
    return instance_new

def restore_from_encrypted_snapshot(snapshot: str, instance_name: str):
    """ Restores an RDS instance from a given snapshot"""
    RDS.restore_db_instance_from_db_snapshot(
        DBInstanceIdentifier=instance_name,
        DBSnapshotIdentifier=snapshot,
    )


if __name__ == "__main__":

    # Initialize our boto3 endpoints
    RDS = boto3.client('rds')
    KMS = boto3.client('kms')

    # Get the RDS_INSTANCE environment variable from the OS if it does not exist prompt the user to
    # set it and return exit code 1
    RDS_INSTANCE = os.getenv('RDS_INSTANCE')
    if RDS_INSTANCE:
        RDS_INSTANCE = check_database(RDS_INSTANCE)
        if RDS_INSTANCE is None:
            print("Please set the 'RDS_INSTANCE' environment variable, see README.md")
            sys.exit(1)
    else:
        print("Please set the 'RDS_INSTANCE' environment variable, see README.md")
        sys.exit(1)

    # Get the KMS_KEY environment variable from the OS and check that the key exists
    KMS_KEY = os.getenv('KMS_KEY')
    if KMS_KEY:
        KEY_EXISTENCE = check_kms(KMS_KEY)
        if KEY_EXISTENCE is None:
            print("Please set the 'KMS_KEY' environment variable, see README.md")
            sys.exit(1)
    else:
        print("Please set the 'KMS_KEY' environment variable, see README.md")
        sys.exit(1)

    # Create our initial snapshot
    SNAPSHOT_INSTANCE = produce_snapshot(RDS_INSTANCE)

    # Catch if SNAPSHOT_INSTANCE found the snapshot already existed
    if SNAPSHOT_INSTANCE is None:
        sys.exit(1)

    # Wait for our snapshot to come available
    BASE_SNAPSHOT_STATE = check_snapshot_state(RDS_INSTANCE)
    while BASE_SNAPSHOT_STATE == "creating":
        print("\t - Snapshot not ready...")
        time.sleep(20)
        BASE_SNAPSHOT_STATE = check_snapshot_state(RDS_INSTANCE)
    print("Snapshot finished")

    # Encrypt our snapshot by passing in our base snapshot and encryption key
    ENCRYPTED_SNAPSHOT_IDENTIFIER = encrypt_snapshot(SNAPSHOT_INSTANCE, KMS_KEY)

    # Wait for our encrypted snapshot to be created.
    ENCRYPTED_SNAPSHOT_STATE = check_encrypted_snapshot_state(RDS_INSTANCE)
    while ENCRYPTED_SNAPSHOT_STATE == "creating":
        print("\t - Encrypted snapshot not ready...")
        time.sleep(20)
        ENCRYPTED_SNAPSHOT_STATE = check_encrypted_snapshot_state(RDS_INSTANCE)
    print("Snapshot finished")

    # Renames the original instance RDS-OLD
    OLD_INSTANCE = rename_instance(RDS_INSTANCE)

    # Create a new DB instance from our snapshot
    restore_from_encrypted_snapshot(ENCRYPTED_SNAPSHOT_IDENTIFIER, RDS_INSTANCE)

    # Check we now have a new encrypted instance running under the original identifier
    if check_database_encryption(RDS_INSTANCE):
        print(f"Instance {RDS_INSTANCE} is now encrypted")
        sys.exit(0)

    remove_db(OLD_INSTANCE)
    