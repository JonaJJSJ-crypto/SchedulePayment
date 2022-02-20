    #Implementation for a payment Based on schedule
    #This program accepts a .txt file with the next Format
    #Author: Jonathan Sánchez
    #Github Repo: JonaJJSJ-crypto

#Reading file
myFile = open("Schedule.txt","r")

#Detting Days Type
RegularDays = ['MO','TU','WE','TH','FR']
WeekEndDays = ['SA','SU']
#Hours
Minutes = [540,1080,1440]

MinTuple = [(540,25),(1080),(1440)]

WeekEndExtraFee = 5

def MinuteFormat(Hour_Format):
    Hour=int(Hour_Format[0:2])
    Min=int(Hour_Format[3:5])
    return Min + Hour*60


def payment(myTimes,IsWeekend):
    WEFee = WeekEndExtraFee
    if not IsWeekend:
        WEFee=0
    myTimeBegin=myTimes[0:5]
    #print(myTimeBegin)
    myTimeEnd=myTimes[6:11]
    #print(myTimeEnd)
    myTimeBegin= MinuteFormat(myTimeBegin)
    myTimeEnd= MinuteFormat(myTimeEnd)
    TMinutes=myTimeEnd-myTimeBegin
    print("Begin Time: ", myTimeBegin)
    print("End Time: ",myTimeEnd)
    print("Total Hours: ",TMinutes)

    pay=0;

    for x in Minutes:
        if myTimeBegin<=x:
            if myTimeBegin+TMinutes<=x:
                if x==540:
                    pay+= (25+WEFee)*TMinutes/60
                elif x==1080:
                    pay+= (15+WEFee)*TMinutes/60
                elif x==1440:
                    pay+= (20+WEFee)*TMinutes/60
                TMinutes=0;
                myTimeBegin=1441;
                #print("El pago es ",pay,' ',x)
            else:
                if x==540:
                    pay+= (25+WEFee)*(540-myTimeBegin)/60
                elif x==1080:
                    pay+= (15+WEFee)*(1080-myTimeBegin)/60
                elif x==1440:
                    pay+= (20+WEFee)*(1440-myTimeBegin)/60
                #print("El pago es ",pay,' ',x," Overlay ")
                myTimeBegin=x+1
                TMinutes=myTimeEnd-x

    print("Pay for the day: ",pay,'\n')

    return pay


for x in myFile:
    mySchedule = x
    print(mySchedule)
    myName = mySchedule[0:mySchedule.find('=')]
    print(myName)
    mySchedule = mySchedule[mySchedule.find('=')+1:len(mySchedule)]
    #print(mySchedule)

    Total_payment=0

    for y in RegularDays:
        myRTimes = mySchedule[mySchedule.find(y)+2:mySchedule.find(y)+13]
        if mySchedule.find(y) != -1:
            print(y,' ',myRTimes)
            Total_payment += payment(myRTimes,False)

    for y in WeekEndDays:
        myWETimes = mySchedule[mySchedule.find(y)+2:mySchedule.find(y)+13]
        if mySchedule.find(y) != -1:
            print(y,' ',myWETimes)
            Total_payment += payment(myWETimes,True)

    print(myName," Ha ganado: ", Total_payment," esta semana.\n\n")
