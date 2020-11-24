
import os
import time
import jwt

from sqlalchemy import Column, Integer, String

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
