#Implementation for a payment Based on schedule
#Author: Jonathan Sánchez
#Github Repo: JonaJJSJ-crypto/SchedulePayment

#Reading file with names and Schedules
#Example of correct entry in the file: ASTRID=MO10:00-12:00,TH12:00-14:00,SU20:00-21:00
myFile = open("Schedule.txt","r")

#Setting Days Type
RegularDays = ['MO','TU','WE','TH','FR']
WeekEndDays = ['SA','SU']
#List of tuple consist of (final_hour_of_the_schedule,payment_of_the_schedule)
Minutes = [(540,25),(1080,15),(1440,20)]
#Extra fee that is granted for working during weekends
WeekEndExtraFee = 5

#Transform time (hh:mm) in 24h format to Minutes
def MinuteFormat(Hour_Format):
    try:
        Hour = int(Hour_Format[0:2])
        Min = int(Hour_Format[3:5])
        TimeMin = Min + Hour*60
        if Hour_Format == "00:00":
            return 1440
        elif TimeMin < 0 or TimeMin > 1440:
            return "Hour out of bounds"
        else:
            return Min + Hour*60

    except ValueError:
        print("\n !!!Error: incorrect hour_format: {}".format(Hour_Format),"!!!Correct format: hh:mm\n")


#Given working hours (hh:mm-hh:mm) & IsWeekEnd flag, returns payment
def payment(myTimes,IsWeekend):
    WEFee = WeekEndExtraFee
    if not IsWeekend:
        WEFee=0
    myTimeBegin=myTimes[0:5]
    myTimeEnd=myTimes[6:11]
    try:
        myTimeBegin= MinuteFormat(myTimeBegin)
        myTimeEnd= MinuteFormat(myTimeEnd)
        TMinutes=myTimeEnd-myTimeBegin
        if TMinutes < 0 or TMinutes > 1440:
            return "Incorrect working hours"
        #Internal Variable that holds the payment
        pay=0;

        for x in Minutes:
            if myTimeBegin<=x[0]:

                #Work hours starts and finishes in the same schedule
                if myTimeBegin+TMinutes<=x[0]:
                    pay+= (x[1]+WEFee)*TMinutes/60
                    TMinutes=0;
                    myTimeBegin=1441;

                #When work hours overlap in diferent schedules prepare for next schedule
                else:
                    pay+= (x[1]+WEFee)*(x[0]-myTimeBegin)/60
                    myTimeBegin=x[0]+1
                    TMinutes=myTimeEnd-x[0]
        print("     Pay for the Schedule: {}".format(round(pay)))

        return pay

    except TypeError:
        print("\n !!!Error: incorrect working hours format: {}".format(myTimes),"!!!Correct format: hh:mm-hh:mm\n")

#Calculate payment for each worker in the file
for x in myFile:
    mySchedule = x
    myName = mySchedule[0:mySchedule.find('=')]
    if mySchedule.find('=') == -1:
        print(" !!!Error: incorrect name format in: {}".format(mySchedule),"!!!Correct format: NAME=DDhh:mm-hh:mm,DDhh:mm-hh:mm\n")
        continue
    else:
        print(myName)
        mySchedule = mySchedule[mySchedule.find('=')+1:len(mySchedule)]

        #internal variable to store payment
        Total_payment=0
        try:
            for y in RegularDays:
                #Search in the entry for multiple appearances of the same day
                while mySchedule.find(y) != -1:
                    myTimes = mySchedule[mySchedule.find(y)+2:mySchedule.find(y)+13]
                    if mySchedule.find(y) != -1:
                        print(y,' ',myTimes,end='')
                        Total_payment += payment(myTimes,False)
                        mySchedule = mySchedule[0:mySchedule.find(y)]+mySchedule[mySchedule.find(y)+14:len(mySchedule)]
            for y in WeekEndDays:
                #Search in the entry for multiple appearances of the same day
                while mySchedule.find(y) != -1:
                    myTimes = mySchedule[mySchedule.find(y)+2:mySchedule.find(y)+13]
                    if mySchedule.find(y) != -1:
                        print(y,' ',myTimes,end='')
                        Total_payment += payment(myTimes,True)
                        mySchedule = mySchedule[0:mySchedule.find(y)]+mySchedule[mySchedule.find(y)+14:len(mySchedule)]
            if len(mySchedule) != 0:
                print("\n !!!Error: Working day not found in: {}".format(mySchedule),"!!!Correct days: MO,TU,WE,TH,FR,SA,SU\n")

        except TypeError:
            print("\n !!!Error: incorrect schedule format: {}".format(mySchedule),"!!!Correct format: DDhh:mm-hh:mm\n")


        print("The amount to pay {}".format(myName),"is: {}".format(round(Total_payment)),"USD.\n\n")
