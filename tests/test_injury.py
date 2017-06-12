#!/usr/bin/env python
import unittest
import requests_mock
import requests
import json
from datetime import datetime
import dateutil.parser
from mlbgame import injury

class TestInjury(unittest.TestCase):
    def setUp(self):
        base_url = 'http://mlb.mlb.com'
        self.injury_url = '%s/fantasylookup/json/named.wsfb_news_injury.bam' % base_url
        self.injury_file = 'tests/files/injury.json'
        with open(self.injury_file) as json_data:
            self.injury_json = json.load(json_data)
            json_data.close()

    def tearDown(self):
        del self.injury_url
        del self.injury_file
        del self.injury_json

    def test_team_id_is_str(self):
        team_id = 117
        i = injury.Injury(team_id)
        self.assertIsInstance(i.team_id, str)

    def test_injury_url(self):
        team_id = 117
        i = injury.Injury(team_id)
        self.assertEqual(i.injury_url, self.injury_url)

    def test_injury_is_list(self):
        team_id = 117
        i = injury.Injury(team_id)
        self.assertIsInstance(i.injuries, list)

    @requests_mock.Mocker()
    def test_injury_json(self, requests_mock):
        requests_mock.get(self.injury_url, json=self.injury_json)
        team_id = 117
        i = injury.Injury(team_id)
        self.assertEqual(i.injury_json, self.injury_json)

    @requests_mock.Mocker()
    def test_last_update(self, requests_mock):
        requests_mock.get(self.injury_url, json=self.injury_json)
        team_id = 117
        i = injury.Injury(team_id)
        last_update = self.injury_json['wsfb_news_injury']['queryResults']['created']
        self.assertEqual(dateutil.parser.parse(last_update), i.last_update)