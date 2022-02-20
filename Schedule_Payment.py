    #Implementation for a payment Based on schedule
    #This program accepts a .txt file with the next Format
    #Author: Jonathan Sánchez
    #Github Repo: JonaJJSJ-crypto

#Reading file with names and Schedules
#Example of a line in the file: ASTRID=MO10:00-12:00,TH12:00-14:00,SU20:00-21:00
myFile = open("Schedule.txt","r")

#Setting Days Type
RegularDays = ['MO','TU','WE','TH','FR']
WeekEndDays = ['SA','SU']
#List of tuple consist of (final_hour_of_the_schedule,payment_of_the_schedule)
#Final_hour_of_the_schedule is the total of minutes of that hours
Minutes = [(540,25),(1080,15),(1440,20)]
#Extra fee that is granted for working during weekends
WeekEndExtraFee = 5

#Recieves a string of the form (hh:mm) in 24 hours format and returns the total of minutes since (00:00)
def MinuteFormat(Hour_Format):
    Hour=int(Hour_Format[0:2])
    Min=int(Hour_Format[3:5])
    return Min + Hour*60

#Recieves a string of the form DDhh:mm-hh:mm & a boolean that confirms if is WeekEnd schedule
#Returns The total payment from the working schedule
def payment(myTimes,IsWeekend):
    #Safe the WeekEndExtraFee as a variable
    WEFee = WeekEndExtraFee
    #Change WeekEndExtraFee to 0 if is not weekend
    if not IsWeekend:
        WEFee=0
    #Set Entry hour
    myTimeBegin=myTimes[0:5]
    #print(myTimeBegin)
    #Set Exit hour
    myTimeEnd=myTimes[6:11]
    #print(myTimeEnd)
    # Change Entry and Exit hour to int Minute format
    myTimeBegin= MinuteFormat(myTimeBegin)
    myTimeEnd= MinuteFormat(myTimeEnd)
    #Calculate total worked time
    TMinutes=myTimeEnd-myTimeBegin
    # Prints the Schedule that will be use to calculate the payment
    ###print("Begin Time: ", myTimeBegin)
    ###print("End Time: ",myTimeEnd)
    ###print("Total Hours: ",TMinutes)

    #Internal Varible that holds the payment
    pay=0;

    #search for (Schedule,Payment) that correspond to the Schedule
    for x in Minutes:
        #Searches for the schedule in which the Work started
        if myTimeBegin<=x[0]:
            #Seaches if the worked started and ended in the same schedule
            #and calculates the payment and exits the calculation
            if myTimeBegin+TMinutes<=x[0]:
                pay+= (x[1]+WEFee)*TMinutes/60
                TMinutes=0;
                myTimeBegin=1441;
                #print("El pago es ",pay,' ',x)
            #If the worked didnt end in the same schedule calculates the payment
            #for the initial schedule, and Sets begin time ant total Hours
            #to the following schedule to allow a new calculation
            else:
                pay+= (x[1]+WEFee)*(x[0]-myTimeBegin)/60
                #print("El pago es ",pay,' ',x," Overlay ")
                myTimeBegin=x[0]+1
                TMinutes=myTimeEnd-x[0]
    #Prints the Payment calculation for the Schedule
    print("     Pay for the Schedule: ",pay)

    return pay

#search for each line "entry" in the File.
for x in myFile:
    #Saves the entry for manipulation
    mySchedule = x
    #print(mySchedule)
    #Stores name
    myName = mySchedule[0:mySchedule.find('=')]
    print(myName)
    #Re-assign the the entry on to schedule
    mySchedule = mySchedule[mySchedule.find('=')+1:len(mySchedule)]
    #print(mySchedule)

    #internal variable to store payment
    Total_payment=0

    #Searched in the schedule for regular days
    for y in RegularDays:
        #Search in the entry for multiple appearances of the same day
        while mySchedule.find(y) != -1:
            #Stores the Day and time in the format DDhh:mm
            myRTimes = mySchedule[mySchedule.find(y)+2:mySchedule.find(y)+13]
            if mySchedule.find(y) != -1:
                print(y,' ',myRTimes,end='')
                #Ask payment() function to calculate the the payment for the given Day and time
                Total_payment += payment(myRTimes,False)
                #Re-stores the Schedule entry ommiting the analized day and Schedule
                #This allows multpiple entries of time in the same day
                mySchedule = mySchedule[0:mySchedule.find(y)]+mySchedule[mySchedule.find(y)+14:len(mySchedule)]

    #Searched in the schedule for Weekend days
    for y in WeekEndDays:
        #Search in the entry for multiple appearances of the same day
        while mySchedule.find(y) != -1:
            #Stores the Day and time in the format DDhh:mm
            myWETimes = mySchedule[mySchedule.find(y)+2:mySchedule.find(y)+13]
            if mySchedule.find(y) != -1:
                print(y,' ',myWETimes,end='')
                #Ask payment() function to calculate the the payment for the given Day and time
                Total_payment += payment(myWETimes,True)
                #Re-stores the Schedule entry ommiting the analized day and Schedule
                #This allows multpiple entries of time in the same day
                mySchedule = mySchedule[0:mySchedule.find(y)]+mySchedule[mySchedule.find(y)+14:len(mySchedule)]

    print("The amount to pay ",myName," is: ",Total_payment," USD.\n\n")
