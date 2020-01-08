"""-------------------------------------------------------------------------------------
FINENHANCE Financial Applications - allows users to create an account and manage various
banking accounts such as checkings and savings. Also allows users to have a stock page where
they are able to view various NYSE stock exchanges
-------------------------------------------------------------------------------------"""

"""Import necessary modules"""
#Tkinter: Used to create and mould app GUI
import tkinter as tk
from tkinter import ttk

#OS: Used to create and access files (for login information)
import os

#Datetime: Used to access and format today's and other dates
#to be used as x points for stock plots (domain)
import datetime as dt
from datetime import timedelta

#Pandas: Used to access stock information Yahoo finance API
#and to manipulate it for use in matplotlib graphing
import pandas as pd
import pandas_datareader as web
#from numpy import arange, sin, pi 

#Yahoo Finance: Also used to access stock info from Yahoo finance
#API but namely to acquire current stock price values
from yahoo_fin import stock_info as si #current stock

#Matplotlib: Used to plot, manipulate and style plots of the stock
#information acquired from Yahoo finance.
import matplotlib
import matplotlib.pyplot as pt
from matplotlib import style
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

#Implement the default mpl key bindings and toolbar support (for plot
#manipulation)
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

"""Create app default variables"""
#Creates default font used for majority of app
LARGE_FONT= ("malgun gothic semilight", 12)

#Creates file that will store login credentials upon
#signup to be referenced in login
creds = 'tempfile.temp'

#New default font size for stock plots
matplotlib.rc('xtick', labelsize=6) 
matplotlib.rc('ytick', labelsize=6)

#Creates default for variables to be
#used throughout the program
balance = 50000
stockFg = 'green'
lineC = 'green'
arrow = 'green'

#For file saving and loading for portfolio
tickerList = [] #stores stock ticker when bough
priceList = [] #stores shares price when bought


"""-------------------------------------------
NAVIGATION
----------------------------------------------"""
#Main function that is used to display pages.
class Finenhance(tk.Tk):

    def __init__(self):
        #Initializes functions
        tk.Tk.__init__(self)
        #Creates constant container to house navigation buttons
        container = tk.Frame(self)
        container.pack()
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1) #places the container on the bottom 

        #Dictionary that will hold all pages (classes)
        self.frames = {}

        #For loop that will select pages to be displayed
        #upon button click event
        for F in (HomePage, Accounts, Stocks, Settings):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(HomePage)
    

    #Selected frame is raised above other frames
    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()




