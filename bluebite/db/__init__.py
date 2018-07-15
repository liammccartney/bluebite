#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Database Models, Connection
"""
# pylint: disable=no-member,invalid-name,too-few-public-methods

from os import environ

from sqlalchemy import Column, Text, text, ForeignKey, Table, MetaData
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID

from bluebite.db.connection import PostgreSQLConnection

UUID_FUNC = text('uuid_generate_v4()')

METADATA = MetaData()

CONNECTION = PostgreSQLConnection(user=environ['PG_USER'],
                                  password=environ['PG_PASSWORD'],
                                  host=environ['PG_HOST'],
                                  db_name=environ['DB_NAME'])


class _Base(object):
    """ A Base Class with generic functionality """

    session = CONNECTION.session

    def json(self):
        """ A function to serialize the model """
        raise NotImplementedError


BASE = declarative_base(metadata=METADATA, cls=_Base)


class Tag(BASE):
    """ Tag """

    __tablename__ = 'tag'

    id = Column(UUID, primary_key=True, server_default=UUID_FUNC)
    vendor_id = Column(UUID, index=True)
    meta = relationship('Meta', back_populates='tag')

    @classmethod
    def save_tags_and_meta(cls, vendor_id, tags):
        """ Saves a Vendor's Tags and their Meta to the db """
        with cls.session() as session:
            for tag in tags:
                Tag(id=tag['tag_id'], vendor_id=vendor_id).save()

                for meta in tag['metadata']:
                    Meta(tag_id=tag['tag_id'],
                         key=meta['key'],
                         value=meta['value']).save()
            session.commit()

    def save(self):
        """ Upserts a Tag """
        with self.session() as session:
            tag = session.query(Tag).filter_by(id=self.id)
            if tag.count():
                tag.update(self.json())
            else:
                session.add(self)

    def json(self, include_meta=False):
        """ Returns a serializable representation of the a Tag """
        serialized = {
            'id': self.id,
            'vendor_id': self.vendor_id,
        }

        if include_meta:
            serialized['meta'] = [meta.json() for meta in self.meta]

        return serialized


class Meta(BASE):
    """ Meta """

    __tablename__ = 'meta'

    tag_id = Column(UUID, ForeignKey('tag.id'), primary_key=True)
    key = Column(Text, primary_key=True)
    value = Column(Text, index=True)
    tag = relationship('Tag', back_populates='meta')

    @classmethod
    def find_tags(cls, query):
        """ Finds a Meta instances and returns related Tags """
        with cls.session() as session:
            metas = session.query(cls).filter_by(key=query['key'],
                                                 value=query['value'])

            return [meta.tag.json(include_meta=True) for meta in metas]

    def save(self):
        """ Upserts a Meta instance """
        with self.session() as session:
            meta = session.query(Meta).filter_by(tag_id=self.tag_id,
                                                 key=self.key)
            if meta.count():
                meta.update(self.json())
            else:
                session.add(self)

    def json(self):
        """ Returns a serializable representation of a Meta"""
        return {
            'tag_id': self.tag_id,
            'key': self.key,
            'value': self.value
        }
