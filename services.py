import pandas as pd
import plotly.express as px

from sqlalchemy.orm import Session
from sql_app import models

from item import Item

def find_items(db: Session):
    items = []
    items_query = db.query(models.Item.name).distinct().all()
    for item_query in items_query:
        items.append(Item(item_query[0]))
    return items

def generate_plots(db: Session):
    products = db.query(models.Item.name).distinct().all()
    for product in products:
        temp_items = db.query(models.Item).filter(models.Item.name == product[0]).all()
        temp_df = pd.DataFrame([(item.date, item.price) for item in temp_items], columns=['date', 'price'])
        plot = px.line(data_frame=temp_df, x='date', y='price', template='plotly_dark')
        plot.update_layout(margin=dict(l=0, r=0, t=0, b=0, pad=20))
        plot.update_xaxes()
        plot.update_yaxes(showgrid=False)
        file_path = 'static/plots/' + product[0] + '.html'
        plot.write_html(file_path, full_html=False, include_plotlyjs='cdn')