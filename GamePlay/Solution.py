#!/usr/bin/python

import signal
import sys

with open("input.txt","r") as fin:
    with open("output.txt","w") as fout:

        max_sum_p1=0
        max_sum_p2=0
        movep1=[]
        movep2=[]
        move=""
        sump1=0
        sump2=0
        llist=[]
        slist=[]
        common=[]
        spla=[]
        lahsa=[]

        count=0
        maxguesscom=0
        maxguessspla=0
        guess=""
        guess_spla=""
        odd=0
        test=0
        test2=0

        def handler(s, f):
            global guess
            fout.write(guess)
            sys.exit()
        def exitp(s,f):
            pass

        signal.signal(signal.SIGALRM, handler)
        signal.alarm(175)
        line=fin.read().splitlines()
        b=int(line[0])
        p=int(line[1])
        l=int(line[2])
        count=3
        for i in range(count,count+l):
            llist.append(line[i])
            count+=1
        s=int(line[count])
        count+=1
        for i in range(count,count+s):
            slist.append(line[i])
            count+=1

        a=int(line[count])
        count+=1
        alist=[]
        for i in range(count,count+a):
            alist.append(line[i])


        shelter=[b for i in range(7)]
        parking=[p for i in range(7)]
        week=[0 for i in range(7)]

        for j in range(len(slist)):
           for i in range(len(alist)):
               s=alist[i]
               if s[:5] == slist[j]:
                   day=s[13:20]
                   for z in range(7):
                       shelter[z]-=int(day[z])
                   alist.remove(alist[i])
                   break

        for j in range(len(llist)):
            for i in range(len(alist)):
               s=alist[i]
               if s[:5] == llist[j]:
                   day=s[13:20]
                   for z in range(7):
                       parking[z]-=int(day[z])
                   alist.remove(alist[i])
                   break

        daytest=parking[:]
        daytest2=shelter[:]


        for i in range(len(alist)):
            sum=0
            s=alist[i]
            day=s[13:20]
            for z in range(7):
                sum+=int(day[z])
            alist[i]=alist[i]+str(sum)
            if s[10]=='N' and s[11]=='Y' and s[12]=='Y' and s[9]=='N' and s[5]=='F' and (int(s[7:-11]) > 17):
                count+=1
                week[sum-1]+=1
                try:
                 if sum == maxguesscom:
                    if(int(guess)> int(s[:5])):
                       guess=str(s[:5])
                 if sum>maxguesscom:
                    maxguesscom=sum
                    guess=str(s[:5])
                except ValueError:
                   pass

            if s[10]=='N' and s[11]=='Y' and s[12]=='Y':
                for z in range(7):
                    daytest[z]-=int(day[z])
                spla.append(alist[i])

                try:
                 if guess_spla=="":
                    guess_spla=s[:5]
                 elif int(guess_spla) > int(s[:5]):
                    guess_spla=s[:5]
                except ValueError:
                   pass
            if s[9]=='N' and s[5]=='F' and (int(s[7:-11]) > 17):
                for z in range(7):
                    daytest2[z]-=int(day[z])
                lahsa.append(alist[i])


        for i in week:
            if i%2==1:
                odd=1

        for i in daytest:
            if i<0:
               test=1

        for i in daytest2:
            if i<0:
                test2=1



        guess=guess_spla




        for i in spla[:]:
            day=i[13:20]
            for j in range(7):
                if int(day[j]) > parking[j]:
                    spla.remove(i)
                    break

        for i in lahsa[:]:
            day=i[13:20]
            for j in range(7):
                if int(day[j]) > shelter[j]:
                    lahsa.remove(i)
                    break



        def play_spla(spla,lahsa,shelter,parking,first):
            global sump1,sump2,test
            max_sum_p1=0
            max_sum_p2=0
            move=""

            if (len(spla)==0) and (len(lahsa)==0):
                  return(sump1,sump2)

            for i in range(len(spla)):
                s=spla[i]
                t=spla[:]
                t1=lahsa[:]
                tparking=parking[:]
                t.remove(s)
                day=s[13:20]


                if test == 1:
                    for j in range(7):
                        tparking[j]-= int(day[j])

                    for z in t[:]:
                        day1=z[13:20]
                        for j in range(7):
                            if int(day1[j])>tparking[j]:
                                t.remove(z)
                                break

                if s in t1:
                    t1.remove(s)
                sump1+=int(s[20])
                if len(t1)==0:
                    (x,y)=play_spla(t,t1,shelter,tparking,0)
                else:
                    (x,y)=play_lahsa(t,t1,shelter,tparking)

                sump1-=int(s[20])

                if x==max_sum_p1:
                    if int(move[:5])> int(s[:5]):
                        move=s
                if x>max_sum_p1:
                    max_sum_p1=x
                    max_sum_p2=y
                    move=s


            if first==1:
                fout.write(move[:5])
            return (max_sum_p1,max_sum_p2)


        def play_lahsa(spla,lahsa,shelter,parking):
            global sump1,sump2,test2
            max_sum_p1=0
            max_sum_p2=0

            if (len(spla)==0) and (len(lahsa)==0):
                 return (sump1,sump2)

            for i in range(len(lahsa)):

                s=lahsa[i]
                t=lahsa[:]
                t1=spla[:]
                tshelter=shelter[:]
                day=s[13:20]
                t.remove(s)
                if s in t1:
                    t1.remove(s)

                if test2 == 1:
                    for j in range(7):
                        tshelter[j]-= int(day[j])

                    for z in t[:]:
                        day1=z[13:20]
                        for j in range(7):
                            if int(day1[j]) > int(tshelter[j]):
                                t.remove(z)
                                break

                sump2+=int(s[20])
                if len(t1)==0:
                    (x,y)=play_lahsa(t1,t,tshelter,parking)
                else:
                    (x,y)=play_spla(t1,t,tshelter,parking,0)

                sump2-=int(s[20])
                if y > max_sum_p2:
                   max_sum_p2=y
                   max_sum_p1=x
            return (max_sum_p1,max_sum_p2)

        play_spla(spla,lahsa,shelter,parking,1)
        signal.signal(signal.SIGALRM, exitp)
        signal.alarm(0)
