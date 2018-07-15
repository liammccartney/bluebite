#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Connection
    ==========
    Sqlalchemy Connection management
"""

from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import Session


class PostgreSQLConnection(object):
    """
        A PostgreSQL database connection

        Note: applications that use this class will need to include the
        psycopg2 package in their path, as the SDK does not include it.

    """

    #: stores the SQLAlchemy engine
    _engine = None
    #: stores the cached session
    _session = None
    #: stores the current session scope
    _session_scope = None
    #: stores the context depth of the SQL Alchemy session
    _session_context_depth = 0


    def __init__(self, user, password, # pylint: disable=too-many-arguments
                 host, db_name):
        """ Stores connection details """

        self.user = user
        self.password = password
        self.host = host
        self.db_name = db_name


    @property
    def uri(self):
        return 'postgresql+psycopg2://%s:%s@%s/%s' % (self.user,
                                                      self.password,
                                                      self.host,
                                                      self.db_name)

    @contextmanager
    def session(self):
        """
        A context manager that yields a SQLAlchemy scoped_session. The
        session is "scoped" to nested calls of this method, such that if
        `session` is called within another `session` call, they will execute
        within the same session. Once the outermost context manager closes,
        that shared session is cleaned up, and any subsequent calls will be
        executed within a new scope.
        """
        if not self._session:
            self._build_session()
        session = self._session
        self._session_context_depth += 1
        try:
            yield session
        finally:
            self._session_context_depth -= 1
            if self._session_context_depth < 1:
                self._clear_connection()

    def _build_session(self):
        """ Construct a new session, bound to the engine """
        if not self._engine:
            self._build_engine()
        self._session = Session(bind=self._engine,
                                autoflush=False,
                                autocommit=False)

    def _build_engine(self):
        """ Construct a SQLAlchemy engine.
        """
        self._engine = create_engine(self.uri)

    def _clear_connection(self):
        """ Resets the session scope to a new unique identifier """
        if self._session:
            self._session.close()
            self._session = None
        if self._engine:
            #  See http://docs.sqlalchemy.org/en/latest/core/connections.html#engine-disposal
            self._engine.dispose()
            self._engine = None
