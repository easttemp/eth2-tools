from datetime import datetime
from pony.orm import *

db = Database()
db.bind(provider='sqlite', filename='db.sqlite', create_db=True)

class GetMixin():
    @classmethod
    def get_or_create(cls, **params):
        o = cls.get(**params)
        if o:
            return o
        return cls(**params)

class Stats(db.Entity, GetMixin):
    epoch = Required(int, size=64)
    validator = Required(int)

    att_slot = Optional(int, size=64)
    inc_slot = Optional(int, size=64)
    status = Optional(int)
    comm_idx = Optional(int)
    dist = Optional(int)

    balance = Optional(int, size=64)
    earn = Optional(int, size=64)

    insert_on = Required(datetime, default=datetime.now)
    update_on = Optional(datetime)

    PrimaryKey(epoch, validator)

db.generate_mapping(create_tables=True)

