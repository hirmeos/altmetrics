"""Core database instance and types."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

Boolean = db.Boolean  # Alias common db types.
Column = db.Column
DateTime = db.DateTime
ForeignKey = db.ForeignKey
Integer = db.Integer
Model = db.Model
String = db.String
Table = db.Table
backref = db.backref
relationship = db.relationship
