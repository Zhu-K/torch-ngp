import pandas as pd
import plotly.express as px
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


# take log of density to squish magnitudes
sampled_df['density'] = np.log(sampled_df['density'])


fig = px.scatter_3d(sampled_df, x='x', y='z', z='y', color='density',
                    color_continuous_scale=px.colors.sequential.Viridis)
fig.update_traces(marker=dict(size=3))


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
