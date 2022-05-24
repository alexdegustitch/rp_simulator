import datetime

import matplotlib.pyplot as plt
import networkx as nx
from numpy import double

import utils

p = double(input())
s = int(input())

G = utils.graph_from_file()
""""
nx.draw_circular(G, with_labels=True)
plt.show()
"""
res_rp = 0
res_test = 0
a = datetime.datetime.now()
for i in range(s):
    res_rp += utils.reliability_polynomial(G, p)
res_rp = res_rp / s
b = datetime.datetime.now()
c = b - a
print("RP:", res_rp, "TIME:", c.seconds, "sekundi i", c.microseconds, "mikrosekundi")

a = datetime.datetime.now()
for i in range(s):
    res_test += utils.monte_carlo_method(G, p)
res_test = res_test / s
b = datetime.datetime.now()
c = b - a
print("MC:", res_test, "TIME:", c.seconds, "sekundi i", c.microseconds, "mikrosekundi")


