#!/usr/bin/env python3

import unittest
from unittest.mock import Mock
from rds_encrypt import (
    check_kms,
    check_database,
    check_database_encryption,
    check_snapshot,
    encrypt_snapshot,
    produce_snapshot,
    rename_instance,
)

mock = Mock()


class TestClass(unittest.TestCase):

    """main test class for rds_auto_encrypt"""

    @mock.patch("check_kms.check_key", return_value={"KeyMetadata": {"KeyId": "123"}})
    def test_check_kms(self):
        expected = "123"
        actual = check_kms("valuse")
        assert expected == actual

    @mock.patch(
        "check_database.check_instance",
        return_value={"DBInstances": [{"DBInstanceIdentifier": "123"}]},
    )
    def test_check_database(self):
        expected = "123"
        actual = check_database("value")
        assert expected == actual

    @mock.patch(
        "check_database_encryption.check_instance",
        return_value={"DBInstances": [{"StorageEncrypted": "True"}]},
    )
    def test_check_database_encryption(self):
        expected = "True"
        actual = check_database_encryption("value")
        assert expected == actual

    @mock.patch("check_snapshot.check_rds", return_value={"DBSnapshots": "Ture"})
    def test_check_snapshot(self):
        expected = "True"
        actual = check_snapshot("value")
        assert expected == actual

    @mock.patch(
        "produce_snapshot.check",
        return_value={"DBSnapshot": {"DBSnapshotIdentifier": "123"}},
    )
    def test_produce_snapshot(self):
        expected = "123"
        actual = produce_snapshot("value")
        assert expected == actual

    @mock.patch(
        "encrypt_snapshot.encrypt",
        return_value={"DBSnapshot": {"DBSnapshotIdentifier": "123"}},
    )
    def test_encrypt_snapshot(self):
        expected = "123"
        actual = encrypt_snapshot("value")
        assert expected == actual

    @mock.patch("rename_instance.instance_new", return_value="new-instance")
    def test_rename_instance(self):
        expected = "new-instance"
        actual = rename_instance("value")
        assert expected == actual
