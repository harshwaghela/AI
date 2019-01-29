#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 14 16:40:35 2018

@author: harshwaghela
"""
import numpy as np
import time
import copy

start=time.time()

with open("input.txt","r") as fin:
    with open("output.txt","w") as fout:
        line=fin.read().splitlines()
        s=(int)(line[0])
        n=(int)(line[1])
        o=(int)(line[2])
        obstacle=[]
        cars=[]
        terminal=[]
        map1 = [([0] * s) for row in range(s)]
        reward = [([-1] * s) for row in range(s)]
        action=[([0] * s) for row in range(s)]
        for i in range(3,3+o):
             currentline = line[i].split(",")
             x = int(currentline[0])
             y = int(currentline[1])
             obstacle.append((y,x))
        for i in range(3+o,3+o+n):
             currentline[:]=[]
             currentline = line[i].split(",")
             x = int(currentline[0])
             y = int(currentline[1])
             cars.append((y,x))
        for i in range(3+o+n,3+o+n+n):
             currentline[:]=[]
             currentline = line[i].split(",")
             x = int(currentline[0])
             y = int(currentline[1])
             terminal.append((y,x))

        d=0.0
        g=0.9
        
        def turn_left(move):
            if move==1:
                return 4
            if move==2:
                return 3
            if move==3:
                return 1
            if move==4:
                return 2
            
        def turn_right(move):
          if move==1:
              return 3
          if move==2:
              return 4
          if move==3:
              return 2
          if move==4:
              return 1
        
        
        def cal(row,col,act):
                  lcol=col if col-1<0 else col-1
                  rcol=col if col+1>=s else col+1
                  lrow=row if row-1<0 else row-1
                  rrow=row if row+1>=s else row+1
                  if act==1:
                      return (row,lcol)
                  if act==2:
                      return (row,rcol)
                  if act==3:
                      return (lrow,col)
                  if act==4:
                      return (rrow,col)
        
        
        
        for z in range(len(cars)):
          map1 = [([0] * s) for row in range(s)]
          reward = [([-1] * s) for row in range(s)]
          for i in obstacle:
            (x,y)=i
            reward[x][y]-=100
          (x,y)=terminal[z]
          reward[x][y]+=100.0
          map1[x][y]=99.0
          action=[([0] * s) for row in range(s)]
          d=2
          c=np.float64((0.1*(1-g))/g)
          count=0

          while(d >= c):

              d=0
              map_old=copy.deepcopy(map1)
              
              for row in range(s):
                for col in range(s):

                  if row==x and col==y:
                      continue

                  
                  lcol=col if col-1<0 else col-1
                  rcol=col if col+1>=s else col+1
                  lrow=row if row-1<0 else row-1
                  rrow=row if row+1>=s else row+1

                  left=np.float64(0.7*map_old[row][lcol]+0.1*map_old[row][rcol]+0.1*map_old[lrow][col]+0.1*map_old[rrow][col])               
                  right=np.float64(0.1*map_old[row][lcol]+0.7*map_old[row][rcol]+0.1*map_old[lrow][col]+0.1*map_old[rrow][col])
                  up=np.float64(0.1*map_old[row][lcol]+0.1*map_old[row][rcol]+0.7*map_old[lrow][col]+0.1*map_old[rrow][col])
                  down=np.float64(0.1*map_old[row][lcol]+0.1*map_old[row][rcol]+0.1*map_old[lrow][col]+0.7*map_old[rrow][col])

#                  left=np.float64(0.7*map_old[row][lcol]+0.1*(map_old[row][rcol]+map_old[lrow][col]+map_old[rrow][col]))               
#                  right=np.float64(0.7*map_old[row][rcol]+0.1*(map_old[row][lcol]+map_old[lrow][col]+map_old[rrow][col]))
#                  up=np.float64(0.7*map_old[lrow][col]+0.1*(map_old[row][lcol]+map_old[row][rcol]+map_old[rrow][col]))
#                  down=np.float64(0.1*(map_old[row][lcol]+map_old[row][rcol]+map_old[lrow][col])+0.7*map_old[rrow][col])

                  maxi=max(left,right,up,down)

                  if maxi==up:
                      action[row][col]=3
                  elif maxi==down:
                      action[row][col]=4
                  elif maxi==right:
                      action[row][col]=2
                  elif maxi==left:
                      action[row][col]=1


                 
                  map1[row][col]=np.float64(reward[row][col] + g*maxi)

                  if abs(map1[row][col]-map_old[row][col]) > d:
                      d = abs(map1[row][col]-map_old[row][col])

     
        
          sump=0    
          for j in range(10):
                pos=cars[z]
                np.random.seed(j)
                swerve=np.random.random_sample(1000000)
                k=0
                sum1=0
                while pos != terminal[z]:
                    (x,y)=pos
                    move=action[x][y]
                    if swerve[k] > 0.7:
                                if swerve[k]>0.8:
                                    if swerve[k]>0.9:
                                        move=turn_left(turn_left(move))
                                        cal1=cal(x,y,move)
                                        (a,b)=cal1
                                        sum1+=reward[a][b]                                       
                                    else:
                                        move=turn_right(move)
                                        cal1=cal(x,y,move)
                                        (a,b)=cal1
                                        sum1+=reward[a][b]
                                else:
                                        move=turn_left(move)
                                        cal1=cal(x,y,move)
                                        (a,b)=cal1
                                        sum1+=reward[a][b]
                    else:
                     cal1=cal(x,y,move)
                     (a,b)=cal1
                     sum1+=reward[a][b]
                       
                    
                    pos=cal1
                               
                    k+=1
                    
                sump+=sum1
          ans=int(np.floor(np.float64(sump/10)))
          print(ans)
          fout.write(str(ans)+"\n")                

