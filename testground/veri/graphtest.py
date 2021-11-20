# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%



# %%
import pandas
column_names = ["x","y","z"]
points = pandas.read_csv("orbit_test_1.asc",delimiter = " ",names=column_names)


# %%
x_list = points['x'].to_list()
y_list = points['y'].to_list()
z_list = points['z'].to_list()


# %%
import plotly
import plotly.graph_objects as go

#plotly.offline.init_notebook_mode()


# %%
#x_list = [elem * -1 for elem in x_list]
#y_list = [elem * -1 for elem in y_list]
#z_list = [abs(elem) for elem in z_list]


# %%
from random import randrange


# %%

# diff = len(x_list) - 3000000
# for _ in range(diff):
#     ind = randrange(len(x_list))
#     x_list.pop(ind)  #a 
#     z_list.pop(ind)
#     y_list.pop(ind)


x_list = x_list[300000:500000]
y_list = y_list[300000:500000]
z_list = z_list[300000:500000]


# %%

trace = go.Scatter3d(
    x=x_list,
    y=y_list,
    z=z_list,
    mode='markers',
    marker={
        'size':5,
        'opacity':0.8,
    }
)

layout = go.Layout(
    margin={'l': 0, 'r': 0, 'b': 0, 't': 0}
)

data = [trace]

plot_figure = go.Figure(data=data, layout=layout)

plotly.offline.plot(plot_figure)

#plot_figure.show()

input("press key")
