#!/usr/bin/env python3
"""
Unit tests for GithubOrgClient.org
"""

import unittest
from unittest.mock import patch
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Test suite for GithubOrgClient"""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.utils.get_json")  # Adjust if get_json is in utils
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org calls get_json correctly"""
        expected_url = f"https://api.github.com/orgs/{org_name}"
        expected_payload = {"login": org_name, "id": 123}
        mock_get_json.return_value = expected_payload

        client = GithubOrgClient(org_name)
        self.assertEqual(client.org, expected_payload)
        mock_get_json.assert_called_once_with(expected_url)

    @patch("client.utils.get_json")
    def test_org_api_error(self, mock_get_json):
        """Test GithubOrgClient.org handles API errors"""
        mock_get_json.side_effect = ValueError("API error")
        client = GithubOrgClient("google")
        with self.assertRaises(ValueError):
            _ = client.org