import dash
import dash_core_components as dcc
import dash_html_components as html
import math
import pandas as pd
import plotly.graph_objs as go


app = dash.Dash()
csv_url = "https://storage.googleapis.com/learn_pd_like_tidyverse/gapminder.csv"
gapminder = pd.read_csv(csv_url)
nrows, ncols = gapminder.shape
min_year = gapminder["year"].min()
max_year = gapminder["year"].max()
year_interval = gapminder["year"].unique()[1] - gapminder["year"].unique()[0]
ncountries = gapminder["country"].nunique()
msg = "這個摘錄版本僅有 {} 個觀測值、{} 個變數，涵括 {} 至 {} 年中每 {} 年、{} 個國家的快照"

print("變數名稱：")
print(list(gapminder.columns))
print(msg.format(nrows, ncols, min_year, max_year, year_interval, ncountries))


df = pd.read_csv(
    "https://storage.googleapis.com/learn_pd_like_tidyverse/gapminder.csv")
bubble_size = [math.sqrt(p / math.pi) for p in df["pop"].values]
df['size'] = bubble_size
sizeref = 2*max(df['size'])/(100**2)

app.layout = html.Div([
    html.H2(children='A Gapminder Replica with Dash'),
    dcc.Graph(id='gapminder',
              animate=True
              ),
    dcc.Slider(
        id='year-slider',
        min=df['year'].min(),
        max=df['year'].max(),
        value=df['year'].min(),
        step=None,
        marks={str(year): str(year) for year in df['year'].unique()}
    )
])


@app.callback(
    dash.dependencies.Output('gapminder', 'figure'),
    [dash.dependencies.Input('year-slider', 'value')])
def update_figure(selected_year):
    filtered_df = df[df.year == selected_year]
    traces = []
    for i in filtered_df.continent.unique():
        df_by_continent = filtered_df[filtered_df['continent'] == i]
        traces.append(go.Scatter(
            x=df_by_continent['gdpPercap'],
            y=df_by_continent['lifeExp'],
            text=df_by_continent['country'],
            mode='markers',
            opacity=0.7,
            marker={
                'size': df[df['continent'] == i]['size'],
                'line': {'width': 0.5, 'color': 'white'},
                'sizeref': sizeref,
                'symbol': 'circle',
                'sizemode': 'area'
            },
            name=i
        ))

    return {
        'data': traces,
        'layout': go.Layout(
            xaxis={'type': 'log', 'title': 'GDP Per Capita'},
            yaxis={'title': 'Life Expectancy', 'range': [20, 90]},
            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            legend={'x': 0, 'y': 1},
            hovermode='closest'
        )
    }


if __name__ == '__main__':
    app.run_server(debug=True)