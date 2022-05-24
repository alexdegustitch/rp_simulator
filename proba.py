from tkinter import *
from tkinter.ttk import *
from math import sin
import tkinter
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from numpy import linspace
import utils
import networkx as nx
from tkinter import messagebox
from matplotlib.figure import Figure





root = Tk()

root.title("Reliability Polynomial Simulator")


G = nx.Graph(utils.graph_from_file())

# p probability
Label(root, text="Probability P:").grid(row=0, column=0)
probability_entry = Entry(root, width=5)
probability_entry.grid(row=0, column=1)

# U
Label(root, text="U:").grid(row=1, column=0)
u_entry = Entry(root, width=5)
u_entry.grid(row=1, column=1)


# label to show result of RP
label_rp = Label(root, text="")
label_rp.grid(row=2, column=1)

# S - Number of samples
Label(root, text="S:").grid(row=3, column=0)
s_entry = Entry(root, width=5)
s_entry.grid(row=3, column=1)



# label to show result of monte carlo simulation
label_test = Label(root, text="")
label_test.grid(row=4, column=1)

# number of vertices
Label(root, text="Enter number of vertices:").grid(row=5, column=0)
num_vertices_entry = Entry(root, width=5)
num_vertices_entry.grid(row=5, column=1)

# number of edges
Label(root, text="Enter number of edges:").grid(row=6, column=0)
num_edges_entry = Entry(root, width=5)
num_edges_entry.grid(row=6, column=1)

f = plt.figure(figsize=(9, 8))
a = f.add_subplot(111)
a.axis("off")
pos = nx.circular_layout(G)
nx.draw_networkx(G, pos=pos, ax=a, with_labels=True)

xlim = a.get_xlim()
ylim = a.get_ylim()

canvas = FigureCanvasTkAgg(f, master=root)
canvas.draw()
canvas.get_tk_widget().grid(row=9, column=0, columnspan=2, sticky=NSEW)



def update_graph(event=None):
    N = int(num_vertices_entry.get())
    M = int(num_edges_entry.get())
    global G
    G = nx.Graph(utils.graph(N, M))

    a.cla()
    nx.draw_networkx(G, pos=nx.circular_layout(G), ax=a, with_labels=True)
    a.set_xlim(xlim)
    a.set_ylim(ylim)
    a.axis("off")
    canvas.draw()

    return None


def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.quit()
        root.destroy()


def compute_rp(event=None):
    global root
    popup = Toplevel(root)
    root.eval(f'tk::PlaceWindow {str(popup)} center')
    Label(popup, text="Reliability Polynomial is being computed").grid(row=0,column=0)
    progress = 0
    progress_var = DoubleVar()
    progress_bar = Progressbar(popup, variable=progress_var, maximum=100)
    progress_bar.grid(row=1, column=0)
    popup.pack_slaves()

    
    res = 0
    U = int(u_entry.get())
    P = float(probability_entry.get())

    progress_step = float(100.0/U)
    for i in range(U):
        res += utils.reliability_polynomial(G, P)
        popup.update()
        progress += progress_step
        progress_var.set(progress)
    popup.destroy()
    
    res = res / U
    label_rp.configure(text=str(res))
    return None


def test_monte_carlo(event=None):
    res = 0
    S = int(s_entry.get())
    P = float(probability_entry.get())

    for i in range(S):
        res += utils.monte_carlo_method(G, P)
    res = res / S
    label_test.configure(text=str(res))
    return None

def generate_fun(event = None):
    global G
    global root

    popup = Toplevel(root)
    root.eval(f'tk::PlaceWindow {str(popup)} center')
    Label(popup, text="Reliability Polynomial is being drawn").grid(row=0,column=0)
    progress = 0
    progress_var = DoubleVar()
    progress_bar = Progressbar(popup, variable=progress_var, maximum=100)
    progress_bar.grid(row=1, column=0)
    popup.pack_slaves()

    p_values = linspace(0, 1, num=101)
    rp_values = []
    s = 100
    progress_step = float(100.0/s)
    for p in p_values:
        res = 0
        for i in range(s):
            res += utils.reliability_polynomial(G, p)
        res = res / s
        rp_values.append(res)
        popup.update()
        progress += progress_step
        progress_var.set(progress)
    popup.destroy()
    fig, ax = plt.subplots()
    ax.plot(p_values, rp_values)
    fig.show()
    

# RP button
buttonCalculateRP = Button(root, text="Compute RP", command=compute_rp)
buttonCalculateRP.grid(row=2, column=0)

# Test button
buttonMonteCarlo = Button(root, text="Test", command=test_monte_carlo)
buttonMonteCarlo.grid(row=4, column=0)

# Generate graph
buttonGenerateGraph = Button(root, text="Generate new Graph", command=update_graph)
buttonGenerateGraph.grid(row=7, column=1)

# Generate graph
buttonGenerateFun = Button(root, text="Generate function", command=generate_fun)
buttonGenerateFun.grid(row=8, column=1)

root.protocol("WM_DELETE_WINDOW", on_closing)
root.eval('tk::PlaceWindow . center')
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(2, weight=1)
root.mainloop()
