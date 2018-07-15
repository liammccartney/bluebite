#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Validation
    ==========
    Payload Validation

"""

import os
from os.path import join
from contextlib import contextmanager
import json

from jsonschema import validate as json_validate

SCHEMAS = join(os.path.dirname(os.path.realpath(__file__)), 'schemas')


@contextmanager
def payload_schema(filename):
    """ A context manager for loading a json schema for validation """

    with open(join(SCHEMAS, filename), 'r') as schema_file:
        yield json.load(schema_file)


def validate(payload, schema_file):
    """ Validates a payload against a schema """

    with payload_schema(schema_file) as schema:
        json_validate(payload, schema)


def format_error(validation_error):
    """ Formats a validation error as a dictionary """
    path = list(validation_error.path)
    instance = dict(validation_error.instance)
    reason = validation_error.message
    return {
        'path': path,
        'instance': instance,
        'reason': reason,
        'message': '%s at %s is invalid because %s' %
                   (instance, path, reason)
    }
