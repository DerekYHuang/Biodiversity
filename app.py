import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd

# 1. Load and prep data
df = pd.read_csv('dashboard_ecological_impact.csv')
df['year_month'] = pd.to_datetime(df['year_month'])
df['year'] = df['year_month'].dt.year

# 2. Initialize Dash app
app = dash.Dash(__name__)

# 3. Define the UI layout
app.layout = html.Div([
    html.H2("Ecological Impact: Vanishing Biodiversity", style={'textAlign': 'center', 'fontFamily': 'sans-serif'}),
    
    html.Div([
        html.Label("Select Year:", style={'fontFamily': 'sans-serif', 'fontWeight': 'bold'}),
        dcc.Slider(
            id='year-slider',
            min=df['year'].min(),
            max=df['year'].max(),
            value=df['year'].max(), # Default to the most recent year
            marks={str(year): str(year) for year in df['year'].unique()},
            step=None
        )
    ], style={'width': '80%', 'margin': 'auto', 'paddingBottom': '20px'}),
    
    dcc.Graph(id='impact-map', style={'height': '70vh'})
])

# 4. Define the callback to update the map when the slider moves
@app.callback(
    Output('impact-map', 'figure'),
    [Input('year-slider', 'value')]
)
def update_map(selected_year):
    # Filter data for the selected year
    filtered_df = df[df['year'] == selected_year]
    
    # Aggregate monthly data into a yearly summary for the map
    agg_df = filtered_df.groupby(['latitude', 'longitude']).agg({
        'anchovy_sightings': 'sum',
        'nitrate_umol_l_mean': 'mean',
        'oxygen_umol_kg_mean': 'mean',
        'temperature_c_mean': 'mean'
    }).reset_index()

    # Generate the Mapbox figure
    fig = px.scatter_mapbox(
        agg_df,
        lat="latitude",
        lon="longitude",
        size="anchovy_sightings",
        color="nitrate_umol_l_mean",
        color_continuous_scale=px.colors.sequential.OrRd, # Red indicates high nitrate
        size_max=40,
        zoom=5,
        mapbox_style="carto-positron", # Built-in style, no API key needed
        title=f"Anchovy Sightings vs. Nitrate Levels ({selected_year})",
        hover_data={
            "anchovy_sightings": True,
            "nitrate_umol_l_mean": ':.2f',
            "oxygen_umol_kg_mean": ':.2f',
            "temperature_c_mean": ':.2f',
            "latitude": False,
            "longitude": False
        }
    )
    
    fig.update_layout(margin={"r":0,"t":40,"l":0,"b":0})
    return fig

# 5. Run the app
if __name__ == '__main__':
    app.run(debug=True)