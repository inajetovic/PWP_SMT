Folder description:

Files:
-)SMT_base_model.py contains the application of the Base Model.

-)SMT_base_model_sb.py contains the application of the Base Model
with the SB constraint.

-)SMT_extended_model_sb.py contains the application of the Extended Model 
(with rotations and repetitions) with the SB constraint.

-)project_utils_final.py contains many useful functions to visualize solutions,
to deal with input and output data etc..

Usage:
In order to execute the code for an instance, assign its name to the string variable "filename".
(e.g.: filename="21x21.txt")
It is possible to visualize the solution by setting the variable "visualize" equal to True.
In the same fashion it is possible to plot the presents' area distribution and the number of 
all possible solutions of the instance (with the variables "plot_area" and "find_all_solutions"). 


Info for the Output folders creation:
To create the ouput instances folders, the models present in each file were simply rewrote as
functions and applied to the input instances folder. Example:
out_path= './smt_out_base/'
files = [str(i)+"x"+str(i) for i in range(25,30)]
for file in files:
    w,h,n,widths,heigths,posx,posy,_,_ = baseline_solver(file)
    with open(out_path+file+'.txt', 'w') as data:
                data.write(str(w)+' '+str(h)+'\n'
                          +str(n)+'\n'
                         )
                for i in range(0,n):
                    data.write(str(widths[i])+' '+str(heigths[i])+'\t'+str(posx[i])+' '+str(posy[i])+'\n')

When using the SB models and print the output instances, we need to use the function "reordering"
(present in the project_utils_final.py) since the presents' positions returned by the model function
are sorted according the area order and not like the input instances.