# dashboard-app
Offers a plug and play dashboard built using Dash and Plotly.

## Prerequisites
* Requires the Dash and Pandas library

## Installing
1. Create a virtual environment for your project and activate project
`virtualenv -p python3 [projectname]`

2. Clone repository
`git clone https://github.com/hd9319/dashboard-app`

3. Install dependencies using requirements.txt files
`pip install -r requirements.txt`

## How to Use
1. Define configurations in config.json for CSS styling and Path of Data File
2. Make changes to Classes defined in app.py so it reflects the column headers used in your file.
```
geographics = Geographics(data, city='col_name', state='col_name', zipcode='col_name', \
                              sale_price='col_name', cost='col_name', quantity='col_name', \
                           customer_id='col_name', order_id='col_name')
```
