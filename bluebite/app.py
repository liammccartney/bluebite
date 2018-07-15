#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    App
"""
from functools import wraps

from flask import Flask, jsonify, request
from jsonschema import ValidationError

from bluebite.db import Tag, Meta
from bluebite.validation import validate, format_error

app = Flask(__name__)


def ensure_valid_request(schema):
    def decorator(function):
        @wraps(function)
        def function_wrapper():
            try:
                if request.is_json:
                    payload = request.get_json()
                else:
                    payload = request.args

                validate(payload, schema)
                return function()
            except ValidationError as invalid:
                return jsonify({'statusCode': 400,
                                'error': format_error(invalid)}), 400
            except Exception as e:
                return jsonify({'statusCode': 500,
                                'error': e.message}), 500
        return function_wrapper
    return decorator


@app.route('/tag', methods=['POST'])
@ensure_valid_request('command.json')
def tag_route():
    post_tags(request.get_json())
    return jsonify({'statusCode': 204}), 204


@app.route('/query', methods=['GET'])
@ensure_valid_request('query.json')
def query_tags():
    return jsonify({'statusCode': 200,
                    'tags': find_tags(request.args)}), 200


def find_tags(query):
    """ Finds tags by their metadata """
    return Meta.find_tags(query)


def post_tags(vendor_tags):
    """ Save incoming tags to the db """
    Tag.save_tags_and_meta(vendor_tags['vendor_id'], vendor_tags['tags'])
