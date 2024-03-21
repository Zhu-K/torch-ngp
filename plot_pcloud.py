import pandas as pd
import plotly.graph_objs as go
import numpy as np
import sys

# maximum points to display, high number may freeze display
MAX_POINTS = 100000

if len(sys.argv) < 2:
    print("Usage: python plot_pcloud.py filename.csv")
    sys.exit(1)

file_name = sys.argv[1]

df = pd.read_csv(file_name)
print("df read finished")
print("Total points:", df.shape[0])

# Sample a subset of the data
# Adjust n to change the sample size
sampled_df = df.sample(n=min(MAX_POINTS, df.shape[0]))
print("Displayed points:", sampled_df.shape[0])


# take log of density to squish magnitudes. Realistically opacity is 1-exp(-density)
sampled_df['density'] = np.log(sampled_df['density'])

# create colour strings for each row based on rgb
sampled_df['colour'] = sampled_df.apply(
    lambda row: f'rgb({int(row.r * 255)}, {int(row.g * 255)}, {int(row.b * 255)})', axis=1)


fig = go.Figure(data=[go.Scatter3d(
    x=sampled_df['x'],
    # Note: y and z are switched here compared to your initial code
    y=sampled_df['z'],
    z=sampled_df['y'],
    mode='markers',
    marker=dict(
        size=3,
        color=sampled_df['colour'],  # Set color to the RGB values
    )
)])

# fig = px.scatter_3d(sampled_df, x='x', y='z', z='y', color='density',
#                     color_continuous_scale=px.colors.sequential.Viridis)


# create point size slider
steps = []
for i in range(1, 11):
    step = dict(
        method="update",
        args=[{"marker.size": [i]}],  # marker size
        label=str(i)
    )
    steps.append(step)

sliders = [dict(
    active=2,
    currentvalue={"prefix": "Marker size: "},
    pad={"t": 50},
    steps=steps
)]

fig.update_layout(
    sliders=sliders
)

fig.show()
