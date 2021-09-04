import cv2
import numpy as np
import Fuzzy_means as fz
from tkinter import *
from tkinter.ttk import *
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import font
from PIL import Image, ImageTk
global file_path
file_path = []
def Openfile():
    global file_path
    file_path =  filedialog.askopenfilename(initialdir = "/home/fasahat/pCloudDrive/MyPictures/",title = "Select file to open",filetypes = [("picture","*.jpg .png .tif .bmp .gif"),("all files","*.*")])
    #file_path =  filedialog.askopenfilename(initialdir = "P:\MyPictures",title = "Select file to open",filetypes = [("picture","*.jpg .png .tif .bmp .gif"),("all files","*.*")])
    image = Image.open(file_path)
    canvas_in.image = ImageTk.PhotoImage(image.resize((170, 195), Image.ANTIALIAS))
    canvas_in.create_image(0, 0, image=canvas_in.image, anchor='nw')
    img = cv2.imread(file_path)
    SS=img.shape
    my_text = tk.Text(bottom_right, height=1, width=16)
    my_text.grid(row=0, column=0)
    my_text.insert(tk.END, str(SS))

def Savefile():
    filedialog.asksaveasfilename(initialdir = "/", title = "Save file as",filetypes = [("picture","*.png"),("all files","*.*")])
    #filedialog.asksaveasfilename(initialdir = "P:\", title = "Save file as",filetypes = [("picture","*.png"),("all files","*.*")])
def Dis_input():
    global T_img
    top=Toplevel()
    top.title("Input Image")
    T_img=ImageTk.PhotoImage(Image.open(file_path))
    T_label=tk.Label(top,image=T_img).pack()
    Exit_button2 =tk.Button(top, text="Exit", command=top.destroy).pack()
    
def Segmentation():
    global tempfile_path
    #tempfile_path="/home/fasahat/pCloudDrive/MyPictures/temp_file.png"
    tempfile_path='P:\MyPictures\temp_file.png'
    file_path
    if len(file_path) > 0:
        img = cv2.imread(file_path)
        if Type == 'Color':
            in_img = img
            if Method == 'KM':
                i_img = img.reshape((-1,3)) # color
                i_img = np.float32(i_img)
                criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, It, EE)
                ret,label,center=cv2.kmeans(i_img,K,None,criteria,It,cv2.KMEANS_RANDOM_CENTERS)
            else:
                ret,label,center = fz.Clustering(K, Type, Method, img, It, EE)
        if Type == 'Grayscale':
            in_img=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            if Method == 'KM':                
                i_img =in_img.reshape((-1,1)) # grayscale
                i_img = np.float32(i_img)
                criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, It, EE)
                ret,label,center=cv2.kmeans(i_img,K,None,criteria,It,cv2.KMEANS_RANDOM_CENTERS)
            else:
                ret,label,center = fz.Clustering(K, Type, Method, img, It, EE)
        center = np.uint8(center)
        res = center[label.flatten()]
        res2 = res.reshape((in_img.shape))
        cv2.imwrite(tempfile_path,res2)
        image_seg = Image.open(tempfile_path)
        canvas_seg.image = ImageTk.PhotoImage(image_seg.resize((170, 195), Image.ANTIALIAS))
        canvas_seg.create_image(0, 0, image=canvas_seg.image, anchor='nw')

def Dis_seg():
    global S_img
    top=Toplevel()
    top.title("Segmented Image")
    S_img=ImageTk.PhotoImage(Image.open(tempfile_path))
    S_label=tk.Label(top,image=S_img).pack()
    Exit_button1 =tk.Button(top, text="Exit", command=top.destroy).pack()


def K_value():
    global K
    K=int(cluster_box.get())

def EE_value():
    global EE
    EE=float(epsilon_box.get())
    
def It_value():
    global It
    It=int(iteration_box.get())

def method_name():
    global Method
    Method=method_box.get()
    
def Type_name():
    global Type
    Type=Type_box.get()
    
def Data_in():
    K_value()
    EE_value()
    It_value()
    method_name()
    Type_name()
    if Method == 'Select method' or Type=='Select data type':
        messagebox.showerror("Error","Please select the method or type correctly")
    if len(file_path) <1:
        messagebox.showerror("Error","Please select input file correctly")
    if Method != 'Select method' and Type!='Select data type' and len(file_path) >1:        
        messagebox.showinfo("Selection Value","Intial setting is sucessfully completed")
    

#GUI code start from here--------------------------------------------------------

root = tk.Tk()
root.minsize(420, 420)
root.title("Clustering- Image Segmentation")

Cap_font = font.Font(name='TkCaptionFont',exists=True,family='Arial Narrow',size=9,slant='roman',weight='normal')
Cap_font.config


