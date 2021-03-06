from mpl_toolkits import mplot3d

#matplotlib inline
import numpy as np
import matplotlib.pyplot as plt
import helper as hlp
from sys import exit
from random import shuffle
from os.path import expanduser
import os_util as pt
import networkx as nx
from networkx.drawing.nx_pydot import graphviz_layout

def func23():
    path_to_file = "{}/{}".format(expanduser("~"),"/car_model/debug/p.csv")
    results = hlp.load__p(path_to_file)
    d={}
    for item in results:
        print(item)
        path = item["traj"]
        w = item["p"]
        for idx in range(len(path)-1):
            ky = (path[idx][0],idx)
            v = (path[idx+1][0],idx+1)
            if ky not in d:
                d[ky]= [v]
            else:
                d[ky].append(v)
    print(d)
    for item in d.keys():
        d[item]=list(set(d[item]))
    return d
def make_graph():
    res = func23()
    # print(results)
    G = nx.from_dict_of_lists(res)
    d_color = {0:'green',1:"blue",2:"red",3:"black",4:"yellow"}
    color_map = []
    for node in G:
        x = []
        if node in res:
            x = res[node]
        color = d_color[len(x)]
        color_map.append(color)

    # G = nx.from_dict_of_lists(dol)
    pos = nx.spring_layout(G, k=0.3 * 1 / np.sqrt(len(G.nodes())), iterations=20)
    plt.figure(3, figsize=(30, 30))
    nx.draw(G, pos=pos)
    # nx.draw_networkx_labels(G, pos=pos)
    # plt.show()
    pos = graphviz_layout(G, prog="dot")
    nx.draw(G, pos,node_color=color_map)
    plt.savefig("{}/car_model/debug/tree.png".format(expanduser("~")))
    plt.show()



def get_cmap(n, name='hsv'):
    '''Returns a function that maps each index in 0, 1, ..., n-1 to a distinct
    RGB color; the keyword argument name must be a standard mpl colormap name.'''
    return plt.cm.get_cmap(name, n)

def path_score(path_to_csv_file):
    l = hlp.load__p(path_to_csv_file)
    l_all = []
    acc=0
    for item in  l:
        l_all.append(np.array(item['traj']))
        acc+=float(item['p'])
        if acc>=1:
            break
    d={}
    for i,list_f1 in enumerate(l_all):
        for item in list_f1:
            item = item.flatten()
            item = tuple(item)
            if item in d:
                d[item]+=1
            else:

                d[item]=1
    ones = 0
    big_one=0
    for item in d.values():
        if item == 1:
            ones+=1
        else:
            big_one+=1
    #print("uniq - {}:{} -> {}".format(ones,big_one,ones/(big_one+ones)))

def main_f():
    cmap = get_cmap(15)

    p='car_model/debug'
    res = pt.walk_rec("{}/{}".format(expanduser("~"),p),[],"p.csv")
    res = [x for x in res if str(x).split('/')[-1].__contains__("map") is False]
    shuffle(res)
    index = 0
    path_score(res[index])
    # for i,x in enumerate(res):
    #     if str(res).split('/')[-1] == '31158_p.csv':
    #         index=i
    #         break
    print(res[index])
    l = hlp.load__p(res[index])

    print(l)
    matrix = []
    for item in l:
        size = len(item["traj"])
        path = np.zeros([size, 3])
        for idx, pos in enumerate(item["traj"]):
            path[idx] = pos[0]
        matrix.append(path)

    # exit(0)
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    # ax = plt.axes(projection='3d')

    # Data for a three-dimensional line
    color = ['red', 'green', 'gold', 'black', 'lime', 'violet', 'plum',
             'orange', 'navy', 'salmon']
    for i, p in enumerate(matrix):
        zline = np.array(p[:, 2])
        xline = np.array(p[:, 1])
        yline = np.array(p[:, 0])
        ax.plot3D(xline, yline, zline, color[i % len(color)])

    ax.view_init(azim=0, elev=100)

    plt.savefig("{}/car_model/debug/paths.png".format(expanduser("~")))
    plt.show()


if __name__ == "__main__":
    main_f()
    make_graph()