from datetime import datetime
from config import db, ma
from marshmallow import fields

class Event(db.Model):
    __tablename__ = 'events'
    event_id = db.Column(db.Integer, primary_key=True)
    event_name = db.Column(db.String)
    event_term = db.Column(db.String)
    event_subtitle = db.Column(db.String)
    event_description = db.Column(db.Unicode)
    event_date = db.Column(db.String)
    event_start = db.Column(db.String)
    event_end = db.Column(db.String)
    event_going = db.Column(db.Integer)
    event_interested = db.Column(db.Integer)
    event_start_timestamp = db.Column(db.Integer)
    event_status = db.Column(db.String)
    event_type = db.Column(db.String)
    event_open_to_all = db.Column(db.String)
    event_photo_url = db.Column(db.String)
    event_action_text = db.Column(db.String)
    event_action_url = db.Column(db.String)

    event_speakers = db.relationship(
        'Speaker',
        backref='event',
        cascade='all, delete, delete-orphan',
        single_parent=True,
        order_by='Speaker.speaker_id'
    )

class Speaker(db.Model):
    __tablename__ = 'speakers'
    speaker_id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.event_id'))
    speaker_name = db.Column(db.String)
    speaker_type = db.Column(db.String)
    speaker_description = db.Column(db.String)
    speaker_thumb_url = db.Column(db.String)

class EventSchema(ma.ModelSchema):
    def __init__(self, **kwargs):
        super().__init__(strict=True, **kwargs)

    class Meta:
        model = Event
        sqla_session = db.session

    event_speakers = fields.Nested("EventSpeakerSchema", default=[], many=True)

class EventSpeakerSchema(ma.ModelSchema):
    """
    This class exists to get around a recursion issue
    """

    def __init__(self, **kwargs):
        super().__init__(strict=True, **kwargs)

    speaker_id = fields.Int()
    event_id = fields.Int()
    speaker_name = fields.Str()
    speaker_type = fields.Str()
    speaker_description = fields.Str()
    speaker_thumb_url = fields.Str()


class SpeakerSchema(ma.ModelSchema):
    def __init__(self, **kwargs):
        super().__init__(strict=True, **kwargs)

    class Meta:
        model = Speaker
        sqla_session = db.session

    event = fields.Nested("SpeakerEventSchema", default=None)


class SpeakerEventSchema(ma.ModelSchema):
    """
    This class exists to get around a recursion issue
    """

    def __init__(self, **kwargs):
        super().__init__(strict=True, **kwargs)

    event_id = fields.Int()
    event_name = fields.Str()
    event_term = fields.Str()
    event_subtitle = fields.Str()
    event_description = fields.Str()
    event_date = fields.Str()
    event_start = fields.Str()
    event_end = fields.Str()
    event_going = fields.Int()
    event_interested = fields.Int()
    event_start_timestamp = fields.Int()
    event_status = fields.Str()
    event_type = fields.Str()
    event_open_to_all = fields.Str()
    event_photo_url = fields.Str()
    event_action_text = fields.Str()
    event_action_url = fields.Str()

class Discount(db.Model):
    __tablename__ = 'discounts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    subtitle = db.Column(db.String)
    image = db.Column(db.String)
    description = db.Column(db.String)

class DiscountSchema(ma.ModelSchema):
    class Meta:
        model = Discount
        sqla_session = db.session