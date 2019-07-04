"""
This is the people module and supports all the REST actions for the
people data
"""

from flask import make_response, abort
from config import db
from models import Event, EventSchema


def read_all():
    """
    This function responds to a request for /api/events
    with the complete lists of people

    :return:        json string of list of people
    """
    # Create the list of people from our data
    events = Event.query.order_by(Event.event_start_timestamp).all()

    # Serialize the data for the response
    event_schema = EventSchema(many=True)
    data = event_schema.dump(events).data
    return data


def read_one(event_id):
    """
    This function responds to a request for /api/events/{person_id}
    with one matching person from people

    :param event_id:   Id of event to find
    :return:            event matching id
    """
    # Build the initial query
    event = (
        Event.query.filter(Event.event_id == event_id)
        .one_or_none()
    )

    # Did we find a person?
    if event is not None:

        # Serialize the data for the response
        event_schema = EventSchema()
        data = event_schema.dump(event).data
        return data

    # Otherwise, nope, didn't find that person
    else:
        abort(404, f"Event not found for Id: {event_id}")

def upcoming():
    """
    This function returns a list of upcoming events from the database

    :return:        200 json string
    """

    upcoming_events = (
        Event.query.filter(Event.event_status == 'upcoming').order_by(Event.event_start_timestamp).all()
    )

    event_schema = EventSchema(many=True)
    data = event_schema.dump(upcoming_events).data
    return data

def next():
    """
    This function returns the next event from the database

    :return:        200 json string
    """

    next_event = (
        Event.query.filter(Event.event_status == 'upcoming').order_by(Event.event_start_timestamp).first()
    )

    event_schema = EventSchema()
    data = event_schema.dump(next_event).data
    return data

'''
def create(person):
    """
    This function creates a new person in the people structure
    based on the passed in person data

    :param person:  person to create in people structure
    :return:        201 on success, 406 on person exists
    """
    fname = person.get("fname")
    lname = person.get("lname")

    existing_person = (
        Person.query.filter(Person.fname == fname)
        .filter(Person.lname == lname)
        .one_or_none()
    )

    # Can we insert this person?
    if existing_person is None:

        # Create a person instance using the schema and the passed in person
        schema = PersonSchema()
        new_person = schema.load(person, session=db.session).data

        # Add the person to the database
        db.session.add(new_person)
        db.session.commit()

        # Serialize and return the newly created person in the response
        data = schema.dump(new_person).data

        return data, 201

    # Otherwise, nope, person exists already
    else:
        abort(409, f"Person {fname} {lname} exists already")


def update(person_id, person):
    """
    This function updates an existing person in the people structure

    :param person_id:   Id of the person to update in the people structure
    :param person:      person to update
    :return:            updated person structure
    """
    # Get the person requested from the db into session
    update_person = Person.query.filter(
        Person.person_id == person_id
    ).one_or_none()

    # Did we find an existing person?
    if update_person is not None:

        # turn the passed in person into a db object
        schema = PersonSchema()
        update = schema.load(person, session=db.session).data

        # Set the id to the person we want to update
        update.person_id = update_person.person_id

        # merge the new object into the old and commit it to the db
        db.session.merge(update)
        db.session.commit()

        # return updated person in the response
        data = schema.dump(update_person).data

        return data, 200

    # Otherwise, nope, didn't find that person
    else:
        abort(404, f"Person not found for Id: {person_id}")


def delete(person_id):
    """
    This function deletes a person from the people structure

    :param person_id:   Id of the person to delete
    :return:            200 on successful delete, 404 if not found
    """
    # Get the person requested
    person = Person.query.filter(Person.person_id == person_id).one_or_none()

    # Did we find a person?
    if person is not None:
        db.session.delete(person)
        db.session.commit()
        return make_response(f"Person {person_id} deleted", 200)

    # Otherwise, nope, didn't find that person
    else:
        abort(404, f"Person not found for Id: {person_id}")
'''