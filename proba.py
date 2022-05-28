from calendar import c
from operator import ge
from textwrap import fill
import tkinter as tk
from tkinter import ttk
from tkinter.font import Font
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from numpy import linspace
import utils
import networkx as nx
from tkinter import messagebox
from matplotlib.figure import Figure
import re
import math



regex_float = re.compile("^(0|(0\.[0-9]+)|1)$")
regex_number = re.compile("^[1-9][0-9]*$")



root = tk.Tk()
root.resizable(False,False)

root.title("Reliability Polynomial Simulator")



font = Font(size = 12)
opt = tk.IntVar(value=None)
accuracy_popup = None
G = nx.Graph(utils.graph_from_file())
running_generate_fun = False
running_computing_rp = False
running_monte_carlo = False

# p probability
tk.Label(root, text="Probability P:", font=font).grid(row=0, column=0, sticky=tk.E, padx=(0, 10))
probability_entry = tk.Entry(root, width=5, font=font)
probability_entry.grid(row=0, column=1, sticky=tk.W,  padx=(10, 0))

# U
tk.Label(root, text="U:", font=font).grid(row=1, column=0, sticky=tk.E, padx=(0, 10))
u_entry = tk.Entry(root, width=5, font=font)
u_entry.grid(row=1, column=1, sticky=tk.W, padx=(10, 0))


# label to show result of RP
label_rp = tk.Label(root, text="", foreground='#00b4d9', font=font)
label_rp.grid(row=2, column=1, sticky=tk.W, padx=(10, 0))

# S - Number of samples
tk.Label(root, text="S:", font=font).grid(row=3, column=0, sticky=tk.E, padx=(0, 10))
s_entry = tk.Entry(root, width=5, font=font)
s_entry.grid(row=3, column=1, sticky=tk.W, padx=(10, 0))



# label to show result of monte carlo simulation
label_test = tk.Label(root, text="", foreground='#00b4d9', font=font)
label_test.grid(row=4, column=1, sticky=tk.W, padx=(10, 0))

frame = tk.Frame(root)
frame.grid(row=5, column=1, sticky=tk.W)
# number of vertices
tk.Label(root, text="Enter number of vertices:", font=font).grid(row=5, column=0, sticky=tk.E, padx=(0, 10))
num_vertices_entry = tk.Entry(frame, width=5, font=font)
num_vertices_entry.grid(row=0, column=0, sticky=tk.W, padx=(10, 0))

#error vertices
error_v_label = tk.Label(frame, text="", font = Font(size = 10), fg='red', width=35)
error_v_label.grid(row =0, column=1, sticky=tk.W)

# number of edges
tk.Label(root, text="Enter number of edges:", font=font).grid(row=6, column=0, sticky=tk.E, padx=(0, 10))
num_edges_entry = tk.Entry(root, width=5, font=font)
num_edges_entry.grid(row=6, column=1, sticky=tk.W, padx=(10, 0))

f = plt.figure()
a = f.add_subplot(111)
a.axis("off")
pos = nx.circular_layout(G)
nx.draw_networkx(G, pos=pos, ax=a, with_labels=True, node_color='#00b4d9')

xlim = a.get_xlim()
ylim = a.get_ylim()

canvas = FigureCanvasTkAgg(f, master=root)
canvas.draw()
canvas.get_tk_widget().grid(row=9, column=0, columnspan=2, padx=0, pady=0)

root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.quit()
        root.destroy()

def on_closing_generate_fun():
    global running_generate_fun
    running_generate_fun = False

def on_closing_compute_rp():
    global running_computing_rp
    running_computing_rp = False

def on_closing_monte_carlo():
    global running_monte_carlo
    running_monte_carlo = False

def update_graph(event=None):
    global G
    N = int(num_vertices_entry.get())
    M = int(num_edges_entry.get())

    if N > 40:
        error_v_label.config(text  = "Number of vertices cannot be higher than 40.")
        return None
    error_v_label.config(text  = "")
    G = nx.Graph(utils.graph(N, M))

    a.cla()
    nx.draw_networkx(G, pos=nx.circular_layout(G), ax=a, with_labels=True, node_color='#00b4d9')
    a.set_xlim(xlim)
    a.set_ylim(ylim)
    a.axis("off")
    canvas.draw()

    return None


