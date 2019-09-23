"""
This is the info module and supports all the REST actions for the
Union general data
"""

from flask import make_response, abort
from config import db
from models import Discount, DiscountSchema
from sqlalchemy import and_, or_

def discounts_read_all():
    """
    This function responds to a request for /api/info/discounts
    with the complete lists of discounts

    :return:        json string of list of discounts
    """
    # Create the list of events from our data
    discounts = Discount.query.order_by(Discount.id).all()

    # Serialize the data for the response
    discount_schema = DiscountSchema(many=True)
    data = discount_schema.dump(discounts).data
    return data