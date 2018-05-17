from pony.orm import *
from models.DataBase import DataBase

db = DataBase.get_database()


class EntityTags(db.Entity):
    id = PrimaryKey(int, auto=True)
    tag_value = Required(str)
    buildin = Required(bool, default=False)
    expressions = Optional(str)
    values = Optional(str)
    lookup = Optional(str)
    info = Set('Info')
    qstnnr = Optional('Questionnaire')

    # ---- Query
    @staticmethod
    @db_session
    def select_all_entitytag():
        return select(p for p in EntityTags)[:]

    @staticmethod
    @db_session
    def select_entitytag(_id=None, tag_value=None):
        if _id is not None:
            return EntityTags[_id]

        if tag_value is not None:
           return EntityTags.get(tag_value=tag_value)

        raise Exception('id or tagvalue must be provided')

    @staticmethod
    @db_session
    def create_entitytag(tag_value, values, exprs, buildin, lookup=''):
        et = EntityTags(tag_value=tag_value, expressions=exprs, values=values, buildin=buildin, lookup=lookup)
        return et
