import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

df = pd.read_csv('data/accidents.csv')

df['Year'] = df['Year'].astype(int)

app = Dash(__name__)

app.layout = html.Div([
    html.H1("India Road Accident Dashboard", style={'textAlign': 'center'}),
    html.Div([
    html.Div(id='total-accidents'),
    html.Div(id='total-fatalities'),
    html.Div(id='fatality-rate')
    ], style={
    'display': 'flex',
    'justifyContent': 'space-around',
    'fontSize': '20px',
    'margin': '20px'
    }),
    dcc.Dropdown(
        id='year-dropdown',
        options=[{'label': y, 'value': y} for y in sorted(df['Year'].unique())],
        value=df['Year'].min()
    ),
    dcc.Dropdown(id='state-dropdown',
        options=[{'label': s, 'value': s} for s in df['State'].unique()],
        multi=True,
        placeholder="Select States"),
    
    dcc.Graph(id='trend-graph'),
    dcc.Graph(id='state-bar'),
    dcc.Graph(id='top10-bar'),
    dcc.Graph(id='cause-pie'),
    dcc.Graph(id='fatal-vs-nonfatal'),
    dcc.Graph(id='monthly-trend'),
    dcc.Graph(id='india-map')
])


@app.callback(
    [
        Output('total-accidents', 'children'),
        Output('total-fatalities', 'children'),
        Output('fatality-rate', 'children'),
        Output('trend-graph', 'figure'),
        Output('state-bar', 'figure'),
        Output('top10-bar', 'figure'),
        Output('cause-pie', 'figure'),
        Output('fatal-vs-nonfatal', 'figure'),
        Output('monthly-trend', 'figure'),
        Output('india-map', 'figure')
    ],
    [Input('year-dropdown', 'value'),
    Input('state-dropdown', 'value')]
)

def update_dashboard(selected_year, selected_states):

    filtered = df[df['Year'] == selected_year]
    if selected_states:
        filtered = filtered[filtered['State'].isin(selected_states)]
    total_acc = filtered['Accidents'].sum()
    total_fat = filtered['Fatalities'].sum()

    if total_acc != 0:
        rate = round((total_fat / total_acc) * 100, 2)
    else:
        rate = 0
    
    kpi1 = f"Total Accidents: {total_acc}"
    kpi2 = f"Total Fatalities: {total_fat}"
    kpi3 = f"Fatality Rate: {rate}%"
    trend = df.groupby('Year')['Accidents'].sum().reset_index()
    fig1 = px.line(trend, x='Year', y='Accidents',
                   title='Total Accidents Over Years')

    state_data = filtered.groupby('State')['Accidents'].sum().reset_index()
    fig2 = px.bar(state_data, x='State', y='Accidents',
                  title=f'State-wise Accidents ({selected_year})')

    top10 = state_data.sort_values(by='Accidents', ascending=False).head(10)
    fig3 = px.bar(top10, x='State', y='Accidents',
                  title='Top 10 Accident States', color='Accidents')

    cause = filtered.groupby('Cause')['Accidents'].sum().reset_index()
    fig4 = px.pie(cause, names='Cause', values='Accidents',
                  title='Accident Causes')

    filtered['Non_Fatal'] = filtered['Accidents'] - filtered['Fatalities']
    fatal_data = filtered[['Fatalities', 'Non_Fatal']].sum().reset_index()
    fatal_data.columns = ['Type', 'Count']

    fig5 = px.bar(fatal_data, x='Type', y='Count',
                  title='Fatal vs Non-Fatal Accidents',
                  color='Type')

    month = filtered.groupby('Month')['Accidents'].sum().reset_index()
    fig6 = px.line(month, x='Month', y='Accidents',
                   title='Monthly Accident Trend')

    fig7 = px.choropleth(
        state_data,
        geojson='https://raw.githubusercontent.com/geohacker/india/master/state/india_telengana.geojson',
        featureidkey='properties.NAME_1',
        locations='State',
        color='Accidents',
        color_continuous_scale='Reds',
        title='India State-wise Accident Map'
    )

    fig7.update_geos(fitbounds="locations", visible=False)

    return kpi1, kpi2, kpi3, fig1, fig2, fig3, fig4, fig5, fig6, fig7
if __name__ == '__main__':
    app.run(debug=True, port = 8060)