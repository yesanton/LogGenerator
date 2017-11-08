# import numpy as np
# import matplotlib.pyplot as plt
# from matplotlib.lines import Line2D
#
#
# points = np.ones(6)  # Draw 3 points for each line
# text_style = dict(horizontalalignment='right', verticalalignment='center',
#                   fontsize=12, fontdict={'family': 'monospace'})
# marker_style = dict(color='cornflowerblue', linestyle=':', marker='o',
#                     markersize=15, markerfacecoloralt='gray')
#
#
# def format_axes(ax):
#     ax.margins(0.2)
#     ax.set_axis_off()
#
#
# def nice_repr(text):
#     return repr(text).lstrip('u')
#
#
# fig, ax = plt.subplots()
#
# # Plot all fill styles.
# for y, fill_style in enumerate(Line2D.fillStyles):
#     ax.text(-0.5, y, nice_repr(fill_style), **text_style)
#     ax.plot(y * points, fillstyle=fill_style, **marker_style)
#     format_axes(ax)
#     ax.set_title('fill style')
#
# plt.show()
#
#

import plotly
import plotly.plotly as py
from plotly.graph_objs import *

import networkx as nx
plotly.tools.set_credentials_file(username='AntonYeshchenko', api_key='5eT8pYJMAXm8ebBixW2P')

G=nx.random_geometric_graph(200,0.125)
pos=nx.get_node_attributes(G,'pos')

dmin=1
ncenter=0
for n in pos:
    x,y=pos[n]
    d=(x-0.5)**2+(y-0.5)**2
    if d<dmin:
        ncenter=n
        dmin=d

p=nx.single_source_shortest_path_length(G,ncenter)

##################

edge_trace = Scatter(
    x=[],
    y=[],
    line=Line(width=0.5,color='#888'),
    hoverinfo='none',
    mode='lines')

for edge in G.edges():
    x0, y0 = G.node[edge[0]]['pos']
    x1, y1 = G.node[edge[1]]['pos']
    edge_trace['x'] += [x0, x1, None]
    edge_trace['y'] += [y0, y1, None]

node_trace = Scatter(
    x=[],
    y=[],
    text=[],
    mode='markers',
    hoverinfo='text',
    marker=Marker(
        showscale=True,
        # colorscale options
        # 'Greys' | 'Greens' | 'Bluered' | 'Hot' | 'Picnic' | 'Portland' |
        # Jet' | 'RdBu' | 'Blackbody' | 'Earth' | 'Electric' | 'YIOrRd' | 'YIGnBu'
        colorscale='YIGnBu',
        reversescale=True,
        color=[],
        size=10,
        colorbar=dict(
            thickness=15,
            title='Node Connections',
            xanchor='left',
            titleside='right'
        ),
        line=dict(width=2)))

for node in G.nodes():
    x, y = G.node[node]['pos']
    node_trace['x'].append(x)
    node_trace['y'].append(y)

####################################################

print (G.edges)

for node, adjacencies in enumerate(G.edges):
    node_trace['marker']['color'].append(len(adjacencies))
    node_info = '# of connections: '+str(len(adjacencies))
    node_trace['text'].append(node_info)

####################################################

fig = Figure(data=Data([edge_trace, node_trace]),
             layout=Layout(
                title='<br>Network graph made with Python',
                titlefont=dict(size=16),
                showlegend=False,
                hovermode='closest',
                margin=dict(b=20,l=5,r=5,t=40),
                annotations=[ dict(
                    text="Python code: <a href='https://plot.ly/ipython-notebooks/network-graphs/'> https://plot.ly/ipython-notebooks/network-graphs/</a>",
                    showarrow=False,
                    xref="paper", yref="paper",
                    x=0.005, y=-0.002 ) ],
                xaxis=XAxis(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=YAxis(showgrid=False, zeroline=False, showticklabels=False)))

py.plot(fig, filename='networkx')

















