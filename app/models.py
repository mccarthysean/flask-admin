
import os
import time
import jwt

from sqlalchemy import Table, Column, Integer, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import mapper

from app import db


class PowerUnit(db.Model):
    """Create a public.power_units table representation"""

    __tablename__ = 'power_units'
    # __table_args__ = {"schema": "public"}

    id = db.Column(Integer, primary_key=True)
    power_unit = db.Column(Integer, nullable=False, unique=True)
    notes = db.Column(String)

    def __repr__(self):
        return f'{self.power_unit}'


def create_meta_class(db, base_model, meta_model, db_table_name):
    """Given a regular base model, and a meta model to be filled out, 
    return the filled out meta model for the base model's metadata"""

    cols = [Column(name, String) for name in base_model.__mapper__.attrs.keys() if name != 'id']
    cols.insert(0, db.Column("id", Integer, primary_key=True))
    cols.insert(1, db.Column("id_foreign", Integer, db.ForeignKey(base_model.id, ondelete="CASCADE")))
    cols.insert(2, db.Column("element", String))
    tbl = Table(db_table_name, db.metadata, *cols)
    mapper(meta_model, tbl)

    return None


class PowerUnitMeta:
    pass


create_meta_class(db, PowerUnit, PowerUnitMeta, 'power_units_meta')

