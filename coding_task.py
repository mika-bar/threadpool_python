# -*- coding: utf-8 -*-
"""
main program

@author: mbar
"""

import math
import numpy as np
import time


from FuncsAndClassPckg.classes import ThreadPool
from FuncsAndClassPckg.functions import create_rand_mat,mult_matrices,mult_row_col,mult_sub_matrix
from ConfigPckg import config


def main():
    
    num_of_threads=int(input("How many threads would you like to create? enter a number between 2-20: "))
    
    while True:
        
        num_of_matrices=int(input("How many matrices? please enter at least 2: "))
        dimension= int(input("Which dimension? please enter a number: "))
        
        config.stop_thread=False
        matrices_arr=[]
        args_list=[]
        res_mat=np.zeros((dimension,dimension),int)
        thread_pool= ThreadPool(num_of_threads)
        
        for i in range(num_of_matrices):
            mat=create_rand_mat(dimension)
            matrices_arr.append(mat.tolist())
            print(f"Matrix number{i}:\n{matrices_arr[i]}")

        if num_of_threads >= dimension**2 :
            # do output decomposition- mult row with col of each pair of matrices
            func = mult_row_col

            for i in range(num_of_matrices):
                if i+1==num_of_matrices:
                    break
                res_mat=np.zeros((dimension,dimension),int)
                args_list=[]
                for j in range(dimension):
                    for k in range(dimension):
                        row1 = list(matrices_arr[i][j])
                        col1 = [row[k] for row in matrices_arr[i+1]]
                        args = row1,col1,dimension,res_mat,j,k
                        args_list.append(args)
                
                thread_pool.map1(func,args_list)
                time.sleep(0.001)
                matrices_arr[i+1]=res_mat
            
            time.sleep(0.001)
            config.stop_thread=True 
            thread_pool.wait_for_completion()    
            print("Result matrix:\n{}".format(res_mat))


        elif num_of_threads > dimension:
            # divide left matrix to #dimension parts
            func= mult_matrices
            
            for i in range(num_of_matrices):
                if i+1==num_of_matrices:
                    break
                res_mat=np.zeros((dimension,dimension),int)
                args_list=[]
                for j in range(dimension):
                    args = matrices_arr,dimension,i,i+1,j,j+1,res_mat
                    args_list.append(args)

                thread_pool.map1(func,args_list)
                time.sleep(0.001)
                matrices_arr[i+1]=res_mat
            
            time.sleep(0.001)
            config.stop_thread=True 
            thread_pool.wait_for_completion()
            print("Result matrix:\n{}".format(res_mat))

        else:
            # divide left matrix to threads number
            func= mult_sub_matrix
            
            for i in range(num_of_matrices):
                if i+1==num_of_matrices:
                    break
                res_mat=np.zeros((dimension,dimension),int)
                args_list=[]
                ranges=[range(dimension)[k*math.floor(dimension/num_of_threads) +min(k,dimension%num_of_threads):
    (k+1)*math.floor(dimension/num_of_threads) +min(k+1,dimension%num_of_threads)] for k in range(num_of_threads)]
                for wanted_range in ranges:
                    args = matrices_arr,dimension,i,i+1,wanted_range,res_mat
                    args_list.append(args)

                thread_pool.map1(func,args_list)
                time.sleep(0.1)
                matrices_arr[i+1]=res_mat
            
            time.sleep(0.001)
            config.stop_thread=True 
            thread_pool.wait_for_completion()
            print("Result matrix:\n{}".format(res_mat))

        keep_going=input("do you want to continue? y/n: ")

        if keep_going.lower()=='n':
            break
    return

if __name__ == "__main__":
    main()
    














