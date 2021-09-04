#  img= color / Grayscal; flag= FCM / ORFCM; C=3; #  E=0.01;  it=30
#--------------------------------------------------------------------
import cv2
from ttictoc import tic,toc
import numpy as np
from tkinter import *
from tkinter.ttk import *
def Clustering(C, img, flag, in_img, it, E):
    tic()
    global pro_cluster, top
    top =Toplevel()
    top.title('Process in Progress')
    pro_cluster=Progressbar(top, length=300, orient='horizontal', mode='determinate')
    pro_cluster.pack(padx=10, pady=10)
    percent = StringVar()
    percentlabel=Label(top, textvariable=percent).pack()
    PW=2/(2-1)
    if img == 'Color':    # color image processing
        X,Y,Z=in_img.shape   #in_img.shape[2]
        I_img = in_img.reshape((-1,3))
        I_img = np.float64(I_img)
        N=I_img.shape[0]
        U=np.zeros((N,C))
        Uc=np.zeros((N,C))
        D=np.zeros((N,C,Z))
        SD=np.zeros((N,C))
        ra=np.random.permutation(C+1)
        ra=ra[ra!= 0]
        ra=ra/sum(ra)
        ra=ra.reshape((1,ra.shape[0]))
        U[0:N,0:C]=ra[0:1,0:C]
        Index_sort = np.argsort(np.random.rand(N,C), axis=1)
        U=U[np.arange(Index_sort.shape[0])[:, None], Index_sort]
        Ci=np.zeros((C,Z))
        if flag=='ORFCM':
            B=(np.divide(np.sum(np.subtract(I_img.max(0),I_img.min(0)))+3,768))+1
        j=0
        while j<it:
            US=np.power(U, 1.0)
            U=np.power(U, 2.0)
            for k in range(Z):
                Uc[0:N,0:C]=U[0:N,0:C]*I_img[0:N,k:k+1]
                Ce=np.divide(sum(Uc),sum(U))
                ans=np.power(np.subtract(I_img[0:N,k:k+1],Ce),2.0)
                D[0:N,0:C,k:k+1] = ans.reshape((ans.shape[0],ans.shape[1],1))
                CE=Ce.reshape((Ce.shape[0],1))
                Ci[0:C,k:k+1]=CE
            T= np.sum(D, axis=-1)
            T= np.power(T,0.5)
            if flag=='ORFCM':
                Fu=B**T
            if flag=='FCM':
                Fu=T    
            FU=np.power(Fu,-PW)
            EA=np.sum(FU, axis = 1)
            EA=EA.reshape((EA.shape[0], 1))
            U[0:N,0:C]=FU[0:N,0:C]/EA[0:N,0:1]                
            SD=abs(np.subtract(U,US))
            EE=np.max(SD)
            if EE<=E:
                break
            j=j+1
            pro_cluster['value']+=100/it
            percent.set(str(int((j/it)*100))+'%')
            top.update_idletasks()
    if img == 'Grayscale':      # gray-scale image processing
        in_img=cv2.cvtColor(in_img, cv2.COLOR_BGR2GRAY)
        I_img = in_img.reshape((-1,1))
        I_img = np.float64(I_img)
        N=I_img.shape[0]    
        U=np.zeros((N,C))
        Uc=np.zeros((N,C))
        T=np.zeros((N,C))
        SD=np.zeros((N,C))
        ra=np.random.permutation(C+1)
        ra=ra[ra!= 0]
        rans=ra/sum(ra)
        rans=rans.reshape((1,rans.shape[0]))
        U[0:N,0:C]=rans[0:1,0:C]
        Index_sort = np.argsort(np.random.rand(N,C), axis=1)
        U=U[np.arange(Index_sort.shape[0])[:, None], Index_sort]
        if flag=='ORFCM':
            B=(np.divide(np.subtract(np.max(I_img),np.min(I_img))+1,256))+1 
        j=0
        while j<it:
            US=np.power(U, 1.0)
            U=np.power(U, 2.0)
            Uc[0:N,0:C]=U[0:N,0:C]*I_img
            Ci=np.divide(sum(Uc),sum(U))
            T=abs(np.subtract(I_img,Ci))
            if flag=='ORFCM':
                Fu=B**T
            if flag=='FCM':
                Fu=T
            FU=np.power(Fu,-PW)
            EA=np.sum(FU, axis = 1)
            EA=EA.reshape((EA.shape[0], 1))
            U[0:N,0:C]=FU[0:N,0:C]/EA[0:N,0:1]
            SD=abs(np.subtract(U,US))
            EE=np.max(SD)
            if EE<=E:
                break
            j=j+1
            pro_cluster['value']+=100/it
            percent.set(str(int((j/it)*100))+'%')
            top.update_idletasks()
    label=np.argmax(US, axis=1)
    center=Ci
    ret=np.sum(T)
    print(toc())
    top.destroy()
    return ret,label,center