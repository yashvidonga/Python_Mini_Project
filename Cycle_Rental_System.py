import mysql.connector as sql
from tabulate import tabulate
import time
obj = sql.connect(host="localhost", user="root",
                  passwd="root", database="Cycle_Rental_System")
cursor = obj.cursor(buffered=True)
cursor.execute("Select * from Sales")
output = cursor.fetchall()
global rcount
rcount = cursor.rowcount


class RentalSystemBill:  # for Bill related functionality this Class is used
    def __init__(self, name, timec, timet, no, phone) -> None:
        self.name = name
        self.timec = timec
        self.timet = timet
        self.no = no
        self.phone = phone

    # This function Generates Values like return date and like which will be then displayed on the bill
    def Generate_Bill(self):
        curtime = time.localtime()
        global rcount
        cury = curtime.tm_year
        curm = curtime.tm_mon
        curh = curtime.tm_hour
        curd = curtime.tm_mday
        self.curdate = str(cury)+"-"+str(curm) + \
            "-"+str(curd)
        self.currenttime = str(
            curh) + ":" + str(curtime.tm_min) + ":" + str(curtime.tm_sec)
        per = 0
        self.percost = 0
        if(self.timec == 1):
            hr = int(input("\nEnter Number of Hours: "))
            curh += hr
            self.percost = 50
            per = 50 * hr
            if(curh >= 24):
                curd += 1
                curh -= 24

        elif(self.timec == 2):
            day = int(input("\nEnter Number of Days: "))
            curd += day
            self.percost = 350
            per = 350 * day
            if(curd > 30):
                curm += 1
                if(curm in [1, 3, 5, 7, 8, 10, 12]):
                    curd -= 31
                elif(curm in [2, 4, 6, 7, 9, 11]):
                    curd -= 30

        elif(self.timec == 3):
            mon = int(input("\nEnter Number of Months: "))
            curm += mon
            self.percost = 2400
            per = 2400 * mon
            if(curm > 12):
                cury += 1
                curm -= 12

        self.redate = str(cury)+"-"+str(curm) + \
            "-"+str(curd)
        self.retime = str(
            curh) + ":" + str(curtime.tm_min) + ":" + str(curtime.tm_sec)
        self.total = float(per)*int(self.no)
        rcount += 1
        cursor.execute("Insert into Sales values({},'{}','{}',{},{},'{}','{}','{}','{}',{},{})".format(
            rcount, self.name, self.phone, self.no, per, self.curdate, self.currenttime, self.redate, self.retime, self.total, 0))
        obj.commit()

    def PrintBill(self):  # This Function prints the Bill(in proper format)
        d = []
        d.append([self.no, self.percost, self.total])
        print("-"*105)
        print("\t\t\t\tCYCLE RENTAL SYSTEM")
        print("\t\t\t\t\tBILL")
        print("Name: ", self.name)
        print("Phone No.: ", self.phone)
        print("Date(YYYY-MM-DD): ", self.curdate, end="\t\t\t\t\t")
        print("Time(HH-MM-SS): ", self.currenttime)
        print("Return Date(YYYY-MM-DD): ", self.redate, end="\t\t\t\t")
        print("Return Time(HH-MM-SS): ", self.retime)
        print(tabulate(d, headers=["No. of Bikes",
              "Cost per Bike \nper Hr/Week/Day", "Total Cost"], tablefmt='psql', numalign="center"))
        print("Please Note: If Cycles are Returned Late, you are required to Pay a Fine\nFor being an Hour Late a Fine of Rs. 50 will be charged\nFor being a Day Late a Fine of Rs. 300 will be charged")
        print("\n", "-"*105)


class RentalSystemSales:  # This class has functionalities which will be used for Sales
    def salesall(self):  # Prints the Sales of the Shop and also Displayes the fines
        print("-"*140)
        print("\t\t\t\t\t\t\tCYCLE RENTAL SYSTEM")
        print("\t\t\t\t\t\t\t  SALES RECORDS")
        cursor.execute("Select * from Sales")
        output = cursor.fetchall()
        print(tabulate(output, headers=["SrNo", "Name", "Phone\nNo.", "No of\nCycles", "Cost per\nCycles", "Rent\nDate", "Rent\nTime",
                                        "Return\nDate", "Return\nTime", "Total\nCost", "Returned"], tablefmt='psql', numalign="center"))
        print("In the Returned Column\n0 - NOT Returned\n1 - Returned")
        print()
        cursor.execute("Select sum(No_of_Bikes),sum(Total_Cost) from Sales")
        totalrec = cursor.fetchall()
        print(tabulate(totalrec, headers=[
            "Total No. of Cycles Sold", "Total Earning"], tablefmt='psql', numalign="center"))
        print("\n\t\t\t\t\t\tFINES RECORDS")
        cursor.execute("Select * from Fines")
        totalfine = cursor.fetchall()
        print(tabulate(totalfine, headers=[
              "Name", "Fine Amount"], tablefmt='psql', numalign="center"))
        print("-"*140)


