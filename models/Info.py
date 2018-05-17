from pony.orm import *
from models.DataBase import DataBase
from models.EntityTags import EntityTags
import json

db = DataBase.get_database()


class Info(db.Entity):
    id = PrimaryKey(int, auto=True)
    tag = Required('EntityTags')

    # The type of object user is asking for. Ex. place, material, abstract, company
    type = Optional(str)

    #The specific objetc user is asking for. Ex: Cetrez, love, stage, room, toilet
    name = Optional(str)

    info_text = Required(str)

    @staticmethod
    @db_session
    def select_all_info():
        all_info = select(info for info in Info)[:]
        for x in range(0, len(all_info)):
            all_info[x].tag.load()
        return all_info

    @staticmethod
    @db_session
    def get_info(entity_name, value, keyword):
        et = EntityTags.get(tag_value=entity_name)
        if et is not None:
            et_values = json.loads(et.values)
            if value in et_values:
                i = Info.get(tag=et, type=value, name=keyword)
                return i
            return None
        return None

    @staticmethod
    @db_session
    def create_info(tag_id, info_text):
        et = EntityTags.select_entitytag(tag_id)
        i = Info(tag=et, info_text=info_text)
        return i
