"""
This is the info module and supports all the REST actions for the
Union general data
"""

from flask import make_response, abort
from config import db
from models import Discount, DiscountSchema, News, NewsSchema
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

def news_read_all():
    """
    This function responds to a request for /api/info/news/all
    with the complete lists of news

    :return:        json string of list of news
    """
    # Create the list of events from our data
    news = News.query.order_by(News.news_id).all()

    # Serialize the data for the response
    news_schema = NewsSchema(many=True)
    data = news_schema.dump(news).data
    return data

def news_read_few():
    """
    This function responds to a request for /api/info/news/few
    with the newest three news items

    :return:        json string of list of news
    """
    # Create the list of events from our data
    news = News.query.order_by(News.news_id).limit(3).all()

    # Serialize the data for the response
    news_schema = NewsSchema(many=True)
    data = news_schema.dump(news).data
    return data