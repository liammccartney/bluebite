#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Test Validation
    ===============
    Tests for the Validation module
"""

import os
from os.path import join
import json

from jsonschema import ValidationError
import pytest

from bluebite.validation import validate

PAYLOADS = join(os.path.dirname(os.path.realpath(__file__)), 'json_payloads')

VALID_PAYLOADS = [
    '7447156584c543658455558747c64d2c',
    '5d207da03b0040578e4c5160597357b7',
    'a3e3853750724e2994515bb70d646c32'
]

INVALID_PAYLOAD = '995c3f51ebd7486695d8947152bb38d3'

def _payload(key):
    """ Loads payload for validation """
    with open(join(PAYLOADS, '%s.json' % key), 'r') as payload_json:
        return json.load(payload_json)


def test_valid():
    """ Tests validate raises no error if a payload is valid """
    for payload_key in VALID_PAYLOADS:
        assert validate(_payload(payload_key), 'command.json') is None

def test_invalid():
    """ Tests validate raises a validation error if a payload is invalid """
    with pytest.raises(ValidationError):
        validate(_payload(INVALID_PAYLOAD), 'command.json')
