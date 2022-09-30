#Authors: Luca Bolognini & Matteo Antonio Inajetovic

                                       #### Libraries ####

from project_utils_final import data_file_reader,solution_visualizer
import numpy as np
from z3 import *
import matplotlib.pyplot as plt


                                    #### Inputs & Variables ####
#instance file name
filename="37x37.txt"
#boolean variable to find all the solutions for the instance
#notice that for instances with w>16 the time needed to compute all the possible solutions is huge
find_all_solutions = False
#boolean variable to plot the area distribution of the instance
plot_area = False
#boolean variable to visualize the solution
visualize = True
#path for the input instances
instances_path= './Instances/'

dims=2
w, h, n, widths, heights,_,_ = data_file_reader(instances_path,filename,sol=False)
n=int(n)
w=int(w)
h=int(h)
widths  = [int(w) for w in widths]
heights = [int(h) for h in heights]
Sizes = [[a,b] for a,b  in zip(widths,heights)]

                                   #### Decision Variables ####
Pos = [ [ Int("R_piece{}_pos{}".format(id, dim+1)) for dim in range(dims) ] for id in range(n) ]

                                      #### Constraints #####
#domains
domain_c = [  And (Pos[i][0] >= 0 , Pos[i][1] >= 0, Pos[i][0] < w, Pos[i][1] < h)  for i in range(n)]

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

solver.add( domain_c + boundaries_c + no_overlap_c + impliedc_c + impliedr_c)

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


### array of all Falses for the "solution_visualizer"
rots = np.zeros(n,dtype="bool") 

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

if visualize:
    print("Visualizing the solution:")
    solution_visualizer(posx=resx,posy=resy,width=widths,height=heights,dim=w,rotations=rots)



