import pandas as pd

import dash
import dash_core_components as dcc
import dash_html_components as html

import plotly.graph_objs as go

from components.app_components import *
from models import *

# GET SETTINGS
settings = Settings(file_path='config.json')

# DEFINE VARIABLES
FILE_PATH = settings.get('FILE_PATH')
CSS = settings.get('CSS')

# GET DATA
data = read_and_reduce_file(FILE_PATH)

# GET MODELS AND DEFINE COLUMNS
geographics = Geographics(data, city='s_city', state='s_state', zipcode='s_zip_code', \
                              sale_price='SalePrice', cost='Cost', quantity='Quantity', \
                           customer_id='CustomerID', order_id='OrderNumber')

customers = Customers(data, customer_id='CustomerID', order_id='OrderNumber', \
                               quantity='Quantity', referrer='Domain', sale_price='SalePrice', \
                               cost= 'Cost')

# DEFINE DATA VARIABLES
geo_sales_breakdown = geographics.get_sales_breakdown(by='state')
geo_customer_breakdown = geographics.get_customer_breakdown(by='state')
geo_orders_breakdown = geographics.get_orders_breakdown(by='state')

# CREATE APP
app = dash.Dash(__name__, external_stylesheets=CSS)

# APP CONTAINS A HEADER, SUMMARY STATISTICS, SEVERAL GRAPHS, TABLE
app.layout = html.Div(children=[
		html.H1(style={'textAlign': 'center'}, children='Infographic'),

		# GEOGRAPHICS SUMMARY
		html.H3(style={'textAlign': 'left'}, children='Geographics Summary'),

		create_graph(id='geo-sales-breakdown', figure_type='pie', labels=geo_sales_breakdown[0], \
						values=geo_sales_breakdown[1], x_legend='STATE', y_legend='PROFITS', mode='lines+markers'),

		create_graph(id='geo-customer-breakdown', figure_type='bar', labels=geo_customer_breakdown[0], \
						values=geo_customer_breakdown[1], x_legend='STATE', y_legend='CUSTOMERS'),

		create_graph(id='geo-orders-breakdown', figure_type='scatter', labels=geo_orders_breakdown[0], \
						values=geo_sales_breakdown[1], x_legend='STATE', y_legend='TOTAL PROFIT ($)', mode='lines+markers'),

		# DATA TABLE
		html.H3(style={'textAlign': 'left'}, children='Data Table'),
		generate_table(data, max_rows=15),
	]
)

if __name__ == '__main__':
	_ = app.run_server(debug=True)