def compute_rp(event=None):
    global root, running_computing_rp
    running_computing_rp = True
    popup = tk.Toplevel(root)
    popup.grab_set()
    popup.protocol("WM_DELETE_WINDOW", on_closing_compute_rp)
    root.eval(f'tk::PlaceWindow {str(popup)} center')

    tk.Label(popup, text="Reliability Polynomial is being computed").grid(row=0,column=0)
    progress = 0
    progress_var = tk.DoubleVar()
    progress_bar = ttk.Progressbar(popup, variable=progress_var, maximum=100)
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
        if not running_computing_rp:
            popup.destroy()
            return
    popup.destroy()
    
    res = res / U
    res = format(res, ".6f")
    label_rp.configure(text=str(res))
    return None


def test_monte_carlo(event=None):
    global root, running_monte_carlo
    running_monte_carlo = True
    popup = tk.Toplevel(root)
    popup.grab_set()
    popup.protocol("WM_DELETE_WINDOW", on_closing_monte_carlo)
    root.eval(f'tk::PlaceWindow {str(popup)} center')

    tk.Label(popup, text="Monte Carlo simulation in process").grid(row=0,column=0)

    progress = 0
    progress_var = tk.DoubleVar()
    progress_bar = ttk.Progressbar(popup, variable=progress_var, maximum=100)
    progress_bar.grid(row=1, column=0)
    popup.pack_slaves()

    res = 0
    S = int(s_entry.get())
    P = float(probability_entry.get())

    progress_step = float(100.0/S)
    for i in range(S):
        res += utils.monte_carlo_method(G, P)
        popup.update()
        progress += progress_step
        progress_var.set(progress)
        if not running_monte_carlo:
            popup.destroy()
            return
    popup.destroy()

    res = res / S
    res = format(res, ".6f")
    label_test.configure(text=str(res))
    return None

def generate_fun(event = None):    
    global G, root, accuracy_popup, running_generate_fun
    running_generate_fun = True
    accuracy_popup.destroy()
    popup = tk.Toplevel(root)
    popup.grab_set()
    popup.protocol("WM_DELETE_WINDOW", on_closing_generate_fun)
    #root.eval(f'tk::PlaceWindow {str(popup)} center')
    root.eval(f'tk::PlaceWindow {str(popup)} center')
    tk.Label(popup, text="Reliability Polynomial is being drawn").grid(row=0,column=0)
    progress = 0
    progress_var = tk.DoubleVar()
    progress_bar = ttk.Progressbar(popup, variable=progress_var, maximum=100)
    progress_bar.grid(row=1, column=0)
    popup.pack_slaves()

    p_values = linspace(0, 1, num=101)
    rp_values = []
    accuracy = "small"
    s = 50
    if opt.get() == 2:
        s = 500
        accuracy = "medium"
    elif opt.get() == 3:
        s = 1000
        accuracy = "high"
    
    M = G.number_of_edges()
    N = G.number_of_nodes()
    n_i_coeficient = [0 for i in range(0, M + 1)]

    progress_step = float(100.0/s)
    for _ in range(s):
        coeficients = utils.get_polynomial(G)
        for i in range(N - 1, M + 1):
            n_i_coeficient[i] += coeficients[i]
        popup.update()
        progress += progress_step
        progress_var.set(progress)
        if not running_generate_fun:
            popup.destroy()
            return
    for i in range(N - 1, M + 1):
            n_i_coeficient[i] = n_i_coeficient[i]/s

    for p in p_values:
        res = 0
        for i in range(len(n_i_coeficient)):
            num = n_i_coeficient[i] * math.pow(p, i) * math.pow(1 - p, M - i)
            res += num
        rp_values.append(res)
    
        if not running_generate_fun:
            popup.destroy()
            return
    
    popup.destroy()
    fig, ax = plt.subplots()
    fig.canvas.manager.set_window_title('Function of reliability polynomial - ' + accuracy  +' accuracy')
    #fig.suptitle('Function of reliability polynomial - ' + accuracy  +' accuracy',fontsize = 12)
    ax.set_xlabel(r'$p$')
    ax.set_ylabel(r'$Rel(G;p)$')
    ax.set_xlim([0, 1])
    ax.set_ylim([0, 1])
    ax.plot(p_values, rp_values, color='#00b4d9')
    fig.show()


def accuracy_fun(event = None):
    global root, opt, accuracy_popup
    accuracy_popup = tk.Toplevel(root)
    accuracy_popup.grab_set()
    tk.Label(accuracy_popup, text = "Choose accuracy").pack(anchor=tk.W)
    opt.set(2)
    root.eval(f'tk::PlaceWindow {str(accuracy_popup)} center')

    
    R1 = tk.Radiobutton(accuracy_popup, text="Small", variable=opt, value=1)
    R1.pack(anchor=tk.W)

    R2 = tk.Radiobutton(accuracy_popup, text="Medium", variable=opt, value=2)
    R2.pack(anchor=tk.W)

    R3 = tk.Radiobutton(accuracy_popup, text="High", variable=opt, value=3)
    R3.pack(anchor=tk.W)

    button = tk.Button(accuracy_popup, text="Generate function", command=generate_fun)
    button.pack(anchor=tk.W)
    accuracy_popup.resizable(False, False)


