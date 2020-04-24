import dash
import dash_core_components as dcc
import dash_html_components as html
import math
import pandas as pd
import plotly.graph_objs as go

# 資料來源
#https://docs.google.com/spreadsheets/d/1oqAodqH5uOICXZOdHztzuGBONO1e-zz2JrWGCjOohQ4/edit?usp=sharing

app = dash.Dash()
csv_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTqzKuhRiVOv_-dbJ8uGKTes2vRQpr9xfORuT9L6gD9qaBLvwZ2eROwOwnCwDMTbC9E7_6oypZOMKdJ/pub?output=csv"
df = pd.read_csv(csv_url)
nrows, ncols = df.shape

##定義氣泡大小
bubble_size = [math.sqrt(p / math.pi) for p in df["rating"].values]
df['size'] = bubble_size
sizeref = 2*max(df['size'])/(100**2)

#建立散佈圖
app.layout = html.Div([
    html.H2(children='身高體重'),
    dcc.Graph(
        id='gapminder',
        figure={
            'data': [
                go.Scatter(
                    x=df['height'],
                    y=df['fans'],
                    text=df['name'],
                    mode='markers',
                    opacity=0.7,
                    marker={
                        'size': df['size'],
                        'line': {'width': 0.5, 'color': 'white'},
                        'sizeref': sizeref,
                        'symbol': 'circle',
                        'sizemode': 'area'
                    },
                    name="tt"
                )
            ],
            'layout': go.Layout(
                xaxis={'type': 'log', 'title': '身高'},
                yaxis={'title': '體重'},
                margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                legend={'x': 0, 'y': 1},
                hovermode='closest'
            )
        }
    ),
    # 折线图
    dcc.Graph(
        id='graph-line',
        className='my_graph',
        figure={
            'data': [{
                'x': df['height'],
                'y': df['fans'],
                'type': 'scatter',
                'mode': 'lines+markers',
            }],
            'layout': {
                'title': '各城市男性人口',
                'height': 600,
                'yaxis': {'hoverformat': '.0f'},
                'margin': {'l': 35, 'r': 35, 't': 50, 'b': 80},
            }
        },
        config={
            'displayModeBar': False
        },
    ),
])

if __name__ == '__main__':
    app.run_server(debug=True)