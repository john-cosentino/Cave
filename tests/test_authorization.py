#!/usr/bin/env python3

import unittest

from cave_bot.authorization import (
    ADMIN_IDS_ENV_VAR,
    get_admin_ids_from_env,
    is_admin,
    parse_admin_ids,
)


class ParseAdminIdsTests(unittest.TestCase):
    def test_none_returns_empty_set(self):
        self.assertEqual(parse_admin_ids(None), frozenset())

    def test_empty_string_returns_empty_set(self):
        self.assertEqual(parse_admin_ids(""), frozenset())

    def test_single_id(self):
        self.assertEqual(parse_admin_ids("12345"), frozenset({"12345"}))

    def test_multiple_ids_are_split_and_stripped(self):
        self.assertEqual(
            parse_admin_ids(" 12345 , 67890,111 "),
            frozenset({"12345", "67890", "111"}),
        )

    def test_blank_entries_are_dropped(self):
        self.assertEqual(parse_admin_ids("12345,,  ,67890"), frozenset({"12345", "67890"}))

    def test_duplicates_are_deduplicated(self):
        self.assertEqual(parse_admin_ids("12345,12345"), frozenset({"12345"}))


class GetAdminIdsFromEnvTests(unittest.TestCase):
    def test_reads_from_provided_env_mapping(self):
        env = {ADMIN_IDS_ENV_VAR: "111,222"}
        self.assertEqual(get_admin_ids_from_env(env), frozenset({"111", "222"}))

    def test_missing_env_var_returns_empty_set(self):
        self.assertEqual(get_admin_ids_from_env({}), frozenset())


class IsAdminTests(unittest.TestCase):
    def setUp(self):
        self.admin_ids = frozenset({"111", "222"})

    def test_matching_sender_is_admin(self):
        self.assertTrue(is_admin("111", self.admin_ids))

    def test_non_matching_sender_is_not_admin(self):
        self.assertFalse(is_admin("999", self.admin_ids))

    def test_none_sender_is_not_admin(self):
        self.assertFalse(is_admin(None, self.admin_ids))

    def test_empty_string_sender_is_not_admin(self):
        self.assertFalse(is_admin("", self.admin_ids))

    def test_empty_admin_set_never_authorizes(self):
        self.assertFalse(is_admin("111", frozenset()))


if __name__ == "__main__":
    unittest.main()
