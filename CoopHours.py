import pygame, sys,smtplib,datetime#Uses smtplib to send emails#Uses datetime to check what day of the week it is
from pygame import *#Uses pygames to run the program
##################################################### Classes ###########################################################
class studentMail(object):#Used to email the Teacher #All import info in here so people can't try and read stuff after program closes
    def __init__(self):
        self.studentNum= ""
        self.password = ""
        self.To = "To: "
        self.From = "From: "
        self.Subject = "Subject: CO-OP hours"
        self.message = ""
        self.Online = False
        self.BadTextFileName = False
        self.failToLogin=False
        self.totalHours = 0 #This will hold the total number of co-op hours they have done
        self.TimeWorkedList = [] #This will have all the hours and times they worked
        self.textFile = None
        self.teachersEmail = self.studentNum+"@ldcsb.org"
    def loginOffline(self,userName):#This will make the user login offline
        self.studentNum = userName
        self.failToLogin = False
    def login(self,userName,password):#This function will be used to login to the server

        ''' No longer works do to not having a school account
        try:#trying to login
            self.mail = smtplib.SMTP("smtp.office365.com",587,None,30) #Gaining connection to the office 365 server
            self.mail.ehlo()
            self.mail.starttls()
            self.studentNum = userName
            self.password = password
            self.mail.login(self.studentNum+"@ldcsb.org",self.password)
            self.failToLogin = False
        except:
            self.failToLogin = True
        '''
    def sendMail(self):#This will be used to send the email to mr.v
        self.message = "The Total Number of CO-OP hours worked is "+str(self.totalHours)+"\n\nThe days worked were:\n\n"+"\n".join(" ".join(x) for x in self.TimeWorkedList)
        while 1:
            try:#Sends mail
                self.mail.sendmail(self.studentNum+"@ldcsb.org",self.studentNum+"@ldcsb.org","\r\n".join([
                    self.To+self.teachersEmail,self.From+self.studentNum+"@ldcsb.org",self.Subject,"",self.message]))
                break
            except: #If it fails to send it must mean that the login timed out so just signed back in.
                self.mail = smtplib.SMTP("smtp.office365.com",587) #Gaining connection to the office 365 server
                self.mail.ehlo()
                self.mail.starttls()
                self.mail.login(self.studentNum+"@ldcsb.org",self.password)
class Button(pygame.sprite.Sprite): #Basic button class
    buttons=[]#This will hold all the button objs
    def __init__(self,x,y):
        self.x=x#The x and y of the button
        self.y=y
        self.FullRect = pygame.Rect(x,y,100,50)#This is the rect of What is being shown
        self.rect= pygame.Rect(x,y,100,50)#This is the rect of one box
        pygame.sprite.Sprite.__init__(self)#This is used for pygame options
        Button.buttons.append(self)
    def check_if_clicked(self, mousepos): #This function checks if the button is clicked
        if self.FullRect.collidepoint(mousepos): self.onclick(mousepos)
    def onclick(): #Placeholder for onclick functions of the child classes
        pass
    def check_if_hover(self,mousepos):
        return (self.FullRect.collidepoint(mousepos))
