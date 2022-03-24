#!/usr/bin/env python3

import unittest
from unittest.mock import Mock
from rds_encrypt import (
    check_encrypted_snapshot_state,
    check_kms,
    check_database,
    check_database_encryption,
    check_snapshot,
    check_snapshot_state,
    encrypt_snapshot,
    produce_snapshot,
    rename_instance,
)

mock = Mock()


class TestClass(unittest.TestCase):

    """main test class for rds_auto_encrypt"""

    @mock.patch("check_kms.check_key", return_value={"KeyMetadata": {"KeyId": "123"}})
    def test_check_kms():
        expected = "123"
        acctual = check_kms("valuse")
        assert expected == acctual

    @mock.patch(
        "check_database.check_instance",
        return_value={"DBInstances": [{"DBInstanceIdentifier": "123"}]},
    )
    def test_check_database():
        expected = "123"
        acctual = check_database("value")
        assert expected == acctual

    @mock.patch(
        "check_database_encryption.check_instance",
        return_value={"DBInstances": [{"StorageEncrypted": "True"}]},
    )
    def test_check_database_encryption():
        expected = "True"
        acctual = check_database_encryption("value")
        assert expected == acctual

    @mock.patch("check_snapshot.check_rds", return_value={"DBSnapshots": "Ture"})
    def test_check_snapshot():
        expected = "True"
        acctual = check_snapshot("value")
        assert expected == acctual

    @mock.patch(
        "check_snapshot_state.check_state",
        return_value={"DBSnapshots": [{"status": "done"}]},
    )
    def test_check_snapshot_state():
        expected = "done"
        acctual = check_snapshot_state("value")
        assert expected == acctual

    @mock.patch(
        "check_encrypted_snapshot_state.check_state",
        return_value={"DBSnapshots": [{"Status": "Done"}]},
    )
    def test_check_encrypted_snapshot_state():
        expected = "Done"
        acctual = check_encrypted_snapshot_state("val")
        assert expected == acctual

    @mock.patch(
        "produce_snapshot.check",
        return_value={"DBSnapshot": {"DBSnapshotIdentifier": "123"}},
    )
    def test_produce_snapshot():
        expected = "123"
        acctual = produce_snapshot("value")
        assert expected == acctual

    @mock.patch(
        "encrypt_snapshot.encrypt",
        return_value={"DBSnapshot": {"DBSnapshotIdentifier": "123"}},
    )
    def test_encrypt_snapshot():
        expected = "123"
        acctual = encrypt_snapshot("value")
        assert expected == acctual

    @mock.patch("rename_instance.instance_new", return_value="new-instance")
    def test_rename_instance():
        expected = "new-instance"
        acctual = rename_instance("value")
        assert expected == acctual
