import sqlalchemy
import sqlalchemy.orm

import threading

# TODO: from farado.items.field_kind import FieldKind
from farado.items.field import Field
from farado.items.file import File
# TODO: from farado.items.issue_kind import IssueKind
from farado.items.issue import Issue
from farado.items.project import Project
from farado.items.user import User



class MetaItemManager:
    def __init__(self, database_connection_string):
        self.engine = sqlalchemy.create_engine(database_connection_string)
        self.metadata = sqlalchemy.MetaData()
        self.create_tables()
        self.map_tables()
        self.metadata.create_all(self.engine)
        self.mutex = threading.RLock()

    def create_tables(self):
        self.projects_table = sqlalchemy.Table('projects'
            , self.metadata
            , sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True)
            , sqlalchemy.Column('caption', sqlalchemy.String)
            , sqlalchemy.Column('content', sqlalchemy.String)
        )

        self.issues_table = sqlalchemy.Table('issues'
            , self.metadata
            , sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True)
            , sqlalchemy.Column('issuekind_id', sqlalchemy.Integer)
            , sqlalchemy.Column('parent_id', sqlalchemy.ForeignKey('issues.id'), index=True)
            , sqlalchemy.Column('project_id', sqlalchemy.ForeignKey('projects.id'), index=True)
            , sqlalchemy.Column('caption', sqlalchemy.String)
            , sqlalchemy.Column('content', sqlalchemy.String)
        )

        self.fields_table = sqlalchemy.Table('fields'
            , self.metadata
            , sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True)
            , sqlalchemy.Column('issue_id',
                sqlalchemy.ForeignKey('issues.id', ondelete="CASCADE"), index=True)
            , sqlalchemy.Column('fieldkind_id', sqlalchemy.Integer)
            , sqlalchemy.Column('value', sqlalchemy.String)
        )

        self.files_table = sqlalchemy.Table('files'
            , self.metadata
            , sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True)
            , sqlalchemy.Column('issue_id',
                sqlalchemy.ForeignKey('issues.id', ondelete="CASCADE"), index=True)
            , sqlalchemy.Column('caption', sqlalchemy.String)
            , sqlalchemy.Column('name', sqlalchemy.String)
            , sqlalchemy.Column('path', sqlalchemy.String)
            , sqlalchemy.Column('description', sqlalchemy.String)
        )

        self.users_table = sqlalchemy.Table('users'
            , self.metadata
            , sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True)
            , sqlalchemy.Column('login', sqlalchemy.String)
            , sqlalchemy.Column('first_name', sqlalchemy.String)
            , sqlalchemy.Column('middle_name', sqlalchemy.String)
            , sqlalchemy.Column('last_name', sqlalchemy.String)
            , sqlalchemy.Column('email', sqlalchemy.String)
            , sqlalchemy.Column('password_hash', sqlalchemy.String)
            , sqlalchemy.Column('need_change_password', sqlalchemy.Boolean)
            , sqlalchemy.Column('more_info', sqlalchemy.String)
            , sqlalchemy.Column('is_blocked', sqlalchemy.Boolean)
        )


    def map_tables(self):
        sqlalchemy.orm.mapper(Project, self.projects_table,
            properties={
                'issues': sqlalchemy.orm.relationship(
                    Issue,
                    lazy='noload')
                }
            )
        sqlalchemy.orm.mapper(Issue, self.issues_table,
            properties={
                'fields': sqlalchemy.orm.relationship(
                    Field,
                    cascade='all,delete',
                    backref="issue",
                    lazy='immediate')
                , 'files': sqlalchemy.orm.relationship(
                    File,
                    cascade='all,delete',
                    backref="file",
                    lazy='immediate')
                , 'children': sqlalchemy.orm.relationship(
                    Issue,
                    lazy='noload')
                }
            )
        sqlalchemy.orm.mapper(Field, self.fields_table)
        sqlalchemy.orm.mapper(File, self.files_table)
        sqlalchemy.orm.mapper(User, self.users_table)


    def add_item(self, item):
        with self.mutex:
            with sqlalchemy.orm.Session(self.engine) as session, session.begin():
                session.add(item)

    def add_items(self, items):
        with self.mutex:
            with sqlalchemy.orm.Session(self.engine) as session, session.begin():
                session.add_all(items)

    def delete_item_by_id(self, item_type, id):
        with self.mutex:
            with sqlalchemy.orm.Session(self.engine) as session, session.begin():
                item = session.get(item_type, id)
                session.delete(item)

    def expunge_item(self, item):
        with self.mutex:
            with sqlalchemy.orm.Session(self.engine) as session, session.begin():
                session.expunge(item)

    def expunge_items(self, items):
        with self.mutex:
            with sqlalchemy.orm.Session(self.engine) as session, session.begin():
                for item in items:
                    session.expunge(item)

    def merge_item(self, item):
        with self.mutex:
            with sqlalchemy.orm.Session(self.engine) as session, session.begin():
                session.merge(item)

    def item_by_id(self, item_type, id):
        with self.mutex:
            with sqlalchemy.orm.Session(self.engine) as session:
                statement = sqlalchemy.select(item_type).filter_by(id=id)
                return session.execute(statement).scalars().first()

    def item_by_value(self, item_type, value_name, value):
        with self.mutex:
            with sqlalchemy.orm.Session(self.engine) as session:
                statement = sqlalchemy.select(item_type)
                statement = eval(f"statement.filter_by({value_name}=value)")
                return session.execute(statement).scalars().first()

    def items_ids(self, item_type):
        with self.mutex:
            with sqlalchemy.orm.Session(self.engine) as session:
                statement = sqlalchemy.select(item_type.id)
                return [id[0] for id in session.execute(statement).all()]

    def issues_by_field(self, value, fieldkind_id=None):
        with self.mutex:
            with sqlalchemy.orm.Session(self.engine) as session:
                query = session.query(Issue).join(Field).where(Field.value == value)
                if not fieldkind_id:
                    return query.all()

                return query.where(Field.fieldkind_id == fieldkind_id).all()

    def subissues_by_id(self, id):
        with self.mutex:
            with sqlalchemy.orm.Session(self.engine) as session:
                return session.query(Issue).where(Issue.parent_id == id).all()