import sqlalchemy
import sqlalchemy.orm

import threading

# TODO: from farado.items.field_kind import FieldKind
from farado.items.field import Field
from farado.items.field_kind import FieldKind
from farado.items.file import File
# TODO: from farado.items.issue_kind import IssueKind
from farado.items.issue import Issue
from farado.items.issue_kind import IssueKind
from farado.items.project import Project
from farado.items.user import User
from farado.items.workflow import Workflow
from farado.items.state import State
from farado.items.edge import Edge
from farado.items.role import Role
from farado.items.rule import Rule
from farado.items.user_role import UserRole



class MetaItemManager:
    def __init__(self, database_connection_string):
        self.engine = sqlalchemy.create_engine(database_connection_string)
        self.metadata = sqlalchemy.MetaData()
        self.create_tables()
        self.map_tables()
        self.metadata.create_all(self.engine)
        self.mutex = threading.RLock()
        self.session = sqlalchemy.orm.Session(self.engine)

    def create_tables(self):
        self.projects_table = sqlalchemy.Table('projects'
            , self.metadata
            , sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True)
            , sqlalchemy.Column('caption', sqlalchemy.String)
            , sqlalchemy.Column('content', sqlalchemy.String)
        )

        self.workflows_table = sqlalchemy.Table('workflows'
            , self.metadata
            , sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True)
            , sqlalchemy.Column('caption', sqlalchemy.String)
            , sqlalchemy.Column('description', sqlalchemy.String)
        )

        self.states_table = sqlalchemy.Table('states'
            , self.metadata
            , sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True)
            , sqlalchemy.Column('caption', sqlalchemy.String)
            , sqlalchemy.Column('description', sqlalchemy.String)
            , sqlalchemy.Column('workflow_id',
                sqlalchemy.ForeignKey('workflows.id', ondelete="CASCADE"), index=True)
        )

        self.edges_table = sqlalchemy.Table('edges'
            , self.metadata
            , sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True)
            , sqlalchemy.Column('from_state_id', sqlalchemy.Integer, index=True)
            , sqlalchemy.Column('to_state_id', sqlalchemy.Integer, index=True)
            , sqlalchemy.Column('workflow_id',
                sqlalchemy.ForeignKey('workflows.id', ondelete="CASCADE"), index=True)
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

        self.issue_kinds_table = sqlalchemy.Table('issue_kinds'
            , self.metadata
            , sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True)
            , sqlalchemy.Column('workflow_id', sqlalchemy.ForeignKey('workflows.id'), index=True)
            , sqlalchemy.Column('caption', sqlalchemy.String)
        )

        self.fields_table = sqlalchemy.Table('fields'
            , self.metadata
            , sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True)
            , sqlalchemy.Column('issue_id',
                sqlalchemy.ForeignKey('issues.id', ondelete="CASCADE"), index=True)
            , sqlalchemy.Column('fieldkind_id', sqlalchemy.Integer)
            , sqlalchemy.Column('value', sqlalchemy.String)
        )

        self.field_kinds_table = sqlalchemy.Table('field_kinds'
            , self.metadata
            , sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True)
            , sqlalchemy.Column('issue_kind_id',
                sqlalchemy.ForeignKey('issue_kinds.id', ondelete="CASCADE"), index=True)
            , sqlalchemy.Column('caption', sqlalchemy.String)
            , sqlalchemy.Column('value_type', sqlalchemy.String)
            , sqlalchemy.Column('description', sqlalchemy.String)
            , sqlalchemy.Column('is_system', sqlalchemy.Boolean)
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

        self.roles_table = sqlalchemy.Table('roles'
            , self.metadata
            , sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True)
            , sqlalchemy.Column('caption', sqlalchemy.String)
        )

        self.rules_table = sqlalchemy.Table('rules'
            , self.metadata
            , sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True)
            , sqlalchemy.Column('caption', sqlalchemy.String)
            , sqlalchemy.Column('role_id',
                sqlalchemy.ForeignKey('roles.id', ondelete="CASCADE"), index=True)
            , sqlalchemy.Column('is_admin', sqlalchemy.Boolean)
            , sqlalchemy.Column('project_id', sqlalchemy.ForeignKey('projects.id'), index=True)
            , sqlalchemy.Column('project_rights', sqlalchemy.Integer)
            , sqlalchemy.Column('issue_kind_id', sqlalchemy.ForeignKey('issue_kinds.id'), index=True)
            , sqlalchemy.Column('workflow_id', sqlalchemy.ForeignKey('workflows.id'), index=True)
            , sqlalchemy.Column('issue_rights', sqlalchemy.Integer)
        )

        self.user_roles_table = sqlalchemy.Table('user_roles'
            , self.metadata
            , sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True)
            , sqlalchemy.Column('user_id',
                sqlalchemy.ForeignKey('users.id', ondelete="CASCADE"), index=True)
            , sqlalchemy.Column('role_id',
                sqlalchemy.ForeignKey('roles.id', ondelete="CASCADE"), index=True)
        )

    def map_tables(self):
        sqlalchemy.orm.mapper(Project, self.projects_table,
            properties={
                'issues': sqlalchemy.orm.relationship(
                    Issue,
                    lazy='noload')
                }
            )
        sqlalchemy.orm.mapper(Workflow, self.workflows_table,
            properties={
                'states': sqlalchemy.orm.relationship(
                    State,
                    cascade='all,delete',
                    backref="state_workflow",
                    lazy='immediate'),
                'edges': sqlalchemy.orm.relationship(
                    Edge,
                    cascade='all,delete',
                    backref="edge_workflow",
                    lazy='immediate'),
                'issue_kinds': sqlalchemy.orm.relationship(
                    IssueKind,
                    lazy='noload'),
                }
            )
        sqlalchemy.orm.mapper(State, self.states_table)
        sqlalchemy.orm.mapper(Edge, self.edges_table)
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
                    backref="issue",
                    lazy='immediate')
                , 'children': sqlalchemy.orm.relationship(
                    Issue,
                    lazy='noload')
                }
            )
        sqlalchemy.orm.mapper(IssueKind, self.issue_kinds_table,
            properties={
                'field_kinds': sqlalchemy.orm.relationship(
                    FieldKind,
                    cascade='all,delete',
                    backref="issue_kind",
                    lazy='immediate')
                }
            )
        sqlalchemy.orm.mapper(Field, self.fields_table)
        sqlalchemy.orm.mapper(FieldKind, self.field_kinds_table)
        sqlalchemy.orm.mapper(File, self.files_table)
        sqlalchemy.orm.mapper(User, self.users_table,
            properties={
                'user_roles': sqlalchemy.orm.relationship(
                    UserRole,
                    cascade='all,delete',
                    backref="user",
                    lazy='immediate'),
                }
            )
        sqlalchemy.orm.mapper(Role, self.roles_table,
            properties={
                'rules': sqlalchemy.orm.relationship(
                    Rule,
                    cascade='all,delete',
                    backref="role",
                    lazy='immediate'),
                'user_roles': sqlalchemy.orm.relationship(
                    UserRole,
                    cascade='all,delete',
                    backref="role",
                    lazy='immediate'),
                }
            )
        sqlalchemy.orm.mapper(Rule, self.rules_table)
        sqlalchemy.orm.mapper(UserRole, self.user_roles_table)

    def add_item(self, item):
        with self.mutex:
            with self.session.begin():
                self.session.add(item)
                self.session.flush()
                self.session.refresh(item)
                self.session.expunge_all()

    def add_items(self, items):
        with self.mutex:
            with self.session.begin():
                self.session.add_all(items)
                self.session.flush()
                self.session.refresh(items)
                self.session.expunge_all()

    def delete_item_by_id(self, item_type, id):
        with self.mutex:
            with self.session.begin():
                item = self.session.get(item_type, id)
                self.session.delete(item)

    def merge_item(self, item):
        with self.mutex:
            with self.session.begin():
                self.session.merge(item)
                self.session.expunge_all()

    def items(self, item_type):
        with self.mutex:
            with self.session.begin():
                statement = sqlalchemy.select(item_type)
                result = self.session.execute(statement).scalars().all()
                self.session.expunge_all()
                return result

    def item_by_id(self, item_type, id):
        with self.mutex:
            with self.session.begin():
                statement = sqlalchemy.select(item_type).filter_by(id=id)
                result = self.session.execute(statement).scalars().first()
                self.session.expunge_all()
                return result

    def item_by_value(self, item_type, value_name, value):
        with self.mutex:
            with self.session.begin():
                statement = sqlalchemy.select(item_type)
                statement = eval(f"statement.filter_by({value_name}=value)")
                result = self.session.execute(statement).scalars().first()
                self.session.expunge_all()
                return result

    def items_by_value(self, item_type, value_name, value):
        with self.mutex:
            with self.session.begin():
                statement = sqlalchemy.select(item_type)
                statement = eval(f"statement.filter_by({value_name}=value)")
                result = self.session.execute(statement).scalars().all()
                self.session.expunge_all()
                return result

    def items_ids(self, item_type):
        with self.mutex:
            with self.session.begin():
                statement = sqlalchemy.select(item_type.id)
                return [id[0] for id in self.session.execute(statement).all()]

    def issues_by_field(self, value, fieldkind_id=None):
        with self.mutex:
            with self.session.begin():
                query = self.session.query(Issue).join(Field).where(Field.value == value)
                if not fieldkind_id:
                    result = query.all()
                else:
                    result = query.where(Field.fieldkind_id == fieldkind_id).all()
                self.session.expunge_all()
                return result

    def roles_by_user(self, user_id=None):
        with self.mutex:
            with self.session.begin():
                query = self.session.query(Role).join(User.user_roles).where(User.id == user_id)
                result = query.all()
                self.session.expunge_all()
                return result

    def subissues_by_id(self, id):
        with self.mutex:
            with self.session.begin():
                result = self.session.query(Issue).where(Issue.parent_id == id).all()
                self.session.expunge_all()
                return result
