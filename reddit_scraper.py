# -*- coding: utf-8 -*-
"""
Created on Mon May 10 10:54:05 2021

@author: ksbig
"""
import countersA
import praw
import numpy as np
from tkinter import * 
import tkinter as tk
from PIL import Image,ImageTk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, 
NavigationToolbar2Tk)




def show1():
    sldr = "Number of Symbols" + str(v1.get())
    s1 = Scale(root, variable= v1, from_ = 100, to= 500,orient =HORIZONTAL)
    b1 = Label(root,text="Get Max Num Symbols", bg="yellow")
    s1.pack(anchor=CENTER)
    b1.pack(anchor=CENTER)
    

def logo():
        logo = Image.open('wsb.png')
        logo = ImageTk.PhotoImage(logo)
        logo_label = tk.Label(image=logo)
        logo_label.image = logo 
        logo_label.pack(side="bottom",ipadx=20,ipady=20)
        
        
def getData(int): 
    if int == 1:      
           subreddit = reddit.subreddit('wallstreetbets')
           top_subreddit = subreddit.top(limit=v1.get())
           for submission in top_subreddit:
                        title= submission.title
                        title_words = title.split()
                        countersA.words_collection.append(title_words)
        
           countersA.cleanTitle(countersA.words_collection)
                
           count = (countersA.CountFrequency(countersA.potential_stock_symbols))
           countLabel= Label(root, text=count)
           countLabel.pack()
           plot(count)
           
    elif int == 2:      
           subreddit = reddit.subreddit('stocks')
           top_subreddit = subreddit.top(limit=v1.get())
           for submission in top_subreddit:
                        title= submission.title
                        title_words = title.split()
                        countersA.words_collection.append(title_words)
        
           countersA.cleanTitle(countersA.words_collection)
                
           count = (countersA.CountFrequency(countersA.potential_stock_symbols))
           countLabel= Label(root, text=count)
           countLabel.pack()
           plot(count)           
 
    elif int ==3:
           subreddit = reddit.subreddit('pennystocks')
           top_subreddit = subreddit.top(limit=v1.get())
           for submission in top_subreddit:
                        title= submission.title
                        title_words = title.split()
                        countersA.words_collection.append(title_words)
        
           countersA.cleanTitle(countersA.words_collection)
                
           count = (countersA.CountFrequency(countersA.potential_stock_symbols))
           countLabel= Label(root, text=count)
           countLabel.pack()
     
           plot(count)                


    
       
def plot(count):
    
    # the figure that will contain the plot
    fig = Figure(figsize = (5, 5),
                 dpi = 100)
  
    # list of squares
    x = []
    y = []
    
    for key,value in count:
           key = x.append(key)
           value = y.append(value)
           
    
    # adding the subplot
    plot1 = fig.add_subplot(111)
    
  
    # plotting the graph
    plot1.plot(x,y,'bo')
    
    # creating the Tkinter canvas
    # containing the Matplotlib figure
    canvas = FigureCanvasTkAgg(fig, master = root)
    canvas.draw()
     
    # placing the canvas on the Tkinter window
    canvas.get_tk_widget().pack()
  
    # creating the Matplotlib toolbar
    toolbar = NavigationToolbar2Tk(canvas,root)
    toolbar.update()
  
    # placing the toolbar on the Tkinter window
    canvas.get_tk_widget().pack(side=BOTTOM)
     
   


                
if __name__ == "__main__":
   
    #from keys import reddit_client_ID, reddit_secrete_token, reddit_userName, reddit_password
    reddit = praw.Reddit(client_id ='FwwowWJjJ3qa2A',  
                     client_secret ='kOGPQcJYvl5Ncu5VPZ7T2yOnbezOFw',  
                     user_agent ='WSB',  
                     username ='',  
                     password ='')  

root = Tk()
root.title("Reddit Stock Symbol Scraper")
root.geometry("900x900")


sel = IntVar()
sel.get()
v1 = DoubleVar() 
Radiobutton(root,text="WallStreetBets", variable=sel, value=1  ).pack(anchor=W)
Radiobutton(root,text="Stocks", variable=sel, value=2   ).pack(anchor=W)
Radiobutton(root,text="PennyStocks", variable=sel, value=3  ).pack(anchor=W)


myButton = Button(root, text="Submit", bg="green", command=lambda: getData(sel.get()))
myButton.pack(ipadx=10,ipady=10)  

logo()
show1()
 
root.mainloop()