menubar = tk.Menu(root)
# file manage bar
filemenu = tk.Menu(menubar, tearoff=0)
filemenu.add_command(label="Open", command=Openfile)
filemenu.add_command(label="Save", command=Savefile)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=filemenu)

# Image Display manage bar
dismenu = tk.Menu(menubar, tearoff=0)
dismenu.add_command(label="Input Image", command=Dis_input)
dismenu.add_command(label="Segmented Image", command=Dis_seg)
menubar.add_cascade(label="View", menu=dismenu)
root.config(menu=menubar)

#root.geometry("400x400") 
top_left = tk.LabelFrame(root, text="Input Data", width=200, height=200)
top_left.grid(row=0, column=0, padx=0, pady=0)

canvas_in = Canvas(top_left, bg='gray', height=170, width=195, borderwidth=2, highlightthickness=2)
canvas_in.grid(row=0, column=0, sticky='NESW', padx=0, pady=0)

#----------------------------------------------------------------------------------------
top_right = tk.LabelFrame(root, text="Segmented Data", width=198, height=200)
top_right.grid(row=0, column=1, padx=0, pady=0)

canvas_seg=Canvas(top_right, bg='gray', height= 170, width=195, borderwidth=2, highlightthickness=2)
canvas_seg.grid(row=0,column=0, sticky='NESW' ,padx=0,pady=0)

#-------------------------------------------------------------------------------------
bottom_left = ttk.LabelFrame(root, text="Initilization", width=200, height=200)
bottom_left.grid(row=1, column=0, padx=0, pady=0)

spin_label1 = tk.Label(bottom_left, text="K :")
spin_label1.grid(row=1, column=0, sticky='W')

spin_label2 = tk.Label(bottom_left, text="E :")
spin_label2.grid(row=2, column=0, sticky='W')

spin_label3 = tk.Label(bottom_left, text="I :")
spin_label3.grid(row=3, column=0, sticky='W')

var1 = tk.StringVar(value='5') # default setting
cluster_box = tk.Spinbox(bottom_left, cursor="arrow", from_=2, to=5, width=10,textvariable=var1, justify=tk.RIGHT, command=K_value)
cluster_box.grid(row=1, column=1, sticky='E', pady=3)

var2 = tk.StringVar(value='0.050') # default setting
epsilon_box = tk.Spinbox(bottom_left, increment=0.001, format='%.3f', cursor="arrow", from_=0, to=1, width=10,textvariable=var2, justify=tk.RIGHT, command=EE_value)
epsilon_box.grid(row=2, column=1, sticky='E', pady=3)           

var3 = tk.StringVar(value='10') # default setting
iteration_box = tk.Spinbox(bottom_left,cursor="arrow", from_=5, to=30, width=10,textvariable=var3, justify=tk.RIGHT, command=It_value)
iteration_box.grid(row=3, column=1, sticky='E', pady=3)

#Label('Combobox with text entry')
list1 = ('Select method','KM', 'FCM', 'ORFCM')
var4 = tk.StringVar()
var4.set(list1[0])
method_box = ttk.Combobox(bottom_left, width = 14, height=3, textvariable=var4, values=list1)
method_box.grid(row=4, column=1,sticky='E', pady=3)
          
list2 = ('Select data type','Color', 'Grayscale')
var5 = tk.StringVar()
var5.set(list2[0])
Type_box = ttk.Combobox(bottom_left, width = 14, height=3, textvariable=var5, values=list2)
Type_box.grid(row=5, column=1,sticky='E', pady=3)
       
#--------------------------------------------------------------------------------
bottom_right = tk.LabelFrame(root, text="Command Window", width=200, height=200)              
bottom_right.grid(row=1, column=1, padx=0, pady=0)

my_text = tk.Text(bottom_right, height=1, width=16)
my_text.grid(row=0, column=0)
my_text.insert(tk.END, "(X,Y,Z)Image Size")

Upload_button = tk.Button(bottom_right, text="Upload data", command= Data_in)
Upload_button.grid(row=1, column=0,pady=3) 

seg_button1 = tk.Button(bottom_right, text="segmentation", command=Segmentation)
seg_button1.grid(row=2, column=0, pady=3)

Exit_button = tk.Button(bottom_right, text='Program Exit', command=root.quit)
Exit_button.grid(row=3,column=0, pady=3)

root.iconphoto(False, PhotoImage(file ='/home/fasahat/pCloudDrive/Python_codes/Image Segmentation/Eco-Leafs.png')) 
#root.iconbitmap("P:\Python_codes\Image Segmentation\Eco-Leafs.ico")
root.mainloop()