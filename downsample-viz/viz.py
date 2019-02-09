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


count = [i for i in range(target, 1000000, 100)]

# Calculate score for each downsampling group
# Floor divide i to simulate the grouping behavior of downsampling
# Note: this is assumes a perfectly spaced write interval in the realtime dataset
# Production values indicate there's a significant offset
scores = [
    [calc(i) for i in count],
    [calc(i//12) for i in count],  # downsample 1m
    [calc(i//(12*10)) for i in count],  # downsample_10m
    [calc(i//(12*10*6)) for i in count],  # downsample_1h
    [calc(i//(12*10*6*6)) for i in count],  # downsample_6h
]

# Comment out this for loop to view full range of data
# We're deleting all data from non-chosen downsampling sets to improve clarity
for vidx in range(len(count)):
    slice = [score[vidx] for score in scores]
    best_score = min([v for v in slice if v is not None])

    for sidx, score in enumerate(scores):
        if slice[sidx] != best_score:
            score[vidx] = None

traces = [
    go.Scatter(
        x=count,
        y=scores[0],
        mode='lines',
        name='realtime',
    ),
    go.Scatter(
        x=count,
        y=scores[1],
        mode='lines',
        name='downsample_1m',
    ),
    go.Scatter(
        x=count,
        y=scores[2],
        mode='lines',
        name='downsample_10m',
    ),
    go.Scatter(
        x=count,
        y=scores[3],
        mode='lines',
        name='downsample_1h',
    ),
    go.Scatter(
        x=count,
        y=scores[4],
        mode='lines',
        name='downsample_6h',
    )
]


py.plot(traces, filename='downsampling')
