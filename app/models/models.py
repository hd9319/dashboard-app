import os
import json
#import requests
import pandas as pd

def read_and_reduce_file(file_path):
    data = pd.read_csv(file_path)
    for column in data.select_dtypes('object'):
        data[column] = data[column].astype('category')
    return data

class Settings:
	def __init__(self, **kwargs):
		with open(file_path, 'r') as readfile:
			settings = json.load(readfile)
		settings.update({k: v for k, v in kwargs.items() if k in settings.key()})
		self.settings = settings

	def __call__(self):
		return self.settings

	def get(self, keyword):
		return self.settings.get(keyword)


class BaseAnalytics:
    allowed_columns = []

    def __init__(self, data, **kwargs):
        self._columns = {}
        self._columns.update({v: k for k, v in kwargs.items() if k in self.allowed_columns})
        data = data.rename(columns=self._columns)
        self.data = self._preprocess(data)

    def _preprocess(self, data):
        data['sales'] = data['sale_price'] * data['quantity']
        data['costs'] = data['cost'] * data['quantity']
        data['profit'] = data['sales'] - data['costs']
        #gender_dict = {name: self._assumed_gender(name) for name in data['first_name'].unique()}
        #data['gender'] = data['first_name'].map(gender_dict)
        return data

    def _assumed_gender(self, name):
        return requests.get('https://api.genderize.io/?name=%s' % name).json()['gender']

class Customers(BaseAnalytics):
    allowed_columns = ['customer_id', 'order_id', 'quantity', 'referrer', 'sale_price', 'cost', \
                       'register_date', 'added_date', 'order_date']

    def get_gender_breakdown(self):
        gender_breakdown = self.data.groupby(by='gender').agg({'customer_id': 'nunique'}).\
                                        reset_index()
        return gender_breakdown['gender'], gender_breakdown['customer_id']

    def get_referral_breakdown(self, ascending=False, n_results=10):
        referral_breakdown = self.data.groupby(by='referrer').agg({'customer_id': 'nunique'}).\
                                                sort_values(by='customer_id', ascending=ascending).\
                                                reset_index().head(n_results)
        return referral_breakdown['referrer'], referral_breakdown['customer_id']

    def get_summary_stats(self, ascending=False, n_results=10):
        average_customer_value = self.data.groupby(by='customer_id').agg({'profit': 'sum'})['profit'].mean()
        average_cart_value = self.data.groupby(by='order_id').agg({'sale_price': 'sum'})['sale_price'].mean()
        average_num_purchases = self.data.groupby(by='customer_id').agg({'order_id': 'nunique'})['order_id'].mean()
        average_cart_size = self.data.groupby(by='order_id').agg({'quantity': 'sum'})['quantity'].mean()

        return {'average_customer_value': average_customer_value, 'average_cart_size': average_cart_size,
                'average_cart_value': average_cart_value, 'average_num_purchases': average_num_purchases}

class Geographics(BaseAnalytics):
    allowed_columns = ['city', 'state', 'zipcode', 'quantity', 'domain', 'customer_id', \
                       'order_id', 'sale_price', 'cost', 'first_name']

    def get_sales_breakdown(self, by, agg_method='sum', ascending=False, n_results=10):
        sales_breakdown = self.data.groupby(by=by).agg({'profit': agg_method}).\
                                                sort_values(by='profit', ascending=ascending).\
                                                reset_index().head(n_results)
        return sales_breakdown[by], sales_breakdown['profit']

    def get_customer_breakdown(self, by, ascending=False, n_results=10):
        customer_breakdown = self.data.groupby(by=by).agg({'customer_id': 'nunique'}).\
                                                sort_values(by='customer_id', ascending=ascending).\
                                                reset_index().head(n_results)
        return customer_breakdown[by], customer_breakdown['customer_id']

    def get_orders_breakdown(self, by, ascending=False, n_results=10):
        orders_breakdown = self.data.groupby(by=by).agg({'order_id': 'nunique'}).\
                                                sort_values(by='order_id', ascending=ascending).\
                                                reset_index().head(n_results)
        return orders_breakdown[by], orders_breakdown['order_id']

    def get_product_breakdown(self, by, ascending=False, n_results=15):
        pass
