#Implementation for a payment Based on schedule
#This program accepts a .txt file with the next Format:
#NAME=DDhh:mm-hh:mm,DDhh:mm-hh:mm
#Author: Jonathan Sánchez
#Github Repo: JonaJJSJ-crypto/SchedulePayment

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
    if Hour_Format == "00:00":
        return 1440
    else:
        Hour=int(Hour_Format[0:2])
        Min=int(Hour_Format[3:5])
        return Min + Hour*60

#Validate that working Hours
#def ValidHours(TimeBegin,TimeEnd):
    #if TimeEnd-TimeBegin < 0:


#Recieves a string of the form DDhh:mm-hh:mm & a boolean that confirms if is WeekEnd schedule
#Returns The total payment from the working schedule
def payment(myTimes,IsWeekend):
    WEFee = WeekEndExtraFee
    if not IsWeekend:
        WEFee=0
    myTimeBegin=myTimes[0:5]
    myTimeEnd=myTimes[6:11]
    # Change working hours to int Minute format
    myTimeBegin= MinuteFormat(myTimeBegin)
    myTimeEnd= MinuteFormat(myTimeEnd)
    #Total worked time
    TMinutes=myTimeEnd-myTimeBegin
    # Print the Schedule that will be use to calculate the payment
    ###print("Begin Time: ", myTimeBegin)
    ###print("End Time: ",myTimeEnd)
    ###print("Total Hours: ",TMinutes)

    #Internal Variable that holds the payment
    pay=0;

    for x in Minutes:
        if myTimeBegin<=x[0]:
            #Work schedule starts and finishes in the same schedule
            if myTimeBegin+TMinutes<=x[0]:
                pay+= (x[1]+WEFee)*TMinutes/60
                TMinutes=0;
                myTimeBegin=1441;
            #When work hours overlap in diferent schedules prepare for next schedule
            else:
                pay+= (x[1]+WEFee)*(x[0]-myTimeBegin)/60
                myTimeBegin=x[0]+1
                TMinutes=myTimeEnd-x[0]
    print("     Pay for the Schedule: {}".format(pay))

    return pay

#search for each line "entry" in the File.
for x in myFile:
    #Saves the entry for manipulation
    mySchedule = x
    myName = mySchedule[0:mySchedule.find('=')]
    print(myName)
    mySchedule = mySchedule[mySchedule.find('=')+1:len(mySchedule)]

    #internal variable to store payment
    Total_payment=0

    for y in RegularDays:
        #Search in the entry for multiple appearances of the same day
        while mySchedule.find(y) != -1:
            #Stores the Day and time in the format DDhh:mm
            myRTimes = mySchedule[mySchedule.find(y)+2:mySchedule.find(y)+13]
            if mySchedule.find(y) != -1:
                print(y,' ',myRTimes,end='')
                Total_payment += payment(myRTimes,False)
                #Re-stores the Schedule entry ommiting the analized day and workhours
                mySchedule = mySchedule[0:mySchedule.find(y)]+mySchedule[mySchedule.find(y)+14:len(mySchedule)]

    for y in WeekEndDays:
        #Search in the entry for multiple appearances of the same day
        while mySchedule.find(y) != -1:
            #Stores the Day and time in the format DDhh:mm
            myWETimes = mySchedule[mySchedule.find(y)+2:mySchedule.find(y)+13]
            if mySchedule.find(y) != -1:
                print(y,' ',myWETimes,end='')
                Total_payment += payment(myWETimes,True)
                #Re-stores the Schedule entry ommiting the analized day and Schedule
                #This allows multpiple entries of time in the same day
                mySchedule = mySchedule[0:mySchedule.find(y)]+mySchedule[mySchedule.find(y)+14:len(mySchedule)]

    print("The amount to pay {}".format(myName),"is: {}".format(Total_payment),"USD.\n\n")