# RP button
buttonCalculateRP = tk.Button(root, text="Compute RP", command=compute_rp, state=tk.DISABLED, font=font)
buttonCalculateRP.grid(row=2, column=0, sticky=tk.E, padx=(0, 10))

# Test button
buttonMonteCarlo = tk.Button(root, text="Test", command=test_monte_carlo, state = tk.DISABLED, font=font)
buttonMonteCarlo.grid(row=4, column=0, sticky=tk.E, padx=(0, 10))

# Generate graph
buttonGenerateGraph = tk.Button(root, text="Generate new Graph", command=update_graph, state = tk.DISABLED, font=font)
buttonGenerateGraph.grid(row=7, column=1, sticky=tk.W, padx=(10, 0))

# Generate graph
buttonGenerateFun = tk.Button(root, text="Generate function", command=accuracy_fun, font=font)
buttonGenerateFun.grid(row=8, column=1, sticky=tk.W, padx=(10, 0))

# regex check
probability_ok = False
u_ok = False
s_ok = False

vertices_ok = False
edges_ok = False

def key_p(event):
    global probability_ok, u_ok, buttonCalculateRP, s_ok
    entry =  probability_entry.get()
    if regex_float.match(entry) != None:
        probability_ok = True
    else:
        probability_ok = False
    state = str(buttonCalculateRP['state'])
    if probability_ok and u_ok:
        if state == tk.DISABLED:
            buttonCalculateRP['state'] = tk.NORMAL
    elif state != tk.DISABLED:
        buttonCalculateRP['state'] = tk.DISABLED

    state = str(buttonMonteCarlo['state'])
    if probability_ok and s_ok:
        if state == tk.DISABLED:
            buttonMonteCarlo['state'] = tk.NORMAL
    elif state != tk.DISABLED:
        buttonMonteCarlo['state'] = tk.DISABLED

    return

def key_u(event):
    global probability_ok, u_ok, buttonCalculateRP
    entry =  u_entry.get()
    if regex_number.match(entry) != None:
        u_ok = True
    else:
        u_ok = False
    state = str(buttonCalculateRP['state'])
    if probability_ok and u_ok:
        if state == tk.DISABLED:
            buttonCalculateRP['state'] = tk.NORMAL
    elif state != tk.DISABLED:
        buttonCalculateRP['state'] = tk.DISABLED
    return

def key_s(event):
    global buttonMonteCarlo, s_ok, probability_ok
    entry = s_entry.get()
    if regex_number.match(entry) != None:
        s_ok = True
    else:
        s_ok = False

    state = str(buttonMonteCarlo['state'])
    if probability_ok and s_ok:
        if state == tk.DISABLED:
            buttonMonteCarlo['state'] = tk.NORMAL
    elif state != tk.DISABLED:
        buttonMonteCarlo['state'] = tk.DISABLED
    return

def key_vertices(event):
    global edges_ok, vertices_ok
    entry = num_vertices_entry.get()
    if regex_number.match(entry) != None:
        vertices_ok = True
    else:
        vertices_ok = False
    
    state = str(buttonGenerateGraph['state'])
    if vertices_ok and edges_ok:
        if state == tk.DISABLED:
            buttonGenerateGraph['state'] = tk.NORMAL
    elif state != tk.DISABLED:
        buttonGenerateGraph['state'] = tk.DISABLED
    
    return

def key_edges(event):
    global edges_ok, vertices_ok
    entry = num_edges_entry.get()
    if regex_number.match(entry) != None:
        edges_ok = True
    else:
        edges_ok = False

    state = str(buttonGenerateGraph['state'])
    if vertices_ok and edges_ok:
        if state == tk.DISABLED:
            buttonGenerateGraph['state'] = tk.NORMAL
    elif state != tk.DISABLED:
        buttonGenerateGraph['state'] = tk.DISABLED
    return

probability_entry.bind('<KeyRelease>', key_p)
u_entry.bind('<KeyRelease>', key_u)
s_entry.bind('<KeyRelease>', key_s)
num_vertices_entry.bind('<KeyRelease>', key_vertices)
num_edges_entry.bind('<KeyRelease>', key_edges)


root.protocol("WM_DELETE_WINDOW", on_closing)
root.eval('tk::PlaceWindow . center')
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(2, weight=1)
root.mainloop()
