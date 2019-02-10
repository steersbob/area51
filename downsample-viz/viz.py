"""
Visualization for downsampling selection
"""

import plotly.graph_objs as go
import plotly.plotly as py

target = 200


def calc(i):
    if i == 0:
        return None
    return max(target, i) / min(target, i)


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
    scores = [calc(res) for res in slice]
    best_score = min([s for s in scores if s is not None])

    for sidx, result in enumerate(results):
        if scores[sidx] != best_score:
            result[vidx] = None

traces = [
    go.Scatter(
        x=count,
        y=[target]*len(count),
        mode='lines',
        name='approx_points',
    ),
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
]


py.plot(traces, filename='downsampling')
