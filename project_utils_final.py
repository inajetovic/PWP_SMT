#Authors: Luca Bolognini & Matteo Antonio Inajetovic

from matplotlib.patches import Rectangle
import matplotlib.pyplot as plt
import os
import numpy as np
from numpy.core.fromnumeric import argmax
import pandas as pd
################# Parameters #########################
path = './Instances/'
data_path='./Instances_fin/'
output_smt_path_ext='./smt_out_extended/'
output_smt_path_base='./smt_out_base/'
elem = os.listdir(path)

###################### Methods ######################
def data_file_reader (read_path, file, sol = False):
    print('Reading Data files, wait...\n')

    with open(read_path + file, 'rt', ) as f:
        if not sol:
            line = f.readlines()
            lines= [line[i].split() for i in range(len(line))]
            widths = [lines[i][0] for i in range(2,len(lines)-2)]
            heights  = [lines[i][1] for i in range(2,len(lines)-2)]
            posx = None
            posy = None
        else:
            line = f.readlines()
            lines= [line[i].split() for i in range(len(line))]
            widths = [lines[i][0] for i in range(2,len(lines))]
            heights  = [lines[i][1] for i in range(2,len(lines))]
            posx = [lines[i][2] for i in range(2,len(lines))]
            posy = [lines[i][3] for i in range(2,len(lines))]
        
    w = lines[0][0]
    h = lines[0][1]
    n = lines[1][0]

    return w, h, n, widths, heights, posx, posy

def output_writer(read_path, write_path, sol_source, ext='.txt', rot =False):
    
    if rot:
        fl= pd.read_excel(io= sol_source, names=['X','Y','R'])
    else:
        fl= pd.read_excel(io= sol_source, names=['X','Y'])
    r = 0
    for file in os.listdir(read_path): 
        w, h, n, widths, heights,_,_ = data_file_reader(read_path, file)
        x = fl['X'][r].split(',')
        y = fl['Y'][r].split(',')
        if rot:
            rotation = fl['R'][r].split('r')
            rotation.reverse()
        x.reverse()
        y.reverse()
        with open(write_path + w +'x'+ h +'-out'+ ext, 'w') as out:
            out.write( w +' '+ h +'\n' 
                     + n + '\n')
            for i in range(0, int(n)):
                if not rot:
                    out.write(widths[i] +' '+ heights[i] +'  '+ x[i] +' '+ y[i]+'\n')
                else:
                    out.write(widths[i] +' '+ heights[i] +'  '+ x[i] +' '+ y[i]+ rotation[i] +'\n')
        r+=1

def solution_output (path, file_name = "every"):

    """Path = directory containing the solution
     File name = "LxL-out.txt" where l is the paper length, if default or "every" then all solution are sequentially inspected"""


    if file_name == "every": 
        for file in os.listdir(path):
            output_visualizer(path, file)
    else:
            output_visualizer(path, file_name)

def output_visualizer (out_path, file_name = "8x8-out.txt", border_reduction = 0.15):

    """
    visualizes the solutions given the path containing the output instances with the positions solutions
    """
    dim, _, _, width, height,posx,posy = data_file_reader(out_path, file_name, sol = True)
    
    colors = ['blue','green','yellow','red','orange',
              'purple','black','pink', 'cyan','gold',
              'silver','indigo', 'aquamarine', 'beige',
              'magenta','teal','aqua', 'lavender',
              'crimson', 'orchid']

    rotations = np.zeros(len(posx))

    fig = plt.figure()
    ax = fig.add_subplot(111)

    for i in range(len(posx)):
        if rotations[i]:
            rect = Rectangle((int(posx[i]), int(posy[i])), float(height[i])-border_reduction, float(width[i])-border_reduction, color = colors[i % len(colors)], ec ='black', label = i+1)
        else:
            rect = Rectangle((int(posx[i]), int(posy[i])), float(width[i])-border_reduction, float(height[i])-border_reduction, color = colors[i % len(colors)], ec ='black', label = i+1)
       
        ax.add_patch(rect)
    
    plt.title(dim + 'x' + dim)
    plt.xlim(-0.15,float(dim) +1.25)
    plt.ylim(-0.15,float(dim) +1.25) 
    #plt.legend()
    plt.show()

def solution_visualizer (posx, posy, width, height, dim,rotations):
    """
    visualizes a solution given the positions obtained with the solver
    """
    colors = [  'blue','green','yellow','red','orange',
                'purple','black','pink', 'cyan','gold',
                'aqua','indigo', 'aquamarine', 'beige',
                'magenta','teal','silver', 'lavender',
                'crimson', 'orchid']
    
    fig = plt.figure()
    ax= fig.add_subplot(111)

    for i in range(len(posx)):
       if rotations[i]==True:
           print('Present {} with w = {} and h = {} has been rotated'.format(i,width[i], height[i]))
           rect = Rectangle((posx[i], posy[i]),height[i] , width[i], color = colors[i % len(colors)],label=i, ec ='white')
           ax.add_patch(rect)
       else:
           rect = Rectangle((posx[i], posy[i]), width[i], height[i], color = colors[i % len(colors)], label=i,ec ='white')
           ax.add_patch(rect)
           
    plt.xlim(0,dim)
    plt.ylim(0,dim)
    plt.legend()
    plt.show()

def reordering(sizes,widths,heights,resx,resy,n):
    """
    function implemented to reorder the positions results when using the SB constraint
    to output the results sorted like the input instances.
    """
    new_widths = [i for i,_ in sizes]
    new_heights = [i for _,i in sizes]

    posx=[]
    posy=[]
    for a,b in zip(widths,heights):
        for i in range(n):
            if a == new_widths[i] and b == new_heights[i]:
                x=resx[i]
                y=resy[i]
        posx.append(x)
        posy.append(y)

    return posx,posy


###########CALL UTILS#############       
solution_output(output_smt_path_ext, "every")

#print('DONE')

