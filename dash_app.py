# DashApp.py
import dash
from dash import html, dcc, dash_table
from dash.dependencies import Input, Output
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import plotly.graph_objs as go

app = dash.Dash(__name__, suppress_callback_exceptions=True)

# Dataset and Calculations
df = pd.read_csv(r'E:\Work\Infina Health\Test 2 Dashboard\GSC_Test_2.csv')
# Date
df['Date'] = pd.to_datetime(df['Date'])
df_agg_date = df.groupby('Date').sum(numeric_only=True).reset_index()
# Country
df_country = df.groupby('Country')['Clicks'].sum(numeric_only=True).reset_index()
df_country = df_country.sort_values('Clicks', ascending=False)
df_country = df_country.head(5)
# Device
df_device = df.groupby('Device')[['Clicks', 'Impressions', 'CTR']].sum(numeric_only=True).reset_index()
# URLs
df_url = df.groupby('URL')['Clicks'].sum().reset_index()
df_url = df_url.sort_values('Clicks', ascending=False).head(10)

# Normalization
scaler = MinMaxScaler()
df_agg_date[['Clicks', 'Impressions', 'CTR']] = scaler.fit_transform(df_agg_date[['Clicks', 'Impressions', 'CTR']])

# garph 1
# Create the wordcloud object
text = " ".join(word for word in df['Keyword'].astype(str))
wordcloud = WordCloud(width=720, height=480, margin=0).generate(text)
wordcloud_image = wordcloud.to_array()

wordcloud_graph = dcc.Graph(
    id='wordcloud-graph',
    figure=go.Figure(
        data=[go.Image(z=wordcloud_image)],
        layout=go.Layout(
            title="Word Cloud for Keywords",
            template='plotly_dark'  # Set the template to 'plotly_dark'
        )
    )
)

# garph 2
trend_graph = dcc.Graph(
    id='line-graph',
    figure={
        'data': [
            go.Scatter(
                x=df_agg_date['Date'],
                y=df_agg_date['Clicks'],
                mode='lines',
                name='Clicks'
            ),
            go.Scatter(
                x=df_agg_date['Date'],
                y=df_agg_date['Impressions'],
                mode='lines',
                name='Impressions'
            ),
            go.Scatter(
                x=df_agg_date['Date'],
                y=df_agg_date['CTR'],
                mode='lines',
                name='CTR'
            )
        ],
        'layout': go.Layout(
            title='Normalized Trend Analysis of Clicks, Impressions and CTR',
            xaxis={'title': 'Date'},
            yaxis={'title': 'Values'},
            template='plotly_dark'
        )
    }
)

# garph 3
country_graph = dcc.Graph(
    id='country-clicks-graph',
    figure={
        'data': [
            go.Bar(
                x=df_country['Country'],
                y=df_country['Clicks'],
                name='Clicks'
            )
        ],
        'layout': go.Layout(
            title='Clicks by Country',
            xaxis={'title': 'Country'},
            yaxis={'title': 'Clicks'},
            template='plotly_dark'
        )
    }
)

# garph 4
device_graph = dcc.Graph(
    id='device-graph',
    figure={
        'data': [
            go.Bar(
                x=df_device['Device'],
                y=df_device['Clicks'],
                name='Clicks'
            ),
            go.Bar(
                x=df_device['Device'],
                y=df_device['Impressions'],
                name='Impressions'
            ),
            go.Bar(
                x=df_device['Device'],
                y=df_device['CTR'],
                name='Click Through Rate'
            )
        ],
        'layout': go.Layout(
            title='Clicks and Impressions by Device',
            xaxis={'title': 'Device'},
            yaxis={'title': 'Count'},
            barmode='group',
            template='plotly_dark'
        )
    }
)

# URL Table
url_table = dash_table.DataTable(
    id='url-table',
    columns=[{"name": i, "id": i} for i in df_url.columns],
    data=df_url.to_dict('records'),
    style_data={
        'whiteSpace': 'normal',
        'height': 'auto',
        'lineHeight': '15px'
    },
    style_cell={
        'backgroundColor': 'rgb(50, 50, 50)',
        'color': 'white',
        'textAlign': 'left',
    },
    style_header={
        'backgroundColor': 'rgb(30, 30, 30)',
        'color': 'white'
    },
)


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div([
        html.Br(),
        html.H1("DataPulse", style={'textAlign': 'center', 'fontSize': '70px', 'marginBottom': '5px', 'color': '#FFF'}),
        html.P("Racing with Care, Tracking with Precision.", style={'textAlign': 'center', 'fontSize': '40px', 'marginTop': '10px', 'marginBottom': '5px', 'color': '#FFF'}),
        html.Hr(style={'width': '100%'})
    ]),
    html.P("DataPulse is a dashboard for tracking and analyzing the performance of your website. It provides a comprehensive analysis of the keywords, countries, devices and URLs that are driving traffic to your website. The dashboard is designed to provide a quick and easy way to understand the performance of your website and make informed decisions.", style={'textAlign': 'center', 'fontSize': '20px', 'marginBottom': '5px', 'color': '#FFF'}),
    html.Br(),
    html.Br(),
    html.P('The graph below shows the trend of Clicks, Impressions and Click Through Rate (CTR) over time. The values have been normalized to provide a better comparison. Click the legends to hide or unhide graph elements.', style={'textAlign': 'center', 'fontSize': '20px', 'marginBottom': '5px', 'color': '#FFF'}),
    html.Br(),
    trend_graph,
    html.Br(),
    html.Br(),
    html.P('The word cloud below shows the most common keywords that are driving traffic to your website. The size of the word represents the frequency of the keyword. The Bar chart shows the top 5 countries by clicks that have visited your webiste.', style={'textAlign': 'center', 'fontSize': '20px', 'marginBottom': '5px', 'color': '#FFF'}),
    html.Br(),
    html.Div(
    children=[
        html.Div(wordcloud_graph, style={'margin-right': '20px'}),
        country_graph
    ],
    style={'display': 'flex'}),
    html.Br(),
    html.Br(),
    html.P('The bar chart below shows the number of clicks and impressions by device. Click the legends to minimize an element from the chart. The table shows the top 10 URLs that have led to clicks on the website.', style={'textAlign': 'center', 'fontSize': '20px', 'marginBottom': '5px', 'color': '#FFF'}),
    html.Br(),
    html.Div(
    children=[
        html.Div(device_graph, style={'margin-right': '20px'}),
        html.Div(
            children=[
                html.H3('Top 10 URLs by Clicks', style={'color': '#FFF'}),
                url_table
            ],
            style={'display': 'block'}
        )
    ], 
    style={'display': 'flex'}),   
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br()
], style={
    'backgroundColor': '#1E1E1E',
    'color': '#FFF'}  # White text
)

if __name__ == '__main__':
    app.run_server(debug=True)