class List(Button):
    def __init__(self,x,y,length,height,options):
        Button.__init__(self,x,y)
        self.text=text
        self.options = options
        self.rect=pygame.Rect(x,y,length,height)
        self.FullRect=pygame.Rect(x,y,length,height*len(options))
        self.yDisplacement = 0
        self.numHit = -1
    def draw(self):#DRAWS THE BUTTON
        y = 0#used to find where to draw the box
        for option in self.options:
            pygame.draw.rect(display,grey,(self.x,self.y+y+self.yDisplacement,self.rect.width,self.rect.height))
            pygame.draw.rect(display,black,(self.x,self.y+y+self.yDisplacement,self.rect.width,self.rect.height),5)
            pygame.draw.rect(display,black,(self.x+self.rect.width-50,self.y+y+self.yDisplacement,50,self.rect.height),5)
            text(self.x+self.rect.width-25,self.y+self.yDisplacement+y+self.rect.height//2,"DEL")
            option = font.render(str(" ".join(option)), False, (10, 10, 10))#This will make the text of the options and center it
            display.blit(option,(self.rect.centerx-option.get_width()//2,self.y+y+self.yDisplacement-option.get_height()//2+25))
            y+=self.rect.height
    def onclick(self,mousePos):
        if self.rect.left+self.rect.width-50<mousePos[0]<self.rect.left+self.rect.width:#checks if del his being hit
            for option in range(0,len(self.options),1):#checks which delete is being hit
                if self.rect.top+self.rect.height*option+self.yDisplacement<mousePos[1]<self.rect.top+self.rect.height*option+self.yDisplacement + self.rect.height:
                    self.numHit = option
                    return True#returns the delete being hit
        return False#returns this if didn't hit del

    def scroll(self,direction):#Scrolls boxes up and down using scroll wheel
        if button.check_if_hover(mousepos) and direction == "up" and self.FullRect.height*-1+self.rect.height<=self.yDisplacement<0:self.yDisplacement +=50
        if button.check_if_hover(mousepos) and direction == "down"and self.FullRect.height*-1+self.rect.height<self.yDisplacement<=0:self.yDisplacement -=50
        self.FullRect.y = self.rect.y+self.yDisplacement #MUST BE AFTER CHANGE OF YDISPLACEMENT OR WON'T CHANGE X OF HIT BOX.
class press_button(Button): #This class is for buttons that are pressed with no dropdown menu
    def __init__(self, x, y, text):
        Button.__init__(self,x,y)
        self.text=text
    def check_if_clicked(self,mousepos):
        return self.FullRect.collidepoint(mousepos)
    def onclick(self, mousepos):
        return True
    def draw(self):
        pygame.draw.rect(display,grey,self.rect)
        pygame.draw.rect(display,black,self.rect,3)
        text(self.x+50,self.y+25,self.text)
class textbox_button(Button):
    def __init__(self,x,y,length,height,ShowText):
        Button.__init__(self,x,y)
        self.inputText = []
        self.ShowText = ShowText
        self.FullRect = pygame.Rect(x,y,length,height)#This is the rect of What is being shown
        self.rect= pygame.Rect(x,y,length,height)#This is the rect of one box
        self.isSelected = False
    def setText(self,key):
        if 31< key<255 and len(self.inputText) < 20:self.inputText.append(event.unicode)
        else:
            if key == K_BACKSPACE and len(self.inputText) != 0:
                self.inputText.pop()#Deletes a char
    def draw(self):
        pygame.draw.rect(display,(255,255,255),self.rect)
        pygame.draw.rect(display,black,self.rect,2)
        if self.ShowText == True: text = font.render("".join(self.inputText), False, (10, 10, 10))
        else: text = font.render(len(self.inputText)*"*", False, (10, 10, 10))
        display.blit(text,(self.x+5,self.y+5))
    def onclick(self,mousepos):
        self.isSelected = True
class dropdown_button(Button): #This class will be used to make button used to input hours
    def __init__(self,option_list,x,y):
        Button.__init__(self, x, y)
        self.option_list=option_list#This will hold all the options for each button
        self.currentOption_list = [option_list[0]]#This will be used to see what current options they can see
        self.isDropDown = False#This will check if the button list is open or closed
        self.YDisplacement = 0
    def dropdown(self):#This will open the list up
        self.currentOption_list=self.option_list[::]#This will add all the options they can see to currentOption_List
        self.isDropDown = True#Set the var to true so I know when its open or not
        self.FullRect.height = len(self.option_list)*self.rect.height#Resets the size to the size displayed on the display
    def draw(self):#Draws all the options on the display
        yCounter = self.rect.y#Checks where the current option should go
        for obj in self.currentOption_list:	#Runs through all the options and prints it on the screen
            pygame.draw.rect(display,grey,(self.rect.x,yCounter+self.YDisplacement,self.rect.width,self.rect.height),0)
            pygame.draw.rect(display,(10,10,10),(self.rect.x,yCounter+self.YDisplacement,self.rect.width,self.rect.height),5)#Makes a box to go around it
            option = font.render(str(obj), False, (10, 10, 10))#This will make the text of the options and center it
            display.blit(option,(self.rect.centerx-option.get_width()//2,yCounter+self.YDisplacement-option.get_height()//2+25))
            yCounter += 50#Drops the box 50 pixels down.
    def fold(self,mousepos):#Selects an option and shinks the dropbox again.

        for option in range(0,len(self.option_list),1):#Checks what square their mouse is on
            if (option*self.rect.height+self.rect.y+self.YDisplacement)<mousepos[1]<(option*self.rect.height+self.rect.y+self.YDisplacement+self.rect.height):
                self.currentOption_list = [self.option_list[option]]#Makes the on they click on the new option
                break
        self.isDropDown = False#Lets the program know its not extened out
        self.FullRect.height = self.rect.height#Changes the fullrect to the right size
        self.FullRect.y = self.rect.y#Resets all the vars to how they should be
        self.YDisplacement = 0
    def onclick(self,mousepos):#Checks if its being clicked and changes it from dropped down to folded or the other way around
        if self.isDropDown==True:self.fold(mousepos)
        else: self.dropdown()
    def scroll(self,direction):#Scrolls boxes up and down using scroll wheel
        if button.check_if_hover(mousepos) and direction == "up" and self.FullRect.height*-1+self.rect.height<=self.YDisplacement<0:button.YDisplacement +=50
        if button.check_if_hover(mousepos) and direction == "down"and self.FullRect.height*-1+self.rect.height<self.YDisplacement<=0:button.YDisplacement -=50
        self.FullRect.y = self.rect.y+self.YDisplacement #MUST BE AFTER CHANGE OF YDISPLACEMENT OR WON'T CHANGE X OF HIT BOX.
##################################################### Fucntions ###########################################################
def getAmountOfDays(month):
    year=int(year_button.currentOption_list[0])
    if month in (0,2, 4,6, 7, 9, 11): day_list=[x for x in range (1,32)]
    elif month==1:
        if year%4==0 and (not(year%100==0) or year%400==0): day_list=[x for x in range(1,30)]
        else: day_list=[x for x in range(1,29)]
    else: day_list=[x for x in range(1,31)]
    for num in day_list: num=str(num)
    return day_list
def findTotalHours():
    totalTime = datetime.timedelta(days= 0,hours=0,minutes=0,seconds=0,microseconds=0)
    for line in student.TimeWorkedList:
        time = line[-1]
        time = time.split(":")

        totalTime += datetime.timedelta(hours= int(time[0]),minutes = int(time[1]))
    totalHours = totalTime.seconds//(60*60) + totalTime.days*24#Find total hours from seconds and years assumes no one will work more than a year worth of hours
    totalMinutes = totalTime.seconds%(60*60)//60#Finds total minutes from seconds
    if len(str(totalMinutes)) < 2: #Making sure that minutes has the right number of zeros
        totalMinutes = "0"+str(totalMinutes)
    student.totalHours = str(totalHours)+":"+str(totalMinutes)
def sortdates():
    dates = []#Empty list to add all the dates to
    for days in student.TimeWorkedList:#Turns them all into dates to be sorted
        dates.append(datetime.datetime(int(days[3]),monthsOfYear.index(days[1]),int(days[2]),int(days[-1].split(":")[0]),int(days[-1].split(":")[1])))
    dates.sort()#Sorts the dates

    student.TimeWorkedList = []#Starts will a blank list so I can add them back in order
    for date in dates:#adds them back into the students file
        minutes = str(date.minute)
        if len(minutes) < 2:
            minutes = "0"+minutes
        student.TimeWorkedList.append([daysOfWeek[date.weekday()],monthsOfYear[int(date.month)],str(date.day),str(date.year),
                                  str(str(date.hour)+":"+minutes) ])

def addToHours(day,month,year):
    date = datetime.datetime(int(year_button.currentOption_list[0]),month_button.option_list.index(month_button.currentOption_list[0])+1,int(day_button.currentOption_list[0]))
    minutes = str(min_button.currentOption_list[0])
    if len(minutes) < 2:
        minutes = "0"+minutes
    hours = str(hours_button.currentOption_list[0])
    student.TimeWorkedList.append([daysOfWeek[date.weekday()],monthsOfYear[int(date.month)],str(date.day),str(date.year),
                                  str(hours+":"+minutes) ])

def save():
    sortdates()
    #sorts all the dates
    #opens a text file of the studentsNum.txt or example 123456.txt
    #if no text file called that creates one
    textFile = open(student.textFile,"w")
    for line in student.TimeWorkedList:
        textFile.write(str(line[0])+" "+str(line[1])+" "+str(line[2])+" "+str(line[3])+" "+str(line[4])+"\n")
    textFile.close()

def text(x,y,msg):#This function will be used as an easy way to make text on the display
    text = font.render(str(msg), False, (10, 10, 10))
    display.blit(text,(x-text.get_width()//2,y-text.get_height()//2))
###################################################### Displaying Functions ##########################################
def loginScreen():
    text(400,50,"LOGIN")
    text(250,275,"Student Number: ")
    text(275,310,"Password:")
def selectHours():
    text(400,50,"TIME WORKED")
    text(200,250,"MONTH")
    text(300,250,"DAY")
    text(400,250,"YEAR")
    text(550,225,"TIME WORKED")
    text(500,250,"HOURS")
    text(600,250,"MINUTES")
    if badDate == True:
        text(400,150,"The Date entered is invalid.")
def confirmDel():
    text(400,50,"Would you like to delete the date")
    text(400,75," ".join(student.TimeWorkedList[hours_List.numHit]))
def confirmHours():
    text(400,50,"CONFIRM HOURS")
    text(250,150,"Date selected:")
    text(255,175,"Time worked:")
    #Prints date
    date = datetime.datetime(int(year_button.currentOption_list[0]),month_button.option_list.index(month_button.currentOption_list[0])+1,int(day_button.currentOption_list[0]))
    msg = font.render(str(daysOfWeek[date.weekday()]+", "+monthsOfYear[date.month]+" "+str(date.day)+","+str(date.year)), False, (10, 10, 10))
    display.blit(msg,(335,140))
    #Prints time worked
    minutes = str(min_button.currentOption_list[0])
    if len(minutes) < 2:
        minutes = "0"+minutes
    hours = str(hours_button.currentOption_list[0])
    msg = font.render(str(hours+":"+minutes), False, (10, 10, 10))
    display.blit(msg,(335,165))
def sendMail():
    text(400,50,"SEND IN HOURS")
def saveHours():
    text(400,50,"SAVE HOURS")
    text(400,200,"Enter The name of the text file")
    if student.BadTextFileName == True:
        text(400,225,"Please enter a different text file name")
def sendHours():
    text(400,50,"SEND HOURS")
def mainMenu():
    text(400,50,"CO-OP HOURS")
    text(400,75,"You have "+student.totalHours+" Hours")
    text(400,100,"Welcome: "+student.studentNum)
def failToLog():#This Function will show if they fail to login
    text(400,175,"Your student Number or password was incorrect")
    text(400,200,"Please retry")
def sameTextName():
    text(400,200,"This text file exists would you like to overwrite it?")
def seeHours():
    text(400,50,"YOUR HOURS")

################################################ local vars #############################################################
loadScreen = True #Called at the first load of a screen
changeHours = False #Called when you want to go back to the change hours screen
badDate= False
pygame.init()
FPS=15
fpsclock=pygame.time.Clock()
display=pygame.display.set_mode((800,600))
pygame.display.set_caption("Hour Log")
font=pygame.font.SysFont("Arial", 16)
white=(255,255,255)
black=(0,0,0)
grey=(192,192,192)
brownish = (175, 149, 149)
#dates
daysOfWeek = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
monthsOfYear = ["","January","February","March","April","May","June","July","August","September","October","November","December"]

screen = "loginScreen" #This will be used to tell what screen The program is on like a enum
student = studentMail()#This will be all info keep about the student
################################################# main Loop ##############################################################
while True:
################################################# events ################################################################
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            for button in Button.buttons:#This will get text for textbox_buttons
                if type(button) is textbox_button:
                    if button.isSelected: button.setText(event.key)
        if event.type== pygame.MOUSEBUTTONDOWN:
            mousepos=pygame.mouse.get_pos()
            if event.button == 1:
                mousepos=pygame.mouse.get_pos()
############################################################# Button Functions ##########################################
                for button in Button.buttons:#This will check if buttons are being pressed
                #List
                    if type(button) == List and screen == "seeHours":
                        if button.onclick(mousepos):
                            screen = "confirmDel"
                            loadScreen = True

                #Textboxs
                    elif type(button) == textbox_button:
                        for buttons in Button.buttons:#This will deselect all other text boxes so you can't type in 2 at once
                            if type(button) == textbox_button: button.isSelected = False
                #press buttons
                    elif type(button)== press_button:#This is where all the button Functions Go
                #Login Screen
                        if button.text == "Login" and button.check_if_clicked(mousepos) and screen == "loginScreen":#Checking if they clicked on the login button
                            text(400,150,"Loading please wait...")
                            pygame.draw.rect(display,brownish,(0,165,800,75))
                            pygame.display.update()
                            student.login("".join(studentNumber_textbox.inputText),"".join(password_textbox.inputText)) #Trying to login to email
                            if student.failToLogin == False:
                                #Trys to open their text file if one isn't there make on for them
                                ###################### TODO make code to open text file
                                student.textFile = student.studentNum+".txt"
                                try:  #opens text file
                                    student.TimeWorkedList = [line.rstrip("\n").split() for line in open(student.textFile)]
                                except: #If it fails means no text file of that name is their
                                    textFile = open(student.textFile,"w")#Makes new textfile
                                    textFile.close()
                                    student.TimeWorkedList = []
                                findTotalHours()
                                screen = "mainMenu"
                                loadScreen = True
                                student.Online = True
                        elif button.text == "Login Offline" and button.check_if_clicked(mousepos) and screen == "loginScreen":#Checking if they clicked on the login offline button
                            text(400,150,"Loading please wait...")
                            pygame.draw.rect(display,brownish,(0,165,800,75))
                            pygame.display.update()
                            if len("".join(studentNumber_textbox.inputText)) == 0:
                                failToLogin = True #If the student Number is empty doesnt login
                            else:
                                student.loginOffline("".join(studentNumber_textbox.inputText)) #logins in offline
                                student.textFile = student.studentNum+".txt"
                                try:  #opens text file
                                    student.TimeWorkedList = [line.rstrip("\n").split() for line in open(student.textFile)]
                                except: #If it fails means no text file of that name is their
                                    textFile = open(student.textFile,"w")#Makes new textfile
                                    textFile.close()
                                    student.TimeWorkedList = []
                                findTotalHours()
                                screen = "mainMenu"
                                loadScreen = True
                                student.Online=False
                #Home Button. have it on many screen so isn't specified to screen
                        elif button.text == "HOME" and button.check_if_clicked(mousepos):
                            screen = "mainMenu"
                            loadScreen = True
                    #SelectHours
                        elif screen == "selectHours":
                            if button.text == "Input Hours" and button.check_if_clicked(mousepos):
                                screen = "confirmHours"
                                loadScreen = True
                    #ConfirmDel
                        elif screen == "confirmDel":
                            if button.text == "Cancel" and button.check_if_clicked(mousepos):
                                screen = "seeHours"
                                loadScreen = True
                            elif button.text == "Delete" and button.check_if_clicked(mousepos):
                                screen = "mainMenu"
                                loadScreen = True
                                student.TimeWorkedList.remove(student.TimeWorkedList[hours_List.numHit])
                                save()
                    #MainMenu
                        elif screen == "mainMenu":
                            if button.text == "LOGOUT" and button.check_if_clicked(mousepos):
                                student = studentMail()#Resets the student class so it loses all its info
                                screen = "loginScreen"
                                loadScreen = True
                            elif button.text == "See hours" and button.check_if_clicked(mousepos):
                                screen = "seeHours"
                                loadScreen = True
                            elif button.text == "Input Hours" and button.check_if_clicked(mousepos):
                                screen = "selectHours"
                                loadScreen = True
                            elif button.text == "Send Hours" and button.check_if_clicked(mousepos):
                                screen = "sendHours"
                                loadScreen = True
                            elif button.text == "Save Hours" and button.check_if_clicked(mousepos):
                                screen = "saveHours"
                                loadScreen = True
                    #SendHours
                        elif screen == "sendHours":
                            if button.text == "Cancel" and button.check_if_clicked(mousepos):
                                screen = "mainMenu"
                                loadScreen = True
                            elif button.text == "Send" and button.check_if_clicked(mousepos):
                                screen = "mainMenu"
                                loadScreen = True
                                text(400,150,"Sending e-mail please wait....")
                                pygame.display.update()
                                student.sendMail()
                            elif button.text == "Save" and button.check_if_clicked(mousepos):
                                screen = "saveHours"
                                loadScreen = True
                    #SametextName
                        elif screen == "sameTextName":
                            if button.text == "Cancel" and button.check_if_clicked(mousepos):
                                screen = "saveHours"
                                loadScreen = True
                            elif button.text == "Save" and button.check_if_clicked(mousepos):#saves the text file
                                textFile = open("".join(saveTextbox.inputText)+".txt","w")#Writing to the textFile of there name
                                textFile.write("From: "+student.studentNum+"\n\n"+"The Total Number of CO-OP hours worked is "+str(student.totalHours)+"\n\nThe days worked were:\n\n"+"\n".join(" ".join(x) for x in student.TimeWorkedList))
                                textFile.close()
                                screen = "mainMenu"
                                loadScreen = True
                    #SaveHours
                        elif screen == "saveHours":
                            if button.text == "Cancel" and button.check_if_clicked(mousepos):
                                screen = "mainMenu"
                                loadScreen = True
                            elif button.text == "Save" and button.check_if_clicked(mousepos):
                                try:#checks if a text file with that name is already there
                                    open("".join(saveTextbox.inputText)+".txt","r")
                                    if "".join(saveTextbox.inputText) == student.studentNum or len("".join(saveTextbox.inputText)) == 0:student.BadTextFileName = True
                                    else:
                                        screen = "sameTextName"
                                        loadScreen = True
                                except:
                                    if len("".join(saveTextbox.inputText)) == 0 or "".join(saveTextbox.inputText) == student.studentNum:
                                        student.BadTextFileName = True
                                    else:
                                        textFile = open("".join(saveTextbox.inputText)+".txt","w")#Writing to the textFile of there name
                                        textFile.write("From: "+student.studentNum+"\n\n"+"The Total Number of CO-OP hours worked is "+str(student.totalHours)+"\n\nThe days worked were:\n\n"+"\n".join(" ".join(x) for x in student.TimeWorkedList))
                                        textFile.close()
                                        screen = "mainMenu"
                                        loadScreen = True
                    #confirmHours
                        elif screen == "confirmHours":
                            if button.text == "CANCEL" and button.check_if_clicked(mousepos):
                                screen = "selectHours"
                                loadScreen = True
                            elif button.text == "Confirm" and button.check_if_clicked(mousepos):#This will add the hour to the list and save the list to the text file
                                addToHours(day_button.currentOption_list[0],month_button.currentOption_list[0],year_button.currentOption_list[0])
                                save()#saves to their textfile
                                findTotalHours()
                                loadScreen = True
                                screen = "selectHours"
                            elif button.text == "Change Hours" and button.check_if_clicked(mousepos):
                                changeHours = True
                                loadScreen = True
                                screen = "selectHours"
                    button.check_if_clicked(mousepos)#Check if button is clicked
            #Dropdown button scroll function.
            if event.button==4:#Scroll up
                for button in Button.buttons:#This will check if dropdown_buttons are being scrolled
                    if type(button) is dropdown_button and button.isDropDown == True: button.scroll("up")
                    elif type(button) is List: button.scroll("up")
            if event.button==5:#Scroll Down
                for button in Button.buttons:#This will check if dropdown_buttons are being scrolled
                    if type(button) is List: button.scroll("down")
                    elif type(button) is dropdown_button and button.isDropDown == True: button.scroll("down")

        if event.type==QUIT:#Check if they try and quit.
            ##TODO SET IT TO AUTO SAVE WHEN THEY TRY AND QUIT.
            student = 0#Resets students so people can't see their password after they leave
            pygame.quit()
            sys.exit()
################################################### loading screens ##########################################################
    if loadScreen == True: ##This will check if it has to load a new screen and if yes set up all the buttons for that screen.
        #Clear the screen of all buttons
        Button.buttons = []
        loadScreen = False
    #MainMenu
        if screen == "mainMenu":
            logout_button = press_button(650,500,"LOGOUT")
            seeHours_button = press_button(250,275,"See hours")
            inputHours_button = press_button(360,275,"Input Hours")
            if student.Online == True: #checks if they are logged in
                sendHours_button = press_button(470,275,"Send Hours")
            else: saveHours_button = press_button(470,275,"Save Hours")
    #CONFIRM HOURS
        elif screen == "confirmHours":
            cancel_button = press_button(650,500,"CANCEL")
            confirm_button = press_button(500,275,"Confirm")
            Change_button = press_button(200,275,"Change Hours")
    #Save hours
        elif screen == "saveHours":
            home_button = press_button(650,500,"HOME")
            save_button = press_button(500,275,"Save")
            saveTextbox = textbox_button(300,240,200,24,True)
            cancel_button = press_button(200,275,"Cancel")
    #confirmDel
        elif screen == "confirmDel":
            cancel_buttton = press_button(200,275,"Cancel")
            home_button = press_button(650,500,"HOME")
            del_button = press_button(500,275,"Delete")
    #SENDHOURS
        elif screen == "sendHours":
            home_button = press_button(650,500,"HOME")
            send_button = press_button(500,275,"Send")
            save_button = press_button(350,275,"Save")
            cancel_button = press_button(200,275,"Cancel")
        elif screen == "seeHours":
            hours_List = List(275,100,300,50,student.TimeWorkedList)
            home_button = press_button(650,500,"HOME")
    #SELECTHOURS
        elif screen == "selectHours" :#Things for hour screen
            if changeHours == True:#This will run if you want to go back to the changeHours screen without losing data
                Button.buttons.extend([month_button,day_button,year_button,min_button,home_button,inputHours_button,hours_button])
                changeHours = False
            else:#This will make a new fresh Screen
                month_button=dropdown_button(["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],150,275)
                setattr(month_button, "selected_month", 0)
                day_button=dropdown_button(["1"], 250, 275)
                year_button=dropdown_button(["2017", "2018", "2019", "2020", "2021", "2022", "2023", "2024", "2025", "2026"], 350, 275)
                setattr(year_button, "current_year", year_button.option_list[0])
                year=int(getattr(year_button, "current_year"))
                hours_button=dropdown_button([str(x) for x in range(1,24,1)],450,275)
                min_button=dropdown_button([str(x) for x in range(0,60,1)],550,275)
                home_button = press_button(650,500,"HOME")
                inputHours_button= press_button(50,500,"Input Hours")
    #LOGINSCREEN
        elif screen == "loginScreen":#Things for login screen
            studentNumber_textbox = textbox_button(325,265,200,24,True)
            password_textbox = textbox_button(325,300,200,24,False)
            login_button = press_button(300,400,"Login")
            loginOffline_button = press_button(425,400,"Login Offline")
    #SameTextName
        elif screen == "sameTextName":
            send_button = press_button(500,275,"Save")
            cancel_button = press_button(200,275,"Cancel")
 ############################################# displaying images ####################################################
    display.fill(brownish) #Redraws screen
    if screen == "loginScreen":#This will handle all drawing for loginScreen
        loginScreen()
        if student.failToLogin == True: failToLog()#Prints error message only when it fails to login
    elif screen == "selectHours":#This will handle all drawing for the hour selection screen.
        day_button.option_list=getAmountOfDays(month_button.option_list.index(month_button.currentOption_list[0]))
        selectHours()
    elif screen == "mainMenu":mainMenu()
    elif screen == "confirmHours":
        badDate = False
        try:confirmHours()
        except:
            screen = "selectHours"
            loadScreen = True
            changeHours = True
            badDate = True
    elif screen == "saveHours": saveHours()
    elif screen == "sameTextName": sameTextName()
    elif screen == "sendHours":sendHours()
    elif screen == "seeHours":seeHours()
    elif screen == "confirmDel":confirmDel()
    for button in Button.buttons: button.draw()#Draws all the buttons
    pygame.display.update()#Updates screen
    fpsclock.tick()#Ticks a frame
