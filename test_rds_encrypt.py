#!/usr/bin/env python3

import unittest
from unittest.mock import Mock
from rds_encrypt import check_kms

mock = Mock()


class TestClass(unittest.TestCase):

    """main test class for rds_auto_encrypt"""


    @mock.patch(
        "check_kms.check_key", return_value={"KeyMetadata": {"KeyId": "123"}}
    )
    def test_check_kms():
        expected = "123"
        acctual = check_kms(expected)
        assert expected == acctual

    # def test_check_database():
    #     pass

    # def test_remove_db():
    #     pass

    # def test_check_database_encryption():
    #     pass

    # def test_check_snapshot():
    #     pass

    # def test_check_snapshot_state():
    #     pass

    # def test_check_encrypted_snapshot_state():
    #     pass

    # def test_produce_snapshot():
    #     pass

    # def test_encrypt_snapshot():
    #     pass

    # def test_rename_instance():
    #     pass

    # def test_restore_from_encrypted_snapshot():
    #     pass
