from datetime import datetime
from config import db, ma
from marshmallow import fields

class Event(db.Model):
    __tablename__ = "events"
    event_id = db.Column(db.Integer, primary_key=True)
    event_name = db.Column(db.String)
    event_description = db.Column(db.Unicode)
    event_date = db.Column(db.String)
    event_start = db.Column(db.String)
    event_end = db.Column(db.String)
    event_going = db.Column(db.Integer)
    event_interested = db.Column(db.Integer)
    event_start_timestamp = db.Column(db.Integer)
    event_status = db.Column(db.String)


class EventSchema(ma.ModelSchema):
    def __init__(self, **kwargs):
        super().__init__(strict=True, **kwargs)

    class Meta:
        model = Event
        sqla_session = db.session