"""-------------------------------------------
APPLICATION PAGES & SUBPAGES
----------------------------------------------"""
#Creates main, home page    
class HomePage(tk.Frame):

    def __init__(self, master, controller):
        #Intiiates the navigational frame (just placeholder until login complete)
        tk.Frame.__init__(self, master, bg='#2e3131')
        style = ttk.Style() #Allows further styling of widgets using ttk

                
        #Signup definition upon start up - creates signup pages that
        #allows user to create an account        
        def Signup():
            #Creates and places main background frame to place everything on
            self.homeFrame = tk.Frame(self, width = 500, height = 600, bg = 'grey')
            self.homeFrame.pack()

            #Creates Finenhance title on homeframe
            labelTitleFIN = tk.Label(self.homeFrame, text="FIN", font=("malgun gothic semilight", 35), bg = 'grey', fg='#121f1f')
            labelTitleFIN.place(relx=0.315, rely=0.2, anchor='n') #Used to places objects on the frame
            labelTitleEN = tk.Label(self.homeFrame, text="ENHANCE", font=("malgun gothic semilight", 35), bg = 'grey', fg='green')
            labelTitleEN.place(relx=0.6, rely=0.2, anchor='n')

            #Puts an instruction label in the window telling users to sign up
            instruction = tk.Label(self.homeFrame, text="Please Enter new Credentials\n", bg="grey", font=("malgun gothic semilight", 12))
            instruction.place(relx=0.5, rely=0.45, anchor="n")

            #Labels to tell users where to place username and password for sign up
            self.nameL = tk.Label(self.homeFrame, text="New Username", font=("malgun gothic semilight", 15), bg="grey", fg='green')
            self.pwordL = tk.Label(self.homeFrame, text="New Password", font=("malgun gothic semilight", 15), bg="grey", fg='green')
            self.nameL.place(relx=0.5, rely=0.55, anchor="n")
            self.pwordL.place(relx=0.5, rely=0.7, anchor="n")

            #Places two text boxes under the according labels to accept credentials
            #as an input (Show="*" shows the password characters as *s)
            self.nameE = tk.Entry(self.homeFrame)
            self.pwordE = tk.Entry(self.homeFrame, show="*")
            self.nameE.place(relx=0.5, rely=0.6, anchor="n")
            self.pwordE.place(relx=0.5, rely=0.75, anchor="n")

            #Creates a signup button to call the next definition FSSignup
            signupButton = ttk.Button(self.homeFrame, text="Signup", command=FSSignup)
            signupButton.place(relx=0.5, rely=0.83, anchor="n")        


        #Stores the users credentials entered in entry box of signup
        def FSSignup():
            #Creates document (creds - called 'tempfile')
            with open(creds, 'w') as f: 
                f.write(self.nameE.get()) #Stores username string from entry on first line
                f.write('\n') #Splits to next line
                f.write(self.pwordE.get())#Stores password string from entry on second line
                f.close() #Closes file
                self.homeFrame.destroy()#Destroys the signup page
            Login() #Calls login definition to open login page


        #Creates login window to allow users to login using signup credentials
        def Login():
            global rmuser #more globals - used to delete login and signup return once logged in
            global loginB
            
            #Creates the new login window
            self.homeLFrame = tk.Frame(self, width = 500, height = 600, bg = 'grey')
            self.homeLFrame.pack()

            #Creates Finenhance title on new login frame           
            labelTitleFIN = tk.Label(self.homeLFrame, text="FIN", font=("malgun gothic semilight", 35), bg = 'grey', fg='#121f1f')
            labelTitleFIN.place(relx=0.315, rely=0.2, anchor='n')
            labelTitleEN = tk.Label(self.homeLFrame, text="ENHANCE", font=("malgun gothic semilight", 35), bg = 'grey', fg='green')
            labelTitleEN.place(relx=0.6, rely=0.2, anchor='n')

            #Puts new instruction label in the window telling users to login
            instruction = tk.Label(self.homeLFrame, text = "Please Login\n", bg="grey", font=("malgun gothic semilight", 12))
            instruction.place(relx=0.5, rely=0.45, anchor="n")

            #More labels to indicate where to enter certain credentials
            self.nameL=tk.Label(self.homeLFrame, text="Username", bg="grey", font=("malgun gothic semilight", 15), fg='green')
            self.pwordL=tk.Label(self.homeLFrame, text="Password", bg="grey", font=("malgun gothic semilight", 15), fg='green')
            self.nameL.place(relx=0.5, rely=0.55, anchor="n")
            self.pwordL.place(relx=0.5, rely=0.7, anchor="n")

            #Two more entry boxes to enter username and password to login
            self.nameEL=tk.Entry(self.homeLFrame)
            self.pwordEL=tk.Entry(self.homeLFrame, show="*")
            self.nameEL.place(relx=0.5, rely=0.6, anchor="n")
            self.pwordEL.place(relx=0.5, rely=0.75, anchor="n")

            #Creates login button, clicked when users have finished entering credentials
            #call checklogin to check input
            loginB = ttk.Button(self.homeLFrame, text="Login", command=CheckLogin)
            loginB.place(relx=0.5, rely=0.8, anchor="n")  

            #Creates remove user button to act as back button to return to signup page
            #to create new credentials if need be
            style.configure("Del.TButton", foreground = 'red', font=("malgun gothic semilight", 9)) #styles the button to be red
            rmuser = ttk.Button(self.homeLFrame, text="Delete User", style = 'Del.TButton', command =DelUser)
            rmuser.place(relx=0.5, rely=0.85, anchor="n")



        #Checks input in entry of login window and compares to the tempfile document
        #to validate if the login matches 
        def CheckLogin():
            #Makes username and password global to load and
            #save data in NavAccess() and save() - in stocks
            global uname, pword 
            with open(creds) as f:
                data = f.readlines()    #Takes entire creds document and puts its info into a variable
                uname = data[0].rstrip()    #makes the first line (username in signup) a variable
                pword = data[1].rstrip()    #makes the second line (password in signup) a variable

            #Checks if login data matches signup data
            if self.nameEL.get() == uname and self.pwordEL.get() == pword: #if so..
                #Opens new window to notify user that they have been logged in
                self.r = tk.Tk() 
                self.r.title(":D")
                self.r.geometry("150x50")
                
                #Prints welcome message to user using their inputed username
                rlbl=tk.Label(self.r, text='\n[+] Logged In \n Welcome back ' + self.nameEL.get() + '!')
                rlbl.pack()
                
                #Deletes the remove user and login buttons since no longer needed
                rmuser.destroy()
                loginB.destroy()
                
                #Calls NavAccess to initiate navigational control over app (can open new pages)
                NavAccess()
                self.r.mainloop() #allows the login notification window to remain open

                
            #If input data do not match, creates new window notifying user that
            #this is an invalid login and to try again.
            else:
                self.r = tk.Tk()
                self.r.title("D:")
                self.r.geometry("150x50")
                rlbl = tk.Label(self.r, text="\n[!] Invalid Login")
                rlbl.pack()
                self.r.mainloop()

                
        #If need be, allows user to delete singup credentials, to return to signup page and restart        
        def DelUser():
            os.remove(creds) #deletes the creds file
            self.homeLFrame.destroy() #destroys the login page
            Signup() #calls signup to return to signup page



        #Creates the navigational bar once logged in   
        def NavAccess():
            global balance, tickerList, priceList
            #Creates a finenhance label on the nav bar
            navLabel = tk.Label(self, text="Finenhance", font=("malgun gothic semilight", 12), bg='#2e3131', fg='#e5dddb')
            navLabel.pack(pady=5,padx=10)

            #Another welcome message (in green) to the user
            welcomeLabel = tk.Label(self, text='Welcome back ' + self.nameEL.get() + '!', font=("malgun gothic semilight", 10), bg='#2e3131', fg='green')
            welcomeLabel.pack(padx=10, pady=10)

            #More styling
            style.configure("TButton", foreground="green", font=("malgun gothic semilight", 9))
            style.map("TButton",
                foreground=[('pressed', 'black'), ('active', 'green')],
                background=[('pressed', '!disabled', 'black'), ('active', 'green')]
                )


            #Creates 2 buttons (Stocks and Accounts to navigate to those
            #respective pages
            button = ttk.Button(self, text="Accounts",
                                command=lambda: controller.show_frame(Accounts))
            button.pack()

            button2 = ttk.Button(self, text="Stocks",
                                command=lambda: controller.show_frame(Stocks))
            button2.pack()

            button3 = ttk.Button(self, text="Settings",
                            command=lambda: controller.show_frame(Settings))
            button3.pack(pady=10)

            #Will try to load data from file if user has previously
            #saved info
            try:
                #Searches for unqiue file pertaining
                #to user's name and pass 
                f = open(uname + pword + ".txt", "r")
                information = f.readlines() #creates list of file info
                print(information)
                balance = float(information[0]) #balance is the first line

                #sorts through the list and formats it to show stock owned and price bought at
                for i in range(len(information)-1):
                    tickerList.append(information[i+1].partition(" ")[0])
                    priceList.append(float(information[i+1].partition(" ")[-1].strip('\n')))
                    

                #Notifies user they have logged before and that their info was found
                #prints the user's saved data
                print("Loaded Profile!")
                print("Balance: ", balance)
                print("Shares Owned Currently: ")
                print()
                for i in range(len(tickerList)):
                    print(tickerList[i] + " " + str(priceList[i]))
                    print()

            #If file is not found, user has not logged in before and so
            #notifies user
            except FileNotFoundError:
                print("No data found for user")

        #Calls signup to initiate the app
        Signup() 



   
