import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import numpy as np
import joblib

# 1. Load the trained model
model = joblib.load('clean_water_model.pkl')

# Define baselines for the start year (2026)
BASE_TEMP = 15.0  
BASE_NITRATE = 10.0 

# 2. Initialize App
app = dash.Dash(__name__)
server = app.server

app.layout = html.Div([
    html.H2("Future Projection: Clean Water Probability (2026-2050)", style={'textAlign': 'center', 'fontFamily': 'sans-serif'}),
    
    html.Div([
        html.Label("Nitrate Reduction % (Policy Intervention):", style={'fontWeight': 'bold'}),
        dcc.Slider(
            id='nitrate-slider', 
            min=0, max=100, value=20, 
            marks={i: f'{i}%' for i in range(0, 101, 20)}
        ),
        
        html.Br(),
        
        html.Label("Sea Surface Temp Anomaly °C (Climate Scenario):", style={'fontWeight': 'bold'}),
        dcc.Slider(
            id='temp-slider', 
            min=0.0, max=3.0, value=1.0, step=0.1, 
            marks={i/10: f'+{i/10}°C' for i in range(0, 31, 5)}
        ),
    ], style={'width': '80%', 'margin': 'auto', 'paddingBottom': '30px', 'fontFamily': 'sans-serif'}),
    
    dcc.Graph(id='projection-graph')
])

# 3. Model Inference Logic
@app.callback(
    Output('projection-graph', 'figure'),
    [Input('nitrate-slider', 'value'),
     Input('temp-slider', 'value')]
)
def update_projection(nitrate_reduction, temp_anomaly):
    years = np.arange(2026, 2051)
    
    # Simulate feature changes over time based on sliders
    # Temperature increases linearly up to the selected anomaly by 2050
    temp_trend = np.linspace(BASE_TEMP, BASE_TEMP + temp_anomaly, len(years))
    
    # Nitrate decreases linearly to the target reduction by 2050
    target_nitrate = BASE_NITRATE * (1 - nitrate_reduction / 100)
    nitrate_trend = np.linspace(BASE_NITRATE, target_nitrate, len(years))
    
    # Create the future dataframe (must match the model's training features)
    future_df = pd.DataFrame({
        'temperature_c_mean': temp_trend,
        'nitrate_umol_l_mean': nitrate_trend
    })
    
    # Predict probabilities. predict_proba returns [prob_class_0, prob_class_1]
    # We want prob_class_1 (Clean Water)
    probs = model.predict_proba(future_df)[:, 1]
    
    # Plot the results
    plot_df = pd.DataFrame({'Year': years, 'Probability': probs * 100})
    fig = px.line(plot_df, x='Year', y='Probability', 
                  range_y=[0, 100],
                  labels={'Probability': 'Probability of Clean Water (%)'})
    
    fig.update_traces(line=dict(width=4, color='#2ca02c'))
    fig.update_layout(margin={"r":40,"t":40,"l":40,"b":40})
    
    return fig

if __name__ == '__main__':
    app.run(debug=True)