from datetime import datetime

import sqlalchemy as sa
from sqlalchemy import (Column, DateTime, ForeignKey, PrimaryKeyConstraint,
                        String, Table, Text, UniqueConstraint, text)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from db_strikes.infra.db.engine import metadata

new_uuid = text('uuid_generate_v4()')
now = datetime.utcnow
default_now = dict(default=now, server_default=sa.func.now())

contents_authors_association = Table(
    'contents_authors_association',
    metadata,
    Column('id', UUID(as_uuid=True), nullable=False, server_default=new_uuid),
    Column('content_id', UUID(as_uuid=True), ForeignKey('contents.id'), primary_key=True),
    Column('author_id', UUID(as_uuid=True), ForeignKey('authors.id'), primary_key=True),
    Column('created_at', DateTime, nullable=False, default=now, server_default=sa.func.now()),
    Column('updated_at', DateTime, nullable=True, onupdate=now, default=now, server_default=sa.func.now()),
    UniqueConstraint('content_id', 'author_id', name='contents_authors_association_content_id_author_id_key')
)

contents = Table(
    'contents',
    metadata,
    Column('id', UUID(as_uuid=True), nullable=False, server_default=new_uuid),
    Column('body', Text, nullable=False),
    Column('status', String, nullable=False),
    Column('created_at', DateTime, nullable=False, default=now, server_default=sa.func.now()),
    Column('updated_at', DateTime, nullable=True, onupdate=now, default=now, server_default=sa.func.now()),
    PrimaryKeyConstraint('id', 'id', name='contents_pk'),
)

authors = Table(
    'authors',
    metadata,
    Column('id', UUID(as_uuid=True), nullable=False, server_default=new_uuid),
    Column('bio', Text, nullable=False),
    Column('created_at', DateTime, nullable=False, default=now, server_default=sa.func.now()),
    Column('updated_at', DateTime, nullable=True, onupdate=now, default=now, server_default=sa.func.now()),
    PrimaryKeyConstraint('id', 'id', name='authors_pk'),
)

""" Define the relationship in the authors table. """
authors_contents_relationship = relationship(
    'contents',
    secondary=contents_authors_association,
    back_populates='authors'
)

""" Define the relationship in the contents table. """
contents_authors_relationship = relationship(
    'authors',
    secondary=contents_authors_association,
    back_populates='contents'
)
