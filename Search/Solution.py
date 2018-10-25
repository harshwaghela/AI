#!/usr/bin/env python

max=0
count=0
summer=0
l=[]
t=[]
cm=[]
        
def col_max(map):
    
    for i in range(rows):
          colmax=0
          for j in range(cols):
               if colmax<map[i][j]:
                   colmax=map[i][j]
          cm.append(colmax)

def check(l,col):
    currsum=0
    currcol=0
    t[:]=[]

    currsum=summer
    for j in range(col,n):
        t.append(cm[j])
    t.sort(reverse=True)
    for i in range(p-len(l)):
        if (len(t) > i):
            currcol+=t[i]
    if currsum+currcol <= max:
        return False
    return True


def isSafe(l, row, col):
 
    
    for i in range(len(l)):
        (x,y)=l[i]
        if x==row or y==col or (x+y)==(row+col) or (x-y)==(row-col):
           return False
    return True

def solve(l,col):
    global summer,max
    
    if col > n-(p-len(l)):
        return
    
    if len(l)==p:
        if summer > max:
            max=summer
        return
    
    for i in range(col,n+1-(p-len(l))):
        flag=0
        for j in range(n):
            if check(l,i):    
                if isSafe(l,i,j):
                    summer+=map[i][j]
                    l.append((i,j))
                    solve(l,i+1)
                    l.remove((i,j)) 
                    summer-=map[i][j]
            else:
                flag=1
                break
        if flag==1:
            break

with open("input.txt","r") as filein:
    with open("output.txt", "w") as fileout:
         line = filein.read().splitlines()
         n= int(line[0])
         p=int(line[1])
         s=int(line[2])
         map = [ ([0] * n) for row in range(n) ]
         rows = len(map)
         cols = len(map[0])       
         i=3
         while i < len(line):
             currentline = line[i].split(",")
             x = int(currentline[0])
             y = int(currentline[1])
             map[x][y]+=1
             i+=1
         col_max(map)
         solve(l,0)
         fileout.write(str(max))
 
     