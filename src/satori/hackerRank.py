'''
Created on May 20, 2017

@author: acer
'''
from pprint import pprint
def test():
    f=open('C:/vasan/HackerRank/test.txt')
    nN,nQ=map(int,f.readline().strip().split(' '))
    print (nN,nQ)
    NL=[0 for i in range(nN)]
    for j in range(nQ):
        a,b,k=map(int,f.readline().strip().split(' '))
        NL[a-1:b]=[NL[i]+k for i in range(a-1,b)]
        if j % 100 == 0:
            print(j)
    
    f.close()

def testNew():
    def createNewRange(RV,a,b,k):
        
        def Overlap(r0,r1,r2,a,b,k):
            #only give the segment of a,b,k over r0,r1,r2
            if b<r0 or a>r1:
                NV.append([r0,r1,r2])
                return #no overlap
            if a<=r0:
                if b>=r1: #complete overlap
                    NV.append([r0,r1,r2+k])
                else:
                    NV.append([r0,b,r2+k])
                    NV.append([b+1,r1,r2])
            else:
                if b >= r1:
                    NV.append([r0,a-1,r2])
                    NV.append([a,r1,r2+k])
                else:
                    NV.append([r0,a-1,r2])
                    NV.append([a,b,r2+k])
                    NV.append([b+1,r1,r2])
            
        NRV=[] #new RV
        for r in RV:
            NV=[]
            Overlap(r[0],r[1],r[2],a,b,k)
            NRV.extend(NV)
        return NRV
    #query based structures: Keeps range and value
    f=open('C:/vasan/HackerRank/test.txt')
    nN,nQ=map(int,f.readline().strip().split(' '))
    print (nN,nQ)
    RV = [[0,nN,0]] #start with one full zero range
    for j in range(nQ):
        a,b,k=map(int,f.readline().strip().split(' '))
        #print('starting:',RV,a,b,k)
        RV=createNewRange(RV,a,b,k)
        #RV.sort(key=lambda r:r[0]) 
        #pprint(RV)
        if j %100 == 0:
            print(j)
    f.close()
    return max([r[2] for r in RV])
    
if __name__ == '__main__':
    print (testNew())