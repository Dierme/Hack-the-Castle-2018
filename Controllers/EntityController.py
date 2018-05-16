from WitClient import WitClient
from config import CONFIG
from models.EntityTags import EntityTags
import json


class EntityController:
    @staticmethod
    def sync():
        client = WitClient(CONFIG['WIT_BASE_TOKEN'])
        entities = client.get_entities()

        for entity in entities:

            # skipping default wit entities
            if entity[:3] == 'wit':
                continue

            data = client.get_entity(entity)

            et = EntityTags.select_entitytag(tag_value=data['name'])
            if et is None:
                EntityTags.create_entitytag(tag_value=data['name'], exprs=json.dumps(data['values']),
                                        buildin=data['builtin'], lookup='/'.join(data['lookups']))

        return 0
