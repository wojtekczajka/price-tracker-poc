import pandas as pd
import plotly.express as px

from sqlalchemy.orm import Session
from backend_app import models, crud

from backend_app.item import Item


def find_items(db: Session):
    items = []
    db_items = crud.get_items(db)
    for db_item in db_items:
        items.append(Item(db_item.name))
    return items


def generate_plots(db: Session):
    products = crud.get_items(db)
    for product in products:
        prices = product.prices
        temp_df = pd.DataFrame([(price.date, price.price)
                               for price in prices], columns=['date', 'price'])
        plot = px.line(data_frame=temp_df, x='date',
                       y='price', template='plotly_dark')
        plot.update_layout(margin=dict(l=0, r=0, t=0, b=0, pad=20))
        plot.update_xaxes()
        plot.update_yaxes(showgrid=False)
        file_path = 'backend_app/static/plots/' + product.name + '.html'
        plot.write_html(file_path, full_html=False, include_plotlyjs='cdn')
