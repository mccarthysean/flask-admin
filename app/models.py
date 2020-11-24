
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


class PowerUnitMeta(db.Model):
    """Model of the public.power_units_meta table, 
    for metadata about the table row/column, such as fill and font color"""

    __tablename__ = 'power_units_meta'
    # __table_args__ = {"schema": "public"}
    
    id = db.Column(Integer, primary_key=True)

    # This is the primary key of the underlying table
    power_unit_id = db.Column(Integer, db.ForeignKey('power_units.id'), nullable=False)

    # The Flask-Admin table view column we're formatting
    col = db.Column(String, nullable=False)

    # The HEX fill color of the cell
    fill_color = db.Column(String)

    # The HEX font color of the cell
    text_color = db.Column(String)

    def __repr__(self):
        return f'PowerUnitMeta({self.power_unit_id}, {self.col}, {self.fill_color}, {self.text_color})'
