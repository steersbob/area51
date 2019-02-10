"""
Visualization for downsampling selection: at least target points
"""

import plotly.graph_objs as go
import plotly.plotly as py

target = 100


count = [i for i in range(target, 500000, 100)]
combined_points = [
    1,
    12,  # downsample 1m
    (12*10),  # downsample_10m
    (12*10*6),  # downsample_1h
    (12*10*6*6),  # downsample_6h
]
results = [[val // cmb for val in count] for cmb in combined_points]

# Calculate score for each downsampling group
# Floor divide i to simulate the grouping behavior of downsampling
# Note: this is assumes a perfectly spaced write interval in the realtime dataset
# Production values indicate there's a significant offset
for vidx in range(len(count)):
    slice = [result[vidx] for result in results]
    best_score = next(v for v in slice[::-1] if v >= target)

    for sidx, result in enumerate(results):
        if slice[sidx] != best_score:
            result[vidx] = None

fig = {
    'data': [
        go.Scatter(
            x=count,
            y=results[0],
            mode='lines',
            name='realtime',
        ),
        go.Scatter(
            x=count,
            y=results[1],
            mode='lines',
            name='downsample_1m',
        ),
        go.Scatter(
            x=count,
            y=results[2],
            mode='lines',
            name='downsample_10m',
        ),
        go.Scatter(
            x=count,
            y=results[3],
            mode='lines',
            name='downsample_1h',
        ),
        go.Scatter(
            x=count,
            y=results[4],
            mode='lines',
            name='downsample_6h',
        )
    ],
    'layout': {
        'shapes': [
            {
                'type': 'line',
                'x0': count[0],
                'x1': count[-1],
                'y0': target,
                'y1': target,
                'line': {
                    'color': 'rgb(55, 128, 191)',
                    'width': 4,
                    'dash': 'dot',
                },
            },
        ]
    }
}


py.plot(fig, filename='downsampling-min-points')
