import pandas as pd

import dash
import dash_core_components as dcc
import dash_html_components as html

import plotly.graph_objs as go

def generate_scatter(x, y, name, mode, colors=False, **kwargs):
	return go.Scatter(
	    x = x,
	    y = y,
	    mode = mode, #markers/lines/lines+markers
	    name = name,
	)

def generate_bar(x, y, name, **kwargs):
	return go.Bar(
            x=x,
            y=y,
            name=name
    )

def generate_pie(labels, values, colors=False, **kwargs):
    return go.Pie(labels=labels, values=values,
    	hoverinfo='label+percent')

def generate_table(dataframe, max_rows=10):
    return html.Table(
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )

def create_graph(id, figure_type, labels, values, x_legend, y_legend, mode=False):
	if figure_type == 'scatter':
		plot = generate_scatter(x=labels, y=values, name=id, mode=mode)
	elif figure_type == 'pie':
		plot = generate_pie(labels=labels, values=values)
	elif figure_type == 'bar':
		plot = generate_bar(x=labels, y=values, name=id)

	return dcc.Graph(id=id,
				figure = {
							'data': [
										plot
								],
							'layout': go.Layout(
									xaxis = {'title': x_legend},
									yaxis = {'title': y_legend},
									margin = {'l': 50, 'r': 50, 't': 50, 'b': 50},
									legend = {'x': 0, 'y': 1},
									hovermode='closest'
								)
						}
			)

def create_nested_graph():
	pass