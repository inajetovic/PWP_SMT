#Authors: Luca Bolognini & Matteo Antonio Inajetovic
 
                                       #### Libraries ####

from project_utils_final import data_file_reader,solution_visualizer
import numpy as np
from z3 import *
import matplotlib.pyplot as plt
from operator import itemgetter

                                    #### Inputs & Variables ####
#instance file name
filename="20x20.txt"
#Boolean variable to find all the solutions for the instance
#Notice that for instances with w>16 the time needed to compute all the possible solutions is huge
#The same thing is valid for the extended model.
find_all_solutions = False
#Boolean variable to plot the area distribution of the instance
plot_area = True
#Boolean variable to visualize the solution
visualize = True
#Path for the input instances
instances_path= './Instances/'

dims=2
w, h, n, widths, heights,_,_ = data_file_reader(instances_path,filename,sol=False)
n=int(n)
w=int(w)
h=int(h)
widths  = [int(w) for w in widths]
heights = [int(h) for h in heights]

#Reordering of the widths and heights arrays, in order to take the bigger present at the first position
#the new array features contains width,height and area for each present
features=[[a,b,a*b] for a,b in zip(widths,heights)]
features=sorted(features, key=itemgetter(2)) #sort by area
features.reverse()
dimensions = [[a,b] for a,b,_  in features]
#print('Dimensions of pieces',Sizes)

                                   #### Decision Variables ####
#Position Decision Variable
Pos = [ [ Int("R_piece{}_pos{}".format(id, dim+1)) for dim in range(dims) ] for id in range(n) ]
#Dimension Decision Variable
Sizes = [[ Int("D_piece{}_dim{}".format(id, dim+1)) for dim in range(dims) ] for id in range(n)]
#Rotation Decision Variable
a = [ Bool ("A_piece{}".format(id)) for id in range(n)]

                                      #### Constraints #####

#rotation:
#if the rotation decision variable is true then the present is rotated, otherwise preserves its dimensions
rotation_c = [If (a[i]==True,And(Sizes[i][0]==dimensions[i][1],Sizes[i][1]==dimensions[i][0]),
                             And(Sizes[i][0]==dimensions[i][0],Sizes[i][1]==dimensions[i][1])) for i in range(n)]

#lexicographic constraint for repetitions
lex_c = [If (And(Sizes[i][0] == Sizes[j][0],Sizes[i][1] == Sizes[j][1]),
                    And(Pos[i][0]<=Pos[j][0], Implies(Pos[i][0]==Pos[j][0],Pos[i][1]<Pos[j][1]),
                        Pos[i][1]<=Pos[j][1], Implies(Pos[i][1]==Pos[j][1],Pos[i][0]<Pos[j][0])),Sizes[i][0]>=0) for j in range(n) 
                                                                                                                 for i in range(n)
                                                                                                                 if i<j]
#domains, with Symmetry Breaking constraint
domain_c = [If (i==0, And(Pos[i][0] <= (w - Sizes[i][0])/2, Pos[i][1] <= (h - Sizes[i][1])/2, Pos[i][0] >= 0, Pos[i][1] >= 0), 
                    And(Pos[i][0] >= 0 , Pos[i][1] >= 0, Pos[i][0] < w, Pos[i][1] < h))                          for i in range(n)]


#The gift's placement should not exceed the wrapping paper
boundaries_c = [  And ( Pos[i][1]+Sizes[i][1] <= h, Pos[i][0]+Sizes[i][0] <= w) for i in range(n)]

#no_overlap btw rectangles
no_overlap_c = [ Or (Pos[i][0]+Sizes[i][0] <= Pos[j][0], Pos[i][0] >= Pos[j][0]+Sizes[j][0],
                Pos[i][1]+Sizes[i][1] <= Pos[j][1], Pos[i][1] >= Pos[j][1]+Sizes[j][1]) for j in range(n) 
                                                                                        for i in range(n)
                                                                                        if i<j]
#implied
#over vertical lines
impliedc_c= [ Sum( [ If( And(i<Pos[r][0]+Sizes[r][0],i>= Pos[r][0]), Sizes[r][1], 0 ) for r in range(n)]) <= h
                                                                                                    for i in range(w)]

#over horizontal lines
impliedr_c= [ Sum( [ If( And(i<Pos[r][1]+Sizes[r][1],i>= Pos[r][1]), Sizes[r][0], 0 ) for r in range(n)] ) <= w
                                                                                                    for i in range(h)]
                                               #####   Solving Part   #####
print("Solving...")
solver = Solver()

solver.add(rotation_c + domain_c + boundaries_c + no_overlap_c + impliedc_c + impliedr_c + lex_c)

print('Satisfiable?:',solver.check())
sol=solver.model()
print(solver.statistics())

# solution for the positions
r = [sol.evaluate(Pos[i][j]) for i in range(n) for j in range(dims)]
resx=[]
resy=[]
for i in range(0, len(r)):
    if i % 2:
        resy.append(r[i].as_long())
    else :
        resx.append(r[i].as_long())

print('X coordinates',resx)
print('Y coordinates',resy)


### Evaluation for the rotation decision variable
rots=[sol.evaluate(a[i]) for i in range(n)]


st = solver.statistics()
time = st.get_key_value('time') #time needed for the solving procedure


##########                      Areas Distirbution Histogram Plot
if plot_area:
    _ = plt.hist([w*h for w,h in zip(widths,heights)], bins='auto')
    plt.show()

##########                    Number of all solutions for the instance

if find_all_solutions:
    counter=0
    while solver.check() == sat :
        sol=solver.model()
        print(solver.check())
        print(counter)
        
        #each time the problem is solved, we add a constraint to avoid solutions aldready found
        solver.add([Or([Pos[i][j] != sol.eval(Pos[i][j], model_completion=True) for i in range(n) for j in range(dims)])])
        counter+=1

    print('Number of different solutions found:',counter)

###########                   Visualization
if visualize:
    print("Visualizing the solution:")
    ### we need to reorder the widths and heigths arrays to plot correctly the solution 
    new_widths  = [i for i,_ in dimensions]
    new_heights = [i for _,i in dimensions]
    solution_visualizer(posx=resx,posy=resy,width=new_widths,height=new_heights,dim=w,rotations=rots)