class RentalSystemReturn:  # This class deals with Return relates Functionalities
    def __init__(self, name) -> None:
        self.name = name

    def ReturnCycle(self):  # This Function checks the records and tells us if the bikes are being returned on time and if not then fines are alloted
        cursor.execute(
            "Select Name,Return_On_Date,Return_On_Time,Returned from Sales where Name = '{}'".format(self.name))
        self.data = cursor.fetchall()
        data = list(self.data)
        current = time.localtime()
        if(current.tm_mon not in [10, 11, 12] and current.tm_mday < 10):
            currentdate = str(current.tm_year) + "-0" + \
                str(current.tm_mon) + "-0" + str(current.tm_mday)
        elif(current.tm_mon not in [10, 11, 12]):
            currentdate = str(current.tm_year) + "-0" + \
                str(current.tm_mon) + "-" + str(current.tm_mday)
        elif(current.tm_mday < 10):
            currentdate = str(current.tm_year) + "-" + \
                str(current.tm_mon) + "-0" + str(current.tm_mday)
        else:
            currentdate = str(current.tm_year) + "-" + \
                str(current.tm_mon) + "-" + str(current.tm_mday)

        if(current.tm_hour in [1, 2, 3, 4, 5, 6, 7, 8, 9]):
            currenttime = str(current.tm_hour) + ":0" + \
                str(current.tm_min) + ":" + str(current.tm_sec)
        else:
            currenttime = str(current.tm_hour) + ":" + \
                str(current.tm_min) + ":" + str(current.tm_sec)
        print("-"*110)
        print("\t\t\t\t\t  CYCLE RENTAL SYSTEM")
        if (cursor.rowcount == 0):
            print("Record NOT Found")
            print("You will be returning to the start of the System")
            time.sleep(3)
        else:
            d1 = str(data[0][1])
            t1 = str(data[0][2])
            fine = 0
            if(currentdate > str(data[0][1])):
                print("You have been late in returning the cycles. ")
                fine = 300*(int(current.tm_mday)-int((d1.split('-'))[2]))
                print("Fine = Rs.", fine, "is required to be Paid by the Customer")
            elif(currentdate == str(data[0][1]) and currenttime > str(data[0][2])):
                print("You have been late in returning the cycles. ")
                fine = 50*(int(current.tm_hour)-int((t1.split(':'))[0]))
                print("Fine = Rs.", fine, "is required to be Paid by the Customer")
            elif(fine == 0):
                print("Thank You For Returning the Cycles on Time")

            if(fine != 0):
                cursor.execute(
                    "Insert into Fines values('{}',{})".format(self.name, fine))
                obj.commit()
            print("-"*110)
            cursor.execute(
                "Update Sales set Return_On_Date = '{}',Return_On_Time = '{}' ,Returned = True where Name = '{}'".format(currentdate, currenttime, self.name))
            obj.commit()


print("-"*110)
print("\t\t\t\t\t  CYCLE RENTAL SYSTEM")  # This is the Login Page
print("\t\t\t\t\t\tLOGIN")
username = input("Enter Your Username: ")
password = input("Enter Your Password: ")
cursor.execute(
    "Select * from Employee where Name = '{}' and Password = '{}'".format(username, password))
if(cursor.rowcount == 1):
    print("\n\t\t\t\t\t   LOGIN SUCCESSFUL")
    print("-"*110)
    choice = 1
    while(choice):
        choice = int(input(
            "\n1.Generate a Bill \n2.View Sales \n3.Return a Cycle \n4.Exit \nEnter your Choice: "))
        if(choice == 1):
            name = input("\nEnter Your Name: ")
            phone = input("\nEnter Your Phone No.: ")
            time_choice = int(input(
                "\nCost per cycle\nFor one Hour - Rs50\nFor one Day - Rs350\nFor one month - Rs2400\n1.Hourly\n2.Daily\n3.Monthly\nFor how much amount of time do you want to Rent the Cycle, Enter your Choice:"))
            no = input("\nEnter the No. of Cycle to be Rented: ")
            customer = RentalSystemBill(name, time_choice, 0, no, phone)
            customer.Generate_Bill()
            customer.PrintBill()

        elif(choice == 2):
            sale = RentalSystemSales()
            sale.salesall()

        elif(choice == 3):
            name = input(
                "\nEnter Your Name(has to be in the same format as in the bill): ")
            returncycle = RentalSystemReturn(name)
            returncycle.ReturnCycle()

        elif(choice == 4):
            time.sleep(2)
            print("\nThank You for using the System")
            break
else:
    print("LOGIN UNSUCCESSFUL\nPlease Restart The Program")
    print("-"*110)