#Creates accounts page (Youcef B and Logan)
class Accounts(tk.Frame):
    
    def __init__(self, master, controller):
        tk.Frame.__init__(self, master, bg='#2e3131')
        accFrame = tk.Frame(self, width = 500, height = 600, bg = 'red')
        accFrame.pack()

        navLabel = tk.Label(self, text="Accounts", font=LARGE_FONT, bg='#2e3131', fg='#e5dddb')
        navLabel.pack(pady=10,padx=10)


        #FRAME
        labelTitle = tk.Label(accFrame, text="Accounts", font=("malgun gothic semilight", 25), bg = 'red',)
        labelTitle.place(relx=0.5, rely=0.2, anchor='n')

        button = ttk.Button(accFrame, text="Back to Home",
                            command=lambda: controller.show_frame(HomePage))
        button.place(relx=0.5, rely=0.9, anchor = 'n')

        button21 = ttk.Button(accFrame, text="Back to Home", command=Withdraw)
        button21.place(relx=0.5, rely=0.5, anchor = 'n')

        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(HomePage))
        button1.pack()

        button2 = ttk.Button(self, text="Stocks",   
                            command=lambda: controller.show_frame(Stocks))
        button2.pack()

        button3 = ttk.Button(self, text="Accounts",
                            command=lambda: controller.show_frame(Accounts))
        button3.pack()

        def Withdraw():
            pass
        #withdrawbbut = ttk.Button(self, text = "Withdraw", command = withdrawmoney)
