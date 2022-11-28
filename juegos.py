from IPython.display import display

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go

import warnings
warnings.filterwarnings('ignore')

data_all = pd.read_csv('vgsales.csv')
scores = pd.read_csv('Video_Games_Sales_as_at_22_Dec_2016.csv')
metacritic = pd.read_csv('all_games.csv')

data_all = data_all.merge(scores, how='left').loc[:, :'Critic_Score']

temp = data_all.pivot_table(values='Global_Sales', index='Year', columns='Platform',
                            aggfunc='sum').fillna(0).reset_index()
temp_ = data_all.groupby(['Year', 'Platform'])['Global_Sales'].sum().reset_index()
t = temp_.groupby(['Year'])['Global_Sales'].nlargest(10).reset_index().level_1.values
order = temp_.iloc[t]['Platform'].unique()
colors = sns.color_palette("Spectral", len(temp.columns)-1)

fig = []
for i, col in enumerate(order):
    fig.append(go.Bar(name=col, x=temp['Year'], y=temp[col],
                      text=col, marker_color='rgb'+str(colors[i])))
figs = go.Figure(fig)
figs.update_layout(barmode='stack', height=600,
                   margin=dict(l=10, r=0, t=40, b=20),
                   title="Platform changes over Year",
                   yaxis_title="Total Sales (million)")
figs.show()