#Creates settings page (Youcef B and Logan)
class Settings(tk.Frame):
    
    def __init__(self, master, controller):
        tk.Frame.__init__(self, master, bg='#2e3131')
        setFrame = tk.Frame(self, width = 500, height = 600, bg = 'blue')
        setFrame.pack()

        navLabel = tk.Label(self, text="Settings", font=LARGE_FONT, bg='#2e3131', fg='#e5dddb')
        navLabel.place(relx=3, rely=3, anchor=n)


        #FRAME
        labelTitle = tk.Label(setFrame, text="Settings", font=("malgun gothic semilight", 25), bg = 'blue',)
        labelTitle.place(relx=0.5, rely=0.2, anchor='n')

        button = ttk.Button(setFrame, text="Back to Home",
                            command=lambda: controller.show_frame(HomePage))
        button.place(relx=0.5, rely=0.9, anchor = 'n')

        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(HomePage))
        button1.pack()

        button2 = ttk.Button(self, text="Stocks",
                            command=lambda: controller.show_frame(Stocks))
        button2.pack()

        button3 = ttk.Button(self, text="Accounts",
                            command=lambda: controller.show_frame(Accounts))
        button3.pack()



#Creates Stock page
class Stocks(tk.Frame):
    
    def __init__(self, master, controller):
        style = ttk.Style()
        
        #Initiates navigational frame (bottom)
        tk.Frame.__init__(self, master, bg='#2e3131')

        #Creates actual stock page frame (create first to be ontop)
        stockFrame = tk.Frame(self, width = 500, height = 600, bg = 'grey')
        stockFrame.pack()
        
        #Creates stock page title and nav buttons on navigational frame
        navLabel = tk.Label(self, text="Stocks", font=LARGE_FONT, bg='#2e3131', fg='#e5dddb')
        navLabel.pack(pady=10,padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(HomePage))
        button1.pack()

        button2 = ttk.Button(self, text="Accounts",
                            command=lambda: controller.show_frame(Accounts))
        button2.pack()

        button3 = ttk.Button(self, text="Settings",
                            command=lambda: controller.show_frame(Settings))
        button3.pack()
        
        #Verfification for existing toolbar and invalid text indicator
        #to delete on reexecution if exists.
        self.tool=False
        self.open = False
        self.i = False

        #FRAME Setup 
        labelTitle = tk.Label(stockFrame, text="Stocks", font=("malgun gothic semilight", 20), bg = 'grey', fg = 'black')
        labelTitle.place(relx=0.5, rely=0.03, anchor='n')

        #Entry widget to enter ticker of stock to be plotted
        tickerEntry = ttk.Entry(stockFrame)
        tickerEntry.place(relx=0.18, rely=0.918, anchor='n')

        #Upon button press, access stock info and plot it (below function)
        tickerButton = ttk.Button(stockFrame, text="Confirm",
                            command=lambda: pressPlot(tickerEntry.get()))
        tickerButton.place(relx=0.38, rely=0.918, anchor='n')

        #Creates radiobuttons to choose length of stock history
        style.configure("TRadiobutton", background = 'grey', selectcolor = 'green', font=("malgun gothic semilight", 10))
        style.map("TRadiobutton", foreground=[('pressed', 'green')])

        #5 days
        Radio_1=ttk.Radiobutton(stockFrame, text = '5dy', value = 1,
                                command=lambda: setDate(5))
        Radio_1.place(relx=0.05, rely=0.76, anchor='nw')

        #1 month    
        Radio_2=ttk.Radiobutton(stockFrame, text = '1mo', value = 2,
                                command=lambda: setDate(30))
        Radio_2.place(relx=0.15, rely=0.76, anchor='nw')

        #6 months    
        Radio_3=ttk.Radiobutton(stockFrame, text = '6mo', value = 3,
                                command=lambda: setDate(180))
        Radio_3.place(relx=0.25, rely=0.76, anchor='nw')

        #1 year
        Radio_4=ttk.Radiobutton(stockFrame, text = '1yr', value = 4,
                                command=lambda: setDate(365))
        Radio_4.place(relx=0.35, rely=0.76, anchor='nw')

        #5 years
        Radio_5=ttk.Radiobutton(stockFrame, text = '5yr', value = 5,
                                command=lambda: setDate(1826))
        Radio_5.place(relx=0.45, rely=0.76, anchor='nw')


        #Upon call from a radio button, sets various variables to match current date
        #and previous date according to inputed time delta
        def setDate(x):
            #These globals make the variables available to the entrie script
            #usable by any definition that follows
            global year2 
            global month2
            global date2
            global year1
            global month1
            global date1

            #-Current Date-
            #uses datetime to create string of current date (x2)
            now = dt.datetime.now() 
            current = str(now)
            #Sorts through string to store year, month and date which is needed
            #to plot the day and acquire stock data (for pandas and numpy)
            year2 = int(current[0:4])
            month2 = int(current[5:7])
            date2 = int(current[8:10])
            currentList = [year2, month2, date2]

            #Uses timedelta to find the prior date (x1)
            before = dt.datetime.now() - timedelta(days=x)

            #-Prior Date-
            #Creates prior date string which is also sorted to find
            #year, month and date for same reasons
            prior = str(before)
            year1 = int(prior[0:4])
            month1 = int(prior[5:7])
            date1 = int(prior[8:10])
            priorList = [year1, month1, date1]
            
            #Prints both dates in shell (mainly for debug)
            print(year2, month2, date2)
            print(year1, month1, date1)


        #Opens new sub window that allows user to invest money (from balance)
        #into defined stock at the live price
        #Money made is "simulated" as if the user invested at the open price since there is no
        #simple manner to acquire and update current stock information to find the actual gain
        def Invest():
            self.open = True
            global tickerList, priceList
            global stocksFg, lineC, arrow
            #Acquire Ticker Info
            x = tickerEntry.get()
            livP = si.get_live_price(x) #not very live 
            table = si.get_quote_table(x)
            opnP = table['Open']
            pclP = table['Previous Close']

            netPrise = opnP - pclP
            prcntrise = (netPrise/pclP)
        
            #Create new investing window    
            self.r = tk.Tk()
            self.r.title("Invest")
            
            #Creates actual stock page frame (create first to be ontop)
            investFrame = tk.Frame(self.r, width = 400, height = 400, bg = 'grey')
            investFrame.pack()

            #Creates top label to show current balance
            Binst = tk.Label(investFrame, text = 'Balance', bg='grey', fg = 'darkgreen', font = ("malgun gothic semilight", 8))
            Binst.pack()
            BLabel = tk.Label(investFrame, text = '$' + str(balance), bg='grey', fg = 'black', font = ("malgun gothic semilight", 20, "bold"))
            BLabel.pack()
            
            #Creates middle label to show current price of shares to be bought
            #according to slider position
            Pinst = tk.Label(investFrame, text = 'Shares Price', bg='grey', fg = 'darkgreen', font = ("malgun gothic semilight", 8))
            Pinst.pack()
            PLabel = tk.Label(investFrame, text = '$' + '0', bg='grey', fg = 'black', font = ("malgun gothic semilight", 20, "bold"))
            PLabel.pack()
            
            #Creates scale bar and displays its value to represent
            #amount of shares to buy
            scalevar = tk.IntVar()
            scalevar.set(0)
                
            #Creates shares label to display number of shares to be bought
            #according to slider
            sharesinst = tk.Label(investFrame, text = 'Number of Shares', bg='grey', fg = 'darkgreen', font = ("malgun gothic semilight", 8))
            sharesinst.pack()
            shares = tk.Label(investFrame, textvariable=scalevar, bg='grey', fg = 'black', font = ("malgun gothic semilight", 20, "bold"))
            shares.pack()

            #Updates PLabel
            def showP(x):
                PLabel['text'] = '$' + str(round(x,2))
            
            #Creates slider to select and show number shares to buy and shows their price
            PLabelPrice = scalevar.get()

            slidStock = tk.Scale(investFrame, from_=0, to_=100, length=394, variable = scalevar, orient="horizontal", bg='grey',
                              command=lambda PLabelPrice: showP(int(PLabelPrice)*livP))
            slidStock.pack()
            
            #Function that will show currently owned stocks, their price bought at
            #and how much money made
            def show():
                #Creates second frame to put stock info on
                self.investFrame2 = tk.Frame(self.r, width = 400, height = 50, bg = 'grey')
                self.investFrame2.pack()

                #Creates 2 lists to hold required frames and buttons for
                #each stock info frame (each ticker will have one - according to ticker and price lists)
                frameList=[]
                buttonList=[]

                #Creates the required number of variable names for frames and buttons
                for i in range(len(tickerList)):
                    frameList.append('stockFrame' + str(i))
                    buttonList.append('stockB' + str(i))
                    
                #Creates and displays the stock info
                for i in frameList:
                    #Creates an actual frame under the name of each item in frameList
                    frame = i
                    frame = tk.Frame(self.investFrame2, relief = 'groove', bd=3, width = 400, height = 50, bg = '#121f1f')
                    frame.pack()

                    #Creates the stock label showing the ticker, price the shares were bought at
                    sL = tk.Label(frame, text = tickerList[frameList.index(i)].upper() + " " + str(priceList[frameList.index(i)]), bg = '#121f1f', fg='white', font = ("malgun gothic semilight", 8))
                    sL.place(relx=0.2, rely=0.5, anchor = 'center')

                    #Creates the net stock profit label to place (different label since needs colour)
                    sP = tk.Label(frame, text = '$' + str(round(priceList[frameList.index(i)]*prcntrise, 2)) + arrow , bg = '#121f1f', fg=stockFg, font = ("malgun gothic semilight", 8))
                    sP.place(relx=0.6, rely=0.5, anchor = 'center')


                    #Creates unique sell button (with unique sell() call parameter pertaining to stock it is
                    #associated with) for each button in button list
                    button = buttonList[frameList.index(i)]

                    #must use i=i to save the frame (and its index position) at the time the
                    #button was created (so we'll have buttons 0 to n and not just all n)
                    button = ttk.Button(frame, text = "Sell", command=lambda i=i: sell(frameList.index(i))) #i=i to store i at the time
                    button.place(relx=0.8, rely=0.5, anchor = 'center')

            #New function that will sell the shares of the ticker it is
            #associated with upon sell button press
            def sell(x):
                print(x)
                global balance
                
                #Creates a sum variable according to the price the shares were bought
                #at in addition to net profit
                summ = priceList[x] + priceList[x]*prcntrise

                #Adds the sum to the balance value
                balance += summ
                
                #updates the balance label
                BLabel['text'] = '$' + str(round(balance,2))

                #removes removed stock ticker and price from appropriate lists
                tickerList.remove(tickerList[x])
                priceList.remove(priceList[x])

                #destroys stock info frame and calls show again to update and register changes
                #(more efficient than updating the whole r window)
                self.investFrame2.destroy()
                show()

            #Calls show from r window startup to display currently owned shares
            #from load data (if any).
            show()
        


            #Trans function to show bought stock, amount made and update balance
            def Trans(y):
                global balance
                global stocksDict
                global tickerList, priceList
                print(priceList)
    
                    
                #Buys stock if balance sufficient and if more than 0 shares bought
                if slidStock.get()*livP <= y and slidStock.get()>0:
                    #Creates transaction history label
                    print("Successfully purchased", slidStock.get(), "Stocks from", x,
                                     "for $", round(slidStock.get()*livP,2), "made", round(slidStock.get()*livP*prcntrise,2) )

                    #Updates balance value
                    balance -= slidStock.get()*livP
                    #Updates balance on label value
                    BLabel['text'] = '$' + str(round(balance,2))

                    #stores stock and share price in 2 seperate lists to
                    #save and access data

                    #if the ticker is already listed, won't add a new object in the list,
                    #rather just add the value to the current pricelist value at the appropriate
                    #position
                    if x in tickerList:
                        ticker = tickerList.index(x) #stores the position of ticker in tickerlist
                        iPrice = priceList[ticker] #old price

                        #updates to new price at appropriate position in pricelist
                        fPrice = round(iPrice + slidStock.get()*livP,2) 
                        priceList[ticker] = fPrice

                    #else creates new objects in both ticker and price lists at the end    
                    else:
                        tickerList.append(x)
                        priceList.append(round(slidStock.get()*livP,2))

                    #same as above to update the stock info
                    self.investFrame2.destroy()
                    show()
                    
                else:
                    print("Insufficient Funds!")
                    
                print(tickerList, priceList)

            #Upon save button press, will save current balance value and ticker/price lists
            #for stock info
            def Save():
                global uname, tickerList, priceList

                #Saves info under unique file pertaining to username and password as the name
                #(if already there will open it, else will create one)
                f=open(uname + pword+ ".txt", "w+")
                f.write(str(round(balance,2))) #stores balance value
                f.write('\n') #skips to new line

                #for each item in ticker list, store it and its value beside it (each ticker
                #and its price are in the same index position in their according lists)
                for i in range(len(tickerList)):
                    f.write(tickerList[i] + " " + str(priceList[i]))
                    f.write('\n')
                
                f.close

    
            #Button to confirm purchase of shares
            iB = ttk.Button(investFrame, text = "Confirm", command=lambda: Trans(balance))
            iB.pack(pady=10)

            #Button to save current portfolio info
            saveB = ttk.Button(investFrame, text = "Save Portfolio", command=lambda: Save())
            saveB.pack()
            

            
        #----------------
        #Stock Graphing
        #---------------
        def pressPlot(x):
            global stockFg, lineC, arrow
            try:
                #Getting stock open price, live price and %netrise
                livP = si.get_live_price(x) #not very live 
                table = si.get_quote_table(x)
                opnP = table['Open']
                pclP = table['Previous Close']

                netPrise = opnP - pclP
                prcntrise = (netPrise/pclP)*100
                print("Open {0}, Previous Close {1}, Current {2}" .format(opnP, pclP, round(livP,2)))

                if netPrise >= 0:
                    stockFg = 'green'
                    lineC = 'g'
                    arrow = '↑'
                else:
                    stockFg = 'red'
                    lineC = 'r'
                    arrow = '↓'    
                    
                #destroys any existing toolbars or labels if they already existed
                #prior to a new plot
                if self.tool==True:
                    self.toolbar.destroy()
                    self.tickerPriceL.destroy()
                    self.tickerRiseL.destroy()
                    self.tickerprcntL.destroy
                    self.tickerTitleL.destroy()

                #Plots ticker and ticker Price Live
                self.tickerPrice = round(livP, 2)
                self.tickerPriceL = tk.Label(stockFrame, text=str(self.tickerPrice) + ' USD', font=("malgun gothic semilight", 15, "bold"), bg = 'grey', fg = 'white') 
                self.tickerPriceL.place(relx=0.41, rely=0.81, anchor='n')

                self.tickerRiseL = tk.Label(stockFrame, text=round(netPrise, 2), font=("malgun gothic semilight", 10, "bold"), bg = 'grey', fg = stockFg)
                self.tickerRiseL.place(relx=0.05, rely=0.875, anchor='nw')

                self.tickerprcntL = tk.Label(stockFrame, text='(' + str(round(prcntrise, 2)) + '%) ' + arrow, font=("malgun gothic semilight", 10, "bold"), bg = 'grey', fg = stockFg)
                self.tickerprcntL.place(relx=0.13, rely=0.875, anchor='nw')
                                             
                self.tickerTitleL = tk.Label(stockFrame, text=x.upper(), font=("malgun gothic semilight", 25, "bold"), bg = 'grey', fg = 'white') 
                self.tickerTitleL.place(relx=0.05, rely=0.8, anchor='nw')

                
                #Plotting the graph of given stock (Ticker)
                pt.style.use("ggplot")
                start = dt.datetime(year1, month1, date1) #Start date, xi on plot
                end = dt.datetime(year2, month2, date2) #End date as today,xf on plot

                #Creates button which opens window for allowing investing
                investB = ttk.Button(stockFrame, text="Invest",
                            command=Invest)
                investB.place(relx=0.68, rely=0.918, anchor='n')

                #Acquires data of given stock (ticker) from
                #Yahoo Finance API
                df = web.get_data_yahoo(str(x), start, end)
                
                #Plots given data, with identifier "Adj Close" on axes
                df["Adj Close"].plot()
                
                #Prints title for Stock graph
                print(x.upper(), "stock price from " +str(start) + " to " + str(end))

                #Graph styling on size
                f = Figure(figsize=(5, 4), dpi=100)
                a = f.add_subplot(111)

                #Makes plot visible on select frame
                f.patch.set_facecolor('#121f1f')        #sets AXES colour
                a.patch.set_facecolor('xkcd:grey')      #sets actual PLOT colour
                a.set_title(str(x.upper()) + " stock price from " + str(start) + " \nto " + str(end), color="#%02x%02x%02x" % (255,250,250))
                a.set_xlabel('Date')    #sets x axis label to "date"
                a.set_ylabel('Price($)')#sets y axis label to "price"
                a.plot(df["Adj Close"], lineC)

    
                #Allocates canvas area to display graph (embeds mtplot graph
                #using FigureCanvasTkAgg function
                canvas = FigureCanvasTkAgg(f, stockFrame)
                canvas.draw()
                canvas.get_tk_widget().place(relx=0.5, rely=0.9, anchor = 'n')
                canvas._tkcanvas.place(relx=0.5, rely=0.1, anchor="n")

                #Creates toolbar to manipulate stock graph
                self.toolbar = NavigationToolbar2Tk(canvas, self)
                self.toolbar.configure(bg='#2e3131')
                self.toolbar.update()
                self.tool=True

                if self.open == True:
                    self.r.destroy()


                if self.i == True:
                    self.LabelI.destroy()
                
                    
            #Exception handling in case that invalid ticker is entered
            except web._utils.RemoteDataError:
                print("Invalid ticker, try again - must be NYSE")
                self.LabelI = tk.Label(stockFrame, text="Invalid ticker, try again - must be NYSE", bg = "green", fg="red")
                self.LabelI.place(relx=0.5, rely=0.9, anchor="n")
                self.i = True #True since invalid text has appeared
                
            except AttributeError:
                print("Invalid ticker, try again - must be NYSE")
                self.LabelI = tk.Label(stockFrame, text="Invalid ticker, try again - must be NYSE", bg = "green", fg="red")
                self.LabelI.place(relx=0.5, rely=0.9, anchor="n")
                self.i = True

            except ValueError:
                print("Please input viewing domain")


            



app = Finenhance()
app.wm_title('Finenhance')
app.wm_iconbitmap('favicon.ico')
app.mainloop()
