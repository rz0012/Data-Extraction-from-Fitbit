#please also read readme. 

# install fitbit, pandas, datetime and matplotlib in  machine through terminal if Ubuntu or through cmd if windows. 
# use pip install (package) to install those 

import fitbit
import pandas as pd 
import datetime
import matplotlib as plt
import numpy as np
from fitbit.exceptions import HTTPTooManyRequests
from fitbit.exceptions import HTTPBadRequest
import sys 
from termcolor import colored, cprint
#gather_keys_oauth2 is a python file to use in this code for authorization purpose in fitbit
#it is already in the folder, so no need to move it. but be sure to use this files in the same directory. 
import gather_keys_oauth2 as Oauth2


# I have attached a readme file in the folder, be sure to read it to understand how you can get client id and client secret. 
CLIENT_ID = input("Please enter Client ID from fitbit registered app:")
CLIENT_SECRET = input("Please enter Client Secret from fitbit registered app:")


#here, we are using Oauth 2.0 for authorization purpose. it will take you to a website where you will be logging in 
#with your fitbit username and password and allow it to get the access/refresh tockens.
server = Oauth2.OAuth2Server(CLIENT_ID, CLIENT_SECRET)
server.browser_authorize()
ACCESS_TOKEN = str(server.fitbit.client.session.token['access_token'])
REFRESH_TOKEN = str(server.fitbit.client.session.token['refresh_token'])
auth2_client = fitbit.Fitbit(CLIENT_ID, CLIENT_SECRET, oauth2=True, access_token=ACCESS_TOKEN, refresh_token=REFRESH_TOKEN)


count = 0; 

print()
print(colored('important', 'red', attrs=['reverse', 'blink']))
print(colored('success', 'green', attrs=['reverse', 'blink']))
print(colored("\nplease enter values carefully, program failure might happen. \nNever leave the code running, be sure to exit as instructed further. \nWhenever entering names for the file, you do not need to put extensions. \nAlways put a slash after puting location if there is not one.  ", 'red', attrs=['reverse', 'blink']) )

countNew = 0

while countNew == 0:
    try:
        typ = int(input("please enter in what file type you want to put your data in, remember Excel will put all data in a single file but in different sheets\n(Please just enter the number): (101) .xlsx (Regular Excel File) (102) .csv :"))
        print()
        if typ == 102:
            locQuery = int(input("please enter the numbers as per the information: (150) same location for all files/data (151) different location for file/data as you choose options individually : "))
                
            if locQuery == 150:
                loc = input("please enter the location for all the .csv files: ")
            
            naam = int(input("please state if you want to name the data files/sheets manually or want it to be automated: (201) automated (202) not automated :"))
            break
        elif typ == 101:
            loc = input("please enter the location for excel file: ")    
            excelName = input("please enter the name you want to put for excel file: ")

            writer = pd.ExcelWriter(loc+ excelName + '.xlsx' , engine = 'openpyxl')
            break
        else:
            print(colored("please try again, you did not type the number as described" , 'red', attrs=['reverse', 'blink']))
            
    except ValueError or KeyError:
        print(colored("please try again, value must be a number or you did not write it precisely. ", 'red', attrs=['reverse', 'blink']))


print()


user1 = 199

while count == 0:

    print()
    print("\n\nHere is the list of data you can get from the fitbit API if you already allowed that in authorization")
    print("you can get data one by one or all together, please look over the options. It will run until you press 99 to exit")
    print("\n(1) Heart Rate Intraday, \n(2) Body Fat, \n(3) Body Weight, \n(4) Calories Intraday, \n(5) Sleep, \n(6) Distance Intraday, \n(7) Steps Intraday, \n(8) Calories, \n(9) CaloriesBMR, \n(10) steps, \n(11) distance, \n(12) minutesSedentary, \n(13) minutesLightlyActive, \n(14) minutesFairlyActive, \n(15) minutesVeryActive, \n(16) activityCalories, \n(17) BMI, \n(18) Food, \n(19) Water, \n(20) Floors, \n(21) Elevation, \n(22) Floors IntraDay, \n(23) Elevation IntraDay.  ")
    print("\n(0) Every data for the same date interval, \n(88) get data from a certain number to a certain number, \n(99) Exit. ")
    print()
    user = int(input("please only enter the number for particular data from above line you want, and be sure that you allowed that data when authorizing: "))
    print()
    
    
    user3 = 0
    user4 = -1
    if user == 88:
        user3 = int(input("please state the number you want to start getting data from: "))
        user4 = int(input("please state the number you want to end getting data to: "))
        
    if user == 0 or user == 88:
        y01 = int(input("please enter the start date year: "))
        m01 = int(input("please enter the start date month: "))
        d01 = int(input("please enter the start day date: "))
        y02 = int(input("please enter the end date year: "))
        m02 = int(input("please enter the end date month: "))
        d02 = int(input("please enter the end day date: "))

    if user == 1 or user == 0 or (user == 88 and user3 <= user4 and user3 == 1):
        user3 = user3 + 1
        try:
            if user ==1:
                y11 = int(input("please enter the start date year: "))
                m11 = int(input("please enter the start date month: "))
                d11 = int(input("please enter the start day date: "))
                y12 = int(input("please enter the end date year: "))
                m12 = int(input("please enter the end date month: "))
                d12 = int(input("please enter the end day date: "))
            else:
                y11 = y01
                m11 = m01
                d11 = d01
                y12 = y02
                m12 = m02
                d12 = d02


            startTime1 = pd.datetime(year = y11, month = m11, day = d11)
            endTime1 = pd.datetime(year = y12, month = m12, day = d12)



            date_list1 = []
            df_list1 = []
            allDates1 = pd.date_range(start=startTime1, end = endTime1)

            
            #to collect data from day to day
            for oneDate1 in allDates1:
                
                oneDate1 = oneDate1.date().strftime("%Y-%m-%d")
                
                oneDayData1 = auth2_client.intraday_time_series('activities/heart', base_date=oneDate1, detail_level='1sec')

                df1 = pd.DataFrame(oneDayData1['activities-heart-intraday']['dataset'])
                
                date_list1.append(oneDate1)

                df_list1.append(df1)

            final_df_list1 = []

            # it will get all the interative data  
            for date1, df1 in zip(date_list1, df_list1):
                if len(df1) == 0:
                    continue
                df1.loc[:,'date'] = pd.to_datetime(date1)
                final_df_list1.append(df1)

            # it will conactinate the data
            final_df1 = pd.concat(final_df_list1,axis = 0)
            final_df1.tail() 

            #finally path to add that .csv file
        
            if typ == 102:
                if naam == 202:
                    filename1 = input("please enter the name you want put for FitBit Heart Rate data file: ") 
                elif naam == 201:
                    filename1 = "Fitbit_Heart_Rate" 

                if locQuery == 151:
                    file1 = input("please enter location where you want to put the file: ")
                else:
                    file1 = loc    
                final_df1.to_csv(file1+ filename1 + '.csv', index = False)

            elif typ == 101:
                final_df1.to_excel(writer, sheet_name = 'Fitbit_Heart_Rate')
                writer.save()
            print(colored("you have successfully retrieved (1) heart rate intraday data, please keep track of it", 'green', attrs=['reverse', 'blink']) )
            
        except ValueError or KeyError:
            print()
            user1 = int(input(colored("you do not have any recorded value of (1) Heart Rate Intraday in your fitbit account or you might have put wrong date, press (99) to exit the program or press (199) to continue:  ", 'red', attrs=['reverse', 'blink'])))
            print()

        except HTTPTooManyRequests:
            print()
            user1 = int(input(colored("you have exceeded the requests limit which is 150 and you are being stopped at number (1) Heart Rate Intraday, please try again after an hour. \nplease look over green lines in terminal where it showed which data you have retrieved successfully, \nit will be helpful when you need to start getting data again from where it stopped.  \nplease press (99) to exit the program or press (199) to continue: ", 'red', attrs=['reverse', 'blink'])))
            print()
        except HTTPBadRequest:
            print()
            user1 = int(input(colored("you might not have this (1) Heart Rate Intraday data named recorded data in your fitbit records. \nplease press (99) to exit the program or press (199) to continue: ", 'red', attrs=['reverse', 'blink'])))
            print()
        if user1 == 99:
            break

    if user == 2 or user == 0 or (user == 88 and user3 <= user4 and user3 == 2):
        user3 = user3 + 1
        try:
            if user ==2:
                y21 = int(input("please enter the start date year: "))
                m21 = int(input("please enter the start date month: "))
                d21 = int(input("please enter the start day date: "))
                y22 = int(input("please enter the end date year: "))
                m22 = int(input("please enter the end date month: "))
                d22 = int(input("please enter the end day date: "))
            else:
                y21 = y01
                m21 = m01
                d21 = d01
                y22 = y02
                m22 = m02
                d22 = d02

            startTime2 = pd.datetime(year = y21, month = m21, day = d21)
            endTime2 = pd.datetime(year = y22, month = m22, day = d22)



            date_list2 = []
            df_list2 = []
            allDates2 = pd.date_range(start=startTime2, end = endTime2)

        
            for oneDate2 in allDates2:
                oneDate2 = oneDate2.date().strftime("%Y-%m-%d") 
    
                oneDayData2 = auth2_client.time_series('body/fat',user_id="-",base_date=oneDate2,period='1d')

                df2 = pd.DataFrame(oneDayData2['body-fat'])
                    
                date_list2.append(oneDate2)
                    
                df_list2.append(df2)
                    

            final_df2 = pd.concat(df_list2, axis = 0)

            #finally path to add that .csv file

            if typ == 102:
                if naam == 202:
                    filename2 = input("please enter the name you want put for FitBit Body Fat data file: ") 
                elif naam == 201:
                    filename2 = "Fitbit_Body_Fat" 

                if locQuery == 151:
                    file2 = input("please enter location where you want to put the file: ")
                else:
                    file2 = loc    
                final_df2.to_csv(file2+ filename2 + '.csv', index = False)

            elif typ == 101:
                final_df2.to_excel(writer, sheet_name = 'Fitbit_Body_Fat')
                writer.save()
            print(colored("you have successfully retrieved (2) body fat data, please keep track of it", 'green', attrs=['reverse', 'blink']) )
            
        except ValueError or KeyError:
            print()
            user1 = int(input(colored("you do not have any recorded value of (2) Body Fat in your fitbit account or you might have put wrong date, press (99) to exit the program or press (199) to continue:  ", 'red', attrs=['reverse', 'blink'])))
            print()

        except HTTPTooManyRequests:
            print()
            user1 = int(input(colored("you have exceeded the requests limit which is 150 and you are being stopped at number (2) Body Fat, please try again after an hour. \nplease look over green lines in terminal where it showed which data you have retrieved successfully, \nit will be helpful when you need to start getting data again from where it stopped.  \nplease press (99) to exit the program or press (199) to continue: ", 'red', attrs=['reverse', 'blink'])))
            print()
        except HTTPBadRequest:
            print()
            user1 = int(input(colored("you might not have this (2) Body Fat data named recorded data in your fitbit records. \nplease press (99) to exit the program or press (199) to continue: ", 'red', attrs=['reverse', 'blink'])))
            print()
        if user1 == 99:
            break

    if user == 3 or user == 0 or (user == 88 and user3 <= user4 and user3 == 3):
        user3 = user3+1
        try:
            if user ==3:
                y31 = int(input("please enter the start date year: "))
                m31 = int(input("please enter the start date month: "))
                d31 = int(input("please enter the start day date: "))
                y32 = int(input("please enter the end date year: "))
                m32 = int(input("please enter the end date month: "))
                d32 = int(input("please enter the end day date: "))
            else:
                y31 = y01
                m31 = m01
                d31 = d01
                y32 = y02
                m32 = m02
                d32 = d02


            startTime3 = pd.datetime(year = y31, month = m31, day = d31)
            endTime3 = pd.datetime(year = y32, month = m32, day = d32)



            date_list3 = []
            df_list3 = []
            allDates3 = pd.date_range(start=startTime3, end = endTime3)

        
            for oneDate3 in allDates3:
                oneDate3 = oneDate3.date().strftime("%Y-%m-%d") 
    
                oneDayData3 = auth2_client.time_series('body/weight',user_id="-",base_date=oneDate3,period='1d')

                df3 = pd.DataFrame(oneDayData3['body-weight'])
                    
                date_list3.append(oneDate3)
                    
                df_list3.append(df3)
                    

            final_df3 = pd.concat(df_list3, axis = 0)
            #finally path to add that .csv file

            if typ == 102:
                if naam == 202:
                    filename3 = input("please enter the name you want put for FitBit Body Weight data file: ") 
                elif naam == 201:
                    filename3 = "Fitbit_Body_Weight" 

                if locQuery == 151:
                    file3 = input("please enter location where you want to put the file: ")
                else:
                    file3 = loc    
                final_df3.to_csv(file3+ filename3 + '.csv', index = False)

            elif typ == 101:
                final_df3.to_excel(writer, sheet_name = 'Fitbit_Body_Weight')
                writer.save()
            print(colored("you have successfully retrieved (3) body weight data, please keep track of it", 'green', attrs=['reverse', 'blink']) )
            
        except ValueError or KeyError:
            print()
            user1 = int(input(colored("you do not have any recorded value of (3) Body Weight in your fitbit account or you might have put wrong date, press (99) to exit the program or press (199) to continue:  ", 'red', attrs=['reverse', 'blink'])))
            print()

        except HTTPTooManyRequests:
            print()
            user1 = int(input(colored("you have exceeded the requests limit which is 150 and you are being stopped at number (3) Body Weight, please try again after an hour. \nplease look over green lines in terminal where it showed which data you have retrieved successfully, \nit will be helpful when you need to start getting data again from where it stopped.  \nplease press (99) to exit the program or press (199) to continue: ", 'red', attrs=['reverse', 'blink'])))
            print()
        except HTTPBadRequest:
            print()
            user1 = int(input(colored("you might not have this (3) Body Weight data named recorded data in your fitbit records. \nplease press (99) to exit the program or press (199) to continue: ", 'red', attrs=['reverse', 'blink'])))
            print()
        if user1 == 99:
            break

    if user == 4 or user == 0 or (user == 88 and user3 <= user4 and user3 == 4):
        user3 = user3 + 1
        try:
            if user ==4:
                y41 = int(input("please enter the start date year: "))
                m41 = int(input("please enter the start date month: "))
                d41 = int(input("please enter the start day date: "))
                y42 = int(input("please enter the end date year: "))
                m42 = int(input("please enter the end date month: "))
                d42 = int(input("please enter the end day date: "))
            else:
                y41 = y01
                m41 = m01
                d41 = d01
                y42 = y02
                m42 = m02
                d42 = d02

            startTime4 = pd.datetime(year = y41, month = m41, day = d41)
            endTime4 = pd.datetime(year = y42, month = m42, day = d42)



            date_list4 = []
            df_list4 = []
            allDates4 = pd.date_range(start=startTime4, end = endTime4)

        
            #to collect data from day to day
            for oneDate4 in allDates4:
                
                oneDate4 = oneDate4.date().strftime("%Y-%m-%d")
                
                oneDayData4 = auth2_client.intraday_time_series('activities/calories', base_date=oneDate4, detail_level='1min')

                df4 = pd.DataFrame(oneDayData4['activities-calories-intraday']['dataset'])
                
                date_list4.append(oneDate4)

                df_list4.append(df4)

            final_df_list4 = []

            # it will get all the interative data  
            for date4, df4 in zip(date_list4, df_list4):
                if len(df4) == 0:
                    continue
                df4.loc[:,'date'] = pd.to_datetime(date4)
                final_df_list4.append(df4)

            # it will conactinate the data
            final_df4 = pd.concat(final_df_list4,axis = 0)
            final_df4.tail() 

            if typ == 102:
                if naam == 202:
                    filename4 = input("please enter the name you want put for FitBit Calories IntraDay data file: ") 
                elif naam == 201:
                    filename4 = "Fitbit_Calories_IntraDay" 

                if locQuery == 151:
                    file4 = input("please enter location where you want to put the file: ")
                else:
                    file4 = loc    
                final_df4.to_csv(file4+ filename4 + '.csv', index = False)

            elif typ == 101:
                final_df4.to_excel(writer, sheet_name = 'Fitbit_Calories_IntraDay')
                writer.save()
            print(colored("you have successfully retrieved (4) calories intraday data, please keep track of it", 'green', attrs=['reverse', 'blink']) )
            
        except ValueError or KeyError:
            print()
            user1 = int(input(colored("you do not have any recorded value of (4) Calories Intraday in your fitbit account or you might have put wrong date, press (99) to exit the program or press (199) to continue:  ", 'red', attrs=['reverse', 'blink'])))
            print()

        except HTTPTooManyRequests:
            print()
            user1 = int(input(colored("you have exceeded the requests limit which is 150 and you are being stopped at number (4) Calories Intraday, please try again after an hour. \nplease look over green lines in terminal where it showed which data you have retrieved successfully, \nit will be helpful when you need to start getting data again from where it stopped.  \nplease press (99) to exit the program or press (199) to continue: ", 'red', attrs=['reverse', 'blink'])))
            print()
        except HTTPBadRequest:
            print()
            user1 = int(input(colored("you might not have this (4) Calories Intraday data named recorded data in your fitbit records. \nplease press (99) to exit the program or press (199) to continue: ", 'red', attrs=['reverse', 'blink'])))
            print()
        if user1 == 99:
            break

    if user == 5 or user == 0 or (user == 88 and user3 <= user4 and user3 == 5):
        user3 = user3 + 1
        try:
            if user ==5:
                y51 = int(input("please enter the start date year: "))
                m51 = int(input("please enter the start date month: "))
                d51 = int(input("please enter the start day date: "))
                y52 = int(input("please enter the end date year: "))
                m52 = int(input("please enter the end date month: "))
                d52 = int(input("please enter the end day date: "))
            else:
                y51 = y01
                m51 = m01
                d51 = d01
                y52 = y02
                m52 = m02
                d52 = d02


            startTime5 = pd.datetime(year = y51, month = m51, day = d51)
            endTime5 = pd.datetime(year = y52, month = m52, day = d52)



            date_list5 = []
            df_list5 = []
            allDates5 = pd.date_range(start=startTime5, end = endTime5)

        
            for oneDate5 in allDates5:
                
                oneDayData5 = auth2_client.get_sleep(date=oneDate5)

                df5 = pd.DataFrame(oneDayData5['sleep'])
                
                date_list5.append(oneDate5)
                
                df_list5.append(df5)
                
                
            final_df_list5 = []


            for date5, df5 in zip(date_list5, df_list5):

                if len(df5) == 0:
                    continue
                
                df5.loc[:, 'date'] = pd.to_datetime(date5)
                
                final_df_list5.append(df5)

            final_df5 = pd.concat(final_df_list5, axis = 0)
            
            if typ == 102:
                if naam == 202:
                    filename5 = input("please enter the name you want put for FitBit Sleep data file: ") 
                elif naam == 201:
                    filename5 = "Fitbit_Sleep" 

                if locQuery == 151:
                    file5 = input("please enter location where you want to put the file: ")
                else:
                    file5 = loc    
                final_df5.to_csv(file5+ filename5 + '.csv', index = False)

            elif typ == 101:
                final_df5.to_excel(writer, sheet_name = 'Fitbit_Sleep')
                writer.save()
            print(colored("you have successfully retrieved (5) sleep data, please keep track of it", 'green', attrs=['reverse', 'blink']) )
            
        except ValueError or KeyError:
            print()
            user1 = int(input(colored("you do not have any recorded value of (5) Sleep in your fitbit account or you might have put wrong date, press (99) to exit the program or press (199) to continue:  ", 'red', attrs=['reverse', 'blink'])))
            print()

        except HTTPTooManyRequests:
            print()
            user1 = int(input(colored("you have exceeded the requests limit which is 150 and you are being stopped at number (5) Sleep, please try again after an hour. \nplease look over green lines in terminal where it showed which data you have retrieved successfully, \nit will be helpful when you need to start getting data again from where it stopped.  \nplease press (99) to exit the program or press (199) to continue: ", 'red', attrs=['reverse', 'blink'])))
            print()
        except HTTPBadRequest:
            print()
            user1 = int(input(colored("you might not have this (5) Sleep data named recorded data in your fitbit records. \nplease press (99) to exit the program or press (199) to continue: ", 'red', attrs=['reverse', 'blink'])))
            print()
        if user1 == 99:
            break

    if user == 6 or user == 0 or (user == 88 and user3 <= user4 and user3 == 6):
        user3 = user3 + 1
        try:
            if user ==6:
                y61 = int(input("please enter the start date year: "))
                m61 = int(input("please enter the start date month: "))
                d61 = int(input("please enter the start day date: "))
                y62 = int(input("please enter the end date year: "))
                m62 = int(input("please enter the end date month: "))
                d62 = int(input("please enter the end day date: "))
            else:
                y61 = y01
                m61 = m01
                d61 = d01
                y62 = y02
                m62 = m02
                d62 = d02

            startTime6 = pd.datetime(year = y61, month = m61, day = d61)
            endTime6 = pd.datetime(year = y62, month = m62, day = d62)



            date_list6 = []
            df_list6 = []
            allDates6 = pd.date_range(start=startTime6, end = endTime6)

        
            #to collect data from day to day
            for oneDate6 in allDates6:
                
                oneDate6 = oneDate6.date().strftime("%Y-%m-%d")
                
                oneDayData6 = auth2_client.intraday_time_series('activities/distance',base_date=oneDate6, detail_level='1min')

                df6 = pd.DataFrame(oneDayData6['activities-distance-intraday']['dataset'])
                
                date_list6.append(oneDate6)

                df_list6.append(df6)

            final_df_list6 = []

            # it will get all the interative data  
            for date6, df6 in zip(date_list6, df_list6):
                if len(df6) == 0:
                    continue
                df6.loc[:,'date'] = pd.to_datetime(date6)
                final_df_list6.append(df6)

            # it will conactinate the data
            final_df6 = pd.concat(final_df_list6,axis = 0)
            final_df6.tail() 

            if typ == 102:
                if naam == 202:
                    filename6 = input("please enter the name you want put for FitBit Distance Intraday data file: ") 
                elif naam == 201:
                    filename6 = "Fitbit_Distance_Intraday"

                if locQuery == 151:
                    file6 = input("please enter location where you want to put the file: ")
                else:
                    file6 = loc    
                final_df6.to_csv(file6+ filename6 + '.csv', index = False)

            elif typ == 101:
                final_df6.to_excel(writer, sheet_name = 'Fitbit_Distance_IntraDay')
                writer.save()
            print(colored("you have successfully retrieved (6) distance intraday data, please keep track of it", 'green', attrs=['reverse', 'blink']) )
            
        except ValueError or KeyError:
            print()
            user1 = int(input(colored("you do not have any recorded value of (6) Distance Intraday in your fitbit account or you might have put wrong date, press (99) to exit the program or press (199) to continue:  ", 'red', attrs=['reverse', 'blink'])))
            print()

        except HTTPTooManyRequests:
            print()
            user1 = int(input(colored("you have exceeded the requests limit which is 150 and you are being stopped at number (6) Distance Intraday, please try again after an hour. \nplease look over green lines in terminal where it showed which data you have retrieved successfully, \nit will be helpful when you need to start getting data again from where it stopped.  \nplease press (99) to exit the program or press (199) to continue: ", 'red', attrs=['reverse', 'blink'])))
            print()
        except HTTPBadRequest:
            print()
            user1 = int(input(colored("you might not have this (6) Distance Intraday data named recorded data in your fitbit records. \nplease press (99) to exit the program or press (199) to continue: ", 'red', attrs=['reverse', 'blink'])))
            print()
        if user1 == 99:
            break

    if user == 7 or user == 0 or (user == 88 and user3 <= user4 and user3 == 7):
        user3 = user3 + 1
        try:
            if user ==7:
                y71 = int(input("please enter the start date year: "))
                m71 = int(input("please enter the start date month: "))
                d71 = int(input("please enter the start day date: "))
                y72 = int(input("please enter the end date year: "))
                m72 = int(input("please enter the end date month: "))
                d72 = int(input("please enter the end day date: "))
            else:
                y71 = y01
                m71 = m01
                d71 = d01
                y72 = y02
                m72 = m02
                d72 = d02

            startTime7 = pd.datetime(year = y71, month = m71, day = d71)
            endTime7 = pd.datetime(year = y72, month = m72, day = d72)



            date_list7 = []
            df_list7 = []
            allDates7 = pd.date_range(start=startTime7, end = endTime7)

        
            #to collect data from day to day
            for oneDate7 in allDates7:
                
                oneDate7 = oneDate7.date().strftime("%Y-%m-%d")
                
                oneDayData7 = auth2_client.intraday_time_series('activities/steps', base_date=oneDate7, detail_level='1min')

                df7 = pd.DataFrame(oneDayData7['activities-steps-intraday']['dataset'])
                
                date_list7.append(oneDate7)

                df_list7.append(df7)

            final_df_list7 = []

            # it will get all the interative data  
            for date7, df7 in zip(date_list7, df_list7):
                if len(df7) == 0:
                    continue
                df7.loc[:,'date'] = pd.to_datetime(date7)
                final_df_list7.append(df7)

            # it will conactinate the data
            final_df7 = pd.concat(final_df_list7,axis = 0)
            final_df7.tail() 

            if typ == 102:
                if naam == 202:
                    filename7 = input("please enter the name you want put for FitBit Steps Intraday data file: ") 
                elif naam == 201:
                    filename7 = "Fitbit_Steps_Intraday"

                if locQuery == 151:
                    file7 = input("please enter location where you want to put the file: ")
                else:
                    file7 = loc    
                final_df7.to_csv(file7+ filename7 + '.csv', index = False)

            elif typ == 101:
                final_df7.to_excel(writer, sheet_name = 'Fitbit_Steps_IntraDay')
                writer.save()
            print(colored("you have successfully retrieved (7) steps intraday data, please keep track of it", 'green', attrs=['reverse', 'blink']) )
            
        except ValueError or KeyError:
            print()
            user1 = int(input(colored("you do not have any recorded value of (7) Steps Intraday in your fitbit account or you might have put wrong date, press (99) to exit the program or press (199) to continue:  ", 'red', attrs=['reverse', 'blink'])))
            print()

        except HTTPTooManyRequests:
            print()
            user1 = int(input(colored("you have exceeded the requests limit which is 150 and you are being stopped at number (7) Steps Intraday, please try again after an hour. \nplease look over green lines in terminal where it showed which data you have retrieved successfully, \nit will be helpful when you need to start getting data again from where it stopped.  \nplease press (99) to exit the program or press (199) to continue: ", 'red', attrs=['reverse', 'blink'])))
            print()
        except HTTPBadRequest:
            print()
            user1 = int(input(colored("you might not have this (7) Steps Intraday data named recorded data in your fitbit records. \nplease press (99) to exit the program or press (199) to continue: ", 'red', attrs=['reverse', 'blink'])))
            print()
        if user1 == 99:
            break

    if user == 8 or user == 0 or (user == 88 and user3 <= user4 and user3 == 8):
        user3 = user3 + 1
        try:
            if user ==8:
                y81 = int(input("please enter the start date year: "))
                m81 = int(input("please enter the start date month: "))
                d81 = int(input("please enter the start day date: "))
                y82 = int(input("please enter the end date year: "))
                m82 = int(input("please enter the end date month: "))
                d82 = int(input("please enter the end day date: "))
            else:
                y81 = y01
                m81 = m01
                d81 = d01
                y82 = y02
                m82 = m02
                d82 = d02

            startTime8 = pd.datetime(year = y81, month = m81, day = d81)
            endTime8 = pd.datetime(year = y82, month = m82, day = d82)



            date_list8 = []
            df_list8 = []
            allDates8 = pd.date_range(start=startTime8, end = endTime8)

        
            for oneDate8 in allDates8:
                oneDate8 = oneDate8.date().strftime("%Y-%m-%d") 
                
                oneDayData8 = auth2_client.time_series('activities/calories',user_id="-",base_date=oneDate8,period='1d')

                df8 = pd.DataFrame(oneDayData8['activities-calories'])
                    
                date_list8.append(oneDate8)
                    
                df_list8.append(df8)
                    

            final_df8 = pd.concat(df_list8, axis = 0)
                
            if typ == 102:
                if naam == 202:
                    filename8 = input("please enter the name you want put for FitBit Calories data file: ") 
                elif naam == 201:
                    filename8 = "Fitbit_Calories"

                if locQuery == 151:
                    file8 = input("please enter location where you want to put the file: ")
                else:
                    file8 = loc    
                final_df8.to_csv(file8+ filename8 + '.csv', index = False)

            elif typ == 101:
                final_df8.to_excel(writer, sheet_name = 'Fitbit_Calories')
                writer.save()
            print(colored("you have successfully retrieved (8) calories data, please keep track of it", 'green', attrs=['reverse', 'blink']) )
            
        except ValueError or KeyError:
            print()
            user1 = int(input(colored("you do not have any recorded value of (8) Calories in your fitbit account or you might have put wrong date, press (99) to exit the program or press (199) to continue:  ", 'red', attrs=['reverse', 'blink'])))
            print()

        except HTTPTooManyRequests:
            print()
            user1 = int(input(colored("you have exceeded the requests limit which is 150 and you are being stopped at number (8) Calories, please try again after an hour. \nplease look over green lines in terminal where it showed which data you have retrieved successfully, \nit will be helpful when you need to start getting data again from where it stopped.  \nplease press (99) to exit the program or press (199) to continue: ", 'red', attrs=['reverse', 'blink'])))
            print()
        except HTTPBadRequest:
            print()
            user1 = int(input(colored("you might not have this (8) Calories data named recorded data in your fitbit records. \nplease press (99) to exit the program or press (199) to continue: ", 'red', attrs=['reverse', 'blink'])))
            print()
        if user1 == 99:
            break

    if user == 9 or user == 0 or (user == 88 and user3 <= user4 and user3 == 9):
        user3 = user3 + 1
        try:
            if user ==9:
                y91 = int(input("please enter the start date year: "))
                m91 = int(input("please enter the start date month: "))
                d91 = int(input("please enter the start day date: "))
                y92 = int(input("please enter the end date year: "))
                m92 = int(input("please enter the end date month: "))
                d92 = int(input("please enter the end day date: "))
            else:
                y91 = y01
                m91 = m01
                d91 = d01
                y92 = y02
                m92 = m02
                d92 = d02


            startTime9 = pd.datetime(year = y91, month = m91, day = d91)
            endTime9 = pd.datetime(year = y92, month = m92, day = d92)



            date_list9 = []
            df_list9 = []
            allDates9 = pd.date_range(start=startTime9, end = endTime9)

        
            for oneDate9 in allDates9:
                oneDate9 = oneDate9.date().strftime("%Y-%m-%d") 
                
                oneDayData9 = auth2_client.time_series('activities/caloriesBMR',user_id="-",base_date=oneDate9,period='1d')

                df9 = pd.DataFrame(oneDayData9['activities-caloriesBMR'])
                    
                date_list9.append(oneDate9)
                    
                df_list9.append(df9)
                    

            final_df9 = pd.concat(df_list9, axis = 0)
                
            if typ == 102:
                if naam == 202:
                    filename9 = input("please enter the name you want put for FitBit CaloriesBMR data file: ") 
                elif naam == 201:
                    filename9 = "Fitbit_CaloriesBMR"

                if locQuery == 151:
                    file9 = input("please enter location where you want to put the file: ")
                else:
                    file9 = loc    
                final_df9.to_csv(file9+ filename9 + '.csv', index = False)

            elif typ == 101:
                final_df9.to_excel(writer, sheet_name = 'Fitbit_CaloriesBMR')
                writer.save()
            print(colored("you have successfully retrieved (9) caloriesBMR data, please keep track of it", 'green', attrs=['reverse', 'blink']) )
            
        except ValueError or KeyError:
            print()
            user1 = int(input(colored("you do not have any recorded value of (9) CaloriesBMR in your fitbit account or you might have put wrong date, press (99) to exit the program or press (199) to continue:  ", 'red', attrs=['reverse', 'blink'])))
            print()

        except HTTPTooManyRequests:
            print()
            user1 = int(input(colored("you have exceeded the requests limit which is 150 and you are being stopped at number (9) CaloriesBMR, please try again after an hour. \nplease look over green lines in terminal where it showed which data you have retrieved successfully, \nit will be helpful when you need to start getting data again from where it stopped.  \nplease press (99) to exit the program or press (199) to continue: ", 'red', attrs=['reverse', 'blink'])))
            print()
        except HTTPBadRequest:
            print()
            user1 = int(input(colored("you might not have this (9) CaloriesBMR data named recorded data in your fitbit records. \nplease press (99) to exit the program or press (199) to continue: ", 'red', attrs=['reverse', 'blink'])))
            print()
        if user1 == 99:
            break

    if user == 10 or user == 0 or (user == 88 and user3 <= user4 and user3 == 10):
        user3 = user3 + 1
        try:
            if user ==10:
                y101 = int(input("please enter the start date year: "))
                m101 = int(input("please enter the start date month: "))
                d101 = int(input("please enter the start day date: "))
                y102 = int(input("please enter the end date year: "))
                m102 = int(input("please enter the end date month: "))
                d102 = int(input("please enter the end day date: "))
            else:
                y101 = y01
                m101 = m01
                d101 = d01
                y102 = y02
                m102 = m02
                d102 = d02


            startTime10 = pd.datetime(year = y101, month = m101, day = d101)
            endTime10 = pd.datetime(year = y102, month = m102, day = d102)



            date_list10 = []
            df_list10 = []
            allDates10 = pd.date_range(start=startTime10, end = endTime10)

       
            for oneDate10 in allDates10:
                oneDate10 = oneDate10.date().strftime("%Y-%m-%d") 
                
                oneDayData10 = auth2_client.time_series('activities/steps',user_id="-",base_date=oneDate10,period='1d')

                df10 = pd.DataFrame(oneDayData10['activities-steps'])
                    
                date_list10.append(oneDate10)
                    
                df_list10.append(df10)
                    

            final_df10 = pd.concat(df_list10, axis = 0)
                
            if typ == 102:
                if naam == 202:
                    filename10 = input("please enter the name you want put for FitBit Steps data file: ") 
                elif naam == 201:
                    filename10 = "Fitbit_Steps"

                if locQuery == 151:
                    file10 = input("please enter location where you want to put the file: ")
                else:
                    file10 = loc    
                final_df10.to_csv(file10+ filename10 + '.csv', index = False)

            elif typ == 101:
                final_df10.to_excel(writer, sheet_name = 'Fitbit_Steps')
                writer.save()
            print(colored("you have successfully retrieved (10) steps data, please keep track of it", 'green', attrs=['reverse', 'blink']) )
            
        except ValueError or KeyError:
            print()
            user1 = int(input(colored("you do not have any recorded value of (10) Steps in your fitbit account or you might have put wrong date, press (99) to exit the program or press (199) to continue:  ", 'red', attrs=['reverse', 'blink'])))
            print()

        except HTTPTooManyRequests:
            print()
            user1 = int(input(colored("you have exceeded the requests limit which is 150 and you are being stopped at number (10) Steps, please try again after an hour. \nplease look over green lines in terminal where it showed which data you have retrieved successfully, \nit will be helpful when you need to start getting data again from where it stopped.  \nplease press (99) to exit the program or press (199) to continue: ", 'red', attrs=['reverse', 'blink'])))
            print()
        except HTTPBadRequest:
            print()
            user1 = int(input(colored("you might not have this (10) Steps data named recorded data in your fitbit records. \nplease press (99) to exit the program or press (199) to continue: ", 'red', attrs=['reverse', 'blink'])))
            print()
        if user1 == 99:
           break

    if user == 11 or user == 0 or (user == 88 and user3 <= user4 and user3 == 11):
        user3 = user3 + 1
        try:
            if user ==11:
                y111 = int(input("please enter the start date year: "))
                m111 = int(input("please enter the start date month: "))
                d111 = int(input("please enter the start day date: "))
                y112 = int(input("please enter the end date year: "))
                m112 = int(input("please enter the end date month: "))
                d112 = int(input("please enter the end day date: "))
            else:
                y111 = y01
                m111 = m01
                d111 = d01
                y112 = y02
                m112 = m02
                d112 = d02

            startTime11 = pd.datetime(year = y111, month = m111, day = d111)
            endTime11 = pd.datetime(year = y112, month = m112, day = d112)



            date_list11 = []
            df_list11 = []
            allDates11 = pd.date_range(start=startTime11, end = endTime11)

        
            for oneDate11 in allDates11:
                oneDate11 = oneDate11.date().strftime("%Y-%m-%d") 
                
                oneDayData11 = auth2_client.time_series('activities/distance',user_id="-",base_date=oneDate11,period='1d')

                df11 = pd.DataFrame(oneDayData11['activities-distance'])
                    
                date_list11.append(oneDate11)
                    
                df_list11.append(df11)
                    

            final_df11 = pd.concat(df_list11, axis = 0)
                
            if typ == 102:
                if naam == 202:
                    filename11 = input("please enter the name you want put for FitBit Distance data file: ") 
                elif naam == 201:
                    filename11 = "Fitbit_Ditance"

                if locQuery == 151:
                    file11 = input("please enter location where you want to put the file: ")
                else:
                    file11 = loc    
                final_df11.to_csv(file11+ filename11 + '.csv', index = False)

            elif typ == 101:
                final_df11.to_excel(writer, sheet_name = 'Fitbit_Distance')
                writer.save()
            print(colored("you have successfully retrieved (11) distance data, please keep track of it", 'green', attrs=['reverse', 'blink']) )
            
        except ValueError or KeyError:
            print()
            user1 = int(input(colored("you do not have any recorded value of (11) Distance in your fitbit account or you might have put wrong date, press (99) to exit the program or press (199) to continue:  ", 'red', attrs=['reverse', 'blink'])))
            print()

        except HTTPTooManyRequests:
            print()
            user1 = int(input(colored("you have exceeded the requests limit which is 150 and you are being stopped at number (11) Distance, please try again after an hour. \nplease look over green lines in terminal where it showed which data you have retrieved successfully, \nit will be helpful when you need to start getting data again from where it stopped.  \nplease press (99) to exit the program or press (199) to continue: ", 'red', attrs=['reverse', 'blink'])))
            print()
        except HTTPBadRequest:
            print()
            user1 = int(input(colored("you might not have this (11) Distance data named recorded data in your fitbit records. \nplease press (99) to exit the program or press (199) to continue: ", 'red', attrs=['reverse', 'blink'])))
            print()
        if user1 == 99:
            break

    if user == 12 or user == 0 or (user == 88 and user3 <= user4 and user3 == 12):
        user3 = user3 + 1
        try:
            if user ==12:
                y121 = int(input("please enter the start date year: "))
                m121 = int(input("please enter the start date month: "))
                d121 = int(input("please enter the start day date: "))
                y122 = int(input("please enter the end date year: "))
                m122 = int(input("please enter the end date month: "))
                d122 = int(input("please enter the end day date: "))
            else:
                y121 = y01
                m121 = m01
                d121 = d01
                y122 = y02
                m122 = m02
                d122 = d02


            startTime12 = pd.datetime(year = y121, month = m121, day = d121)
            endTime12 = pd.datetime(year = y122, month = m122, day = d122)



            date_list12 = []
            df_list12 = []
            allDates12 = pd.date_range(start=startTime12, end = endTime12)

        
            for oneDate12 in allDates12:
                oneDate12 = oneDate12.date().strftime("%Y-%m-%d") 
                
                oneDayData12 = auth2_client.time_series('activities/minutesSedentary',user_id="-",base_date=oneDate12,period='1d')

                df12 = pd.DataFrame(oneDayData12['activities-minutesSedentary'])
                    
                date_list12.append(oneDate12)
                    
                df_list12.append(df12)
                    

            final_df12 = pd.concat(df_list12, axis = 0)
                
            if typ == 102:
                if naam == 202:
                    filename12 = input("please enter the name you want put for FitBit minutesSedentary data file: ") 
                elif naam == 201:
                    filename12 = "Fitbit_MinutesSedentary"

                if locQuery == 151:
                    file12 = input("please enter location where you want to put the file: ")
                else:
                    file12 = loc    
                final_df12.to_csv(file12+ filename12 + '.csv', index = False)

            elif typ == 101:
                final_df12.to_excel(writer, sheet_name = 'Fitbit_MinutesSedentary')
                writer.save()
            print(colored("you have successfully retrieved (12) MinutesSedentary data, please keep track of it", 'green', attrs=['reverse', 'blink']) )
            
        except ValueError or KeyError:
            print()
            user1 = int(input(colored("you do not have any recorded value of (12) minutesSedentary in your fitbit account or you might have put wrong date, press (99) to exit the program or press (199) to continue:  ", 'red', attrs=['reverse', 'blink'])))
            print()

        except HTTPTooManyRequests:
            print()
            user1 = int(input(colored("you have exceeded the requests limit which is 150 and you are being stopped at number (12) minutesSedentary, please try again after an hour. \nplease look over green lines in terminal where it showed which data you have retrieved successfully, \nit will be helpful when you need to start getting data again from where it stopped.  \nplease press (99) to exit the program or press (199) to continue: ", 'red', attrs=['reverse', 'blink'])))
            print()
        except HTTPBadRequest:
            print()
            user1 = int(input(colored("you might not have this (12) minutesSedentary data named recorded data in your fitbit records. \nplease press (99) to exit the program or press (199) to continue: ", 'red', attrs=['reverse', 'blink'])))
            print()
        if user1 == 99:
            break
            
    if user == 13 or user == 0 or (user == 88 and user3 <= user4 and user3 == 13):
        user3 = user3 + 1
        try:
            if user ==13:
                y131 = int(input("please enter the start date year: "))
                m131 = int(input("please enter the start date month: "))
                d131 = int(input("please enter the start day date: "))
                y132 = int(input("please enter the end date year: "))
                m132 = int(input("please enter the end date month: "))
                d132 = int(input("please enter the end day date: "))
            else:
                y131 = y01
                m131 = m01
                d131 = d01
                y132 = y02
                m132 = m02
                d132 = d02

            startTime13 = pd.datetime(year = y131, month = m131, day = d131)
            endTime13 = pd.datetime(year = y132, month = m132, day = d132)



            date_list13 = []
            df_list13 = []
            allDates13 = pd.date_range(start=startTime13, end = endTime13)
        
            for oneDate13 in allDates13:
                oneDate13 = oneDate13.date().strftime("%Y-%m-%d") 
                
                oneDayData13 = auth2_client.time_series('activities/minutesLightlyActive',user_id="-",base_date=oneDate13,period='1d')

                df13 = pd.DataFrame(oneDayData13['activities-minutesLightlyActive'])
                    
                date_list13.append(oneDate13)
                    
                df_list13.append(df13)
                    

            final_df13 = pd.concat(df_list13, axis = 0)
                
            if typ == 102:
                if naam == 202:
                    filename13 = input("please enter the name you want put for FitBit minutesLightlyActive data file: ") 
                elif naam == 201:
                    filename13 = "Fitbit_MinutesLightlyActive"

                if locQuery == 151:
                    file13 = input("please enter location where you want to put the file: ")
                else:
                    file13 = loc    
                final_df13.to_csv(file13+ filename13 + '.csv', index = False)

            elif typ == 101:
                final_df13.to_excel(writer, sheet_name = 'Fitbit_MinutesLightlyActive')
                writer.save()
            print(colored("you have successfully retrieved (13) MinutesLightlyActive data, please keep track of it", 'green', attrs=['reverse', 'blink']) )
            
        except ValueError or KeyError:
            print()
            user1 = int(input(colored("you do not have any recorded value of (13) minutesLightlyActive in your fitbit account or you might have put wrong date, press (99) to exit the program or press (199) to continue:  ", 'red', attrs=['reverse', 'blink'])))
            print()

        except HTTPTooManyRequests:
            print()
            user1 = int(input(colored("you have exceeded the requests limit which is 150 and you are being stopped at number (13) minutesLightlyActive, please try again after an hour. \nplease look over green lines in terminal where it showed which data you have retrieved successfully, \nit will be helpful when you need to start getting data again from where it stopped.  \nplease press (99) to exit the program or press (199) to continue: ", 'red', attrs=['reverse', 'blink'])))
            print()
        except HTTPBadRequest:
            print()
            user1 = int(input(colored("you might not have this (13) minutesLightlyActive data named recorded data in your fitbit records. \nplease press (99) to exit the program or press (199) to continue: ", 'red', attrs=['reverse', 'blink'])))
            print()
        if user1 == 99:
            break
    
    if user == 14 or user == 0 or (user == 88 and user3 <= user4 and user3 == 14):
        user3 = user3 + 1
        try:
            if user ==14:
                y141 = int(input("please enter the start date year: "))
                m141 = int(input("please enter the start date month: "))
                d141 = int(input("please enter the start day date: "))
                y142 = int(input("please enter the end date year: "))
                m142 = int(input("please enter the end date month: "))
                d142 = int(input("please enter the end day date: "))
            else:
                y141 = y01
                m141 = m01
                d141 = d01
                y142 = y02
                m142 = m02
                d142 = d02

            startTime14 = pd.datetime(year = y141, month = m141, day = d141)
            endTime14 = pd.datetime(year = y142, month = m142, day = d142)



            date_list14 = []
            df_list14 = []
            allDates14 = pd.date_range(start=startTime14, end = endTime14)

        
            for oneDate14 in allDates14:
                oneDate14 = oneDate14.date().strftime("%Y-%m-%d") 
                
                oneDayData14 = auth2_client.time_series('activities/minutesFairlyActive',user_id="-",base_date=oneDate14,period='1d')

                df14 = pd.DataFrame(oneDayData14['activities-minutesFairlyActive'])
                    
                date_list14.append(oneDate14)
                    
                df_list14.append(df14)
                    

            final_df14 = pd.concat(df_list14, axis = 0)
                
            if typ == 102:
                if naam == 202:
                    filename14 = input("please enter the name you want put for FitBit minutesFairlyActive data file: ") 
                elif naam == 201:
                    filename14 = "Fitbit_MinutesFairlyActive"

                if locQuery == 151:
                    file14 = input("please enter location where you want to put the file: ")
                else:
                    file14 = loc    
                final_df14.to_csv(file14+ filename14 + '.csv', index = False)

            elif typ == 101:
                final_df14.to_excel(writer, sheet_name = 'Fitbit_MinutesFairlyActive')
                writer.save()
            print(colored("you have successfully retrieved (14) MinutesFairlyActive data, please keep track of it", 'green', attrs=['reverse', 'blink']) )
            
        except ValueError or KeyError:
            print()
            user1 = int(input(colored("you do not have any recorded value of (14) minutesFairlyActive in your fitbit account or you might have put wrong date, press (99) to exit the program or press (199) to continue:  ", 'red', attrs=['reverse', 'blink'])))
            print()

        except HTTPTooManyRequests:
            print()
            user1 = int(input(colored("you have exceeded the requests limit which is 150 and you are being stopped at number (14) minutesFairlyActive, please try again after an hour. \nplease look over green lines in terminal where it showed which data you have retrieved successfully, \nit will be helpful when you need to start getting data again from where it stopped.  \nplease press (99) to exit the program or press (199) to continue: ", 'red', attrs=['reverse', 'blink'])))
            print()
        except HTTPBadRequest:
            print()
            user1 = int(input(colored("you might not have this (14) minutesFairlyActive data named recorded data in your fitbit records. \nplease press (99) to exit the program or press (199) to continue: ", 'red', attrs=['reverse', 'blink'])))
            print()
        if user1 == 99:
            break
    
    if user == 15 or user == 0 or (user == 88 and user3 <= user4 and user3 == 15):
        user3 = user3 + 1
        try:
            if user ==15:
                y151 = int(input("please enter the start date year: "))
                m151 = int(input("please enter the start date month: "))
                d151 = int(input("please enter the start day date: "))
                y152 = int(input("please enter the end date year: "))
                m152 = int(input("please enter the end date month: "))
                d152 = int(input("please enter the end day date: "))
            else:
                y151 = y01
                m151 = m01
                d151 = d01
                y152 = y02
                m152 = m02
                d152 = d02

            startTime15 = pd.datetime(year = y151, month = m151, day = d151)
            endTime15 = pd.datetime(year = y152, month = m152, day = d152)



            date_list15 = []
            df_list15 = []
            allDates15 = pd.date_range(start=startTime15, end = endTime15)

       
                
            for oneDate15 in allDates15:
                oneDate15 = oneDate15.date().strftime("%Y-%m-%d") 
                
                oneDayData15 = auth2_client.time_series('activities/minutesVeryActive',user_id="-",base_date=oneDate15,period='1d')

                df15 = pd.DataFrame(oneDayData15['activities-minutesVeryActive'])
                    
                date_list15.append(oneDate15)
                    
                df_list15.append(df15)
                    

            final_df15 = pd.concat(df_list15, axis = 0)
                
            if typ == 102:
                if naam == 202:
                    filename15 = input("please enter the name you want put for FitBit minutesVeryActive data file: ") 
                elif naam == 201:
                    filename15 = "Fitbit_MinutesVeryActive"

                if locQuery == 151:
                    file15 = input("please enter location where you want to put the file: ")
                else:
                    file15 = loc    
                final_df15.to_csv(file15+ filename15 + '.csv', index = False)

            elif typ == 101:
                final_df15.to_excel(writer, sheet_name = 'Fitbit_MinutesVeryActive')
                writer.save()
            print(colored("you have successfully retrieved (15) MinutesVeryActive data, please keep track of it", 'green', attrs=['reverse', 'blink']) )
            
        except ValueError or KeyError:
            print()
            user1 = int(input(colored("you do not have any recorded value of (15) minutesVeryActive in your fitbit account or you might have put wrong date, press (99) to exit the program or press (199) to continue:  ", 'red', attrs=['reverse', 'blink'])))
            print()

        except HTTPTooManyRequests:
            print()
            user1 = int(input(colored("you have exceeded the requests limit which is 150 and you are being stopped at number (15) minutesVeryActive, please try again after an hour. \nplease look over green lines in terminal where it showed which data you have retrieved successfully, \nit will be helpful when you need to start getting data again from where it stopped.  \nplease press (99) to exit the program or press (199) to continue: ", 'red', attrs=['reverse', 'blink'])))
            print()
        except HTTPBadRequest:
            print()
            user1 = int(input(colored("you might not have this (15) minutesVeryActive data named recorded data in your fitbit records. \nplease press (99) to exit the program or press (199) to continue: ", 'red', attrs=['reverse', 'blink'])))
            print()
        if user1 == 99:
            break

    if user == 16 or user == 0 or (user == 88 and user3 <= user4 and user3 == 16):
        user3 =user3 + 1
        try:
            if user ==16:
                y161 = int(input("please enter the start date year: "))
                m161 = int(input("please enter the start date month: "))
                d161 = int(input("please enter the start day date: "))
                y162 = int(input("please enter the end date year: "))
                m162 = int(input("please enter the end date month: "))
                d162 = int(input("please enter the end day date: "))
            else:
                y161 = y01
                m161 = m01
                d161 = d01
                y162 = y02
                m162 = m02
                d162 = d02

            startTime16 = pd.datetime(year = y161, month = m161, day = d161)
            endTime16 = pd.datetime(year = y162, month = m162, day = d162)



            date_list16 = []
            df_list16 = []
            allDates16 = pd.date_range(start=startTime16, end = endTime16)
        
            for oneDate16 in allDates16:
                oneDate16 = oneDate16.date().strftime("%Y-%m-%d") 
                
                oneDayData16 = auth2_client.time_series('activities/activityCalories',user_id="-",base_date=oneDate16,period='1d')

                df16 = pd.DataFrame(oneDayData16['activities-activityCalories'])
                    
                date_list16.append(oneDate16)
                    
                df_list16.append(df16)
                    

            final_df16 = pd.concat(df_list16, axis = 0)
                
            if typ == 102:
                if naam == 202:
                    filename16 = input("please enter the name you want put for FitBit activityCalories data file: ") 
                elif naam == 201:
                    filename16 = "Fitbit_ActivityCalories"

                if locQuery == 151:
                    file16 = input("please enter location where you want to put the file: ")
                else:
                    file16 = loc    
                final_df16.to_csv(file16+ filename16 + '.csv', index = False)

            elif typ == 101:
                final_df16.to_excel(writer, sheet_name = 'Fitbit_ActivityCalories')
                writer.save()
            print(colored("you have successfully retrieved (16) ActivityCalories data, please keep track of it", 'green', attrs=['reverse', 'blink']) )
            
        except ValueError or KeyError:
            print()
            user1 = int(input(colored("you do not have any recorded value of (16) activityCalories in your fitbit account or you might have put wrong date, press (99) to exit the program or press (199) to continue:  ", 'red', attrs=['reverse', 'blink'])))
            print()

        except HTTPTooManyRequests:
            print()
            user1 = int(input(colored("you have exceeded the requests limit which is 150 and you are being stopped at number (16) activityCalories, please try again after an hour. \nplease look over green lines in terminal where it showed which data you have retrieved successfully, \nit will be helpful when you need to start getting data again from where it stopped.  \nplease press (99) to exit the program or press (199) to continue: ", 'red', attrs=['reverse', 'blink'])))
            print()
        except HTTPBadRequest:
            print()
            user1 = int(input(colored("you might not have this (16) activityCalories data named recorded data in your fitbit records. \nplease press (99) to exit the program or press (199) to continue: ", 'red', attrs=['reverse', 'blink'])))
            print()
        if user1 == 99:
            break
   
    if user == 17 or user == 0 or (user == 88 and user3 <= user4 and user3 == 17):
        user3 = user3 + 1
        try:
            if user ==17:
                y171 = int(input("please enter the start date year: "))
                m171 = int(input("please enter the start date month: "))
                d171 = int(input("please enter the start day date: "))
                y172 = int(input("please enter the end date year: "))
                m172 = int(input("please enter the end date month: "))
                d172 = int(input("please enter the end day date: "))
            else:
                y171 = y01
                m171 = m01
                d171 = d01
                y172 = y02
                m172 = m02
                d172 = d02

            startTime17 = pd.datetime(year = y171, month = m171, day = d171)
            endTime17 = pd.datetime(year = y172, month = m172, day = d172)



            date_list17 = []
            df_list17 = []
            allDates17 = pd.date_range(start=startTime17, end = endTime17)

        
            for oneDate17 in allDates17:
                oneDate17 = oneDate17.date().strftime("%Y-%m-%d") 
    
                oneDayData17 = auth2_client.time_series('body/bmi',user_id="-",base_date=oneDate17,period='1d')

                df17 = pd.DataFrame(oneDayData17['body-bmi'])
                    
                date_list17.append(oneDate17)
                    
                df_list17.append(df17)
                    

            final_df17 = pd.concat(df_list17, axis = 0)

            if typ == 102:
                if naam == 202:
                    filename17 = input("please enter the name you want put for FitBit Body BMI data file: ") 
                elif naam == 201:
                    filename17 = "Fitbit_Body_BMI"

                if locQuery == 151:
                    file17 = input("please enter location where you want to put the file: ")
                else:
                    file17 = loc    
                final_df17.to_csv(file17+ filename17 + '.csv', index = False)

            elif typ == 101:
                final_df17.to_excel(writer, sheet_name = 'Fitbit_Body_BMI')
                writer.save()
            print(colored("you have successfully retrieved (17) body BMI data, please keep track of it", 'green', attrs=['reverse', 'blink']) )
            
        except ValueError or KeyError:
            print()
            user1 = int(input(colored("you do not have any recorded value of (17) BMI in your fitbit account or you might have put wrong date, press (99) to exit the program or press (199) to continue:  ", 'red', attrs=['reverse', 'blink'])))
            print()

        except HTTPTooManyRequests:
            print()
            user1 = int(input(colored("you have exceeded the requests limit which is 150 and you are being stopped at number (17) BMI, please try again after an hour. \nplease look over green lines in terminal where it showed which data you have retrieved successfully, \nit will be helpful when you need to start getting data again from where it stopped.  \nplease press (99) to exit the program or press (199) to continue: ", 'red', attrs=['reverse', 'blink'])))
            print()
        except HTTPBadRequest:
            print()
            user1 = int(input(colored("you might not have this (17) BMI data named recorded data in your fitbit records. \nplease press (99) to exit the program or press (199) to continue: ", 'red', attrs=['reverse', 'blink'])))
            print()
        if user1 == 99:
            break

    if user == 18 or user == 0 or (user == 88 and user3 <= user4 and user3 == 18):
        user3 = user3 + 1
        try:
            if user ==18:
                y181 = int(input("please enter the start date year: "))
                m181 = int(input("please enter the start date month: "))
                d181 = int(input("please enter the start day date: "))
                y182 = int(input("please enter the end date year: "))
                m182 = int(input("please enter the end date month: "))
                d182 = int(input("please enter the end day date: "))
            else:
                y181 = y01
                m181 = m01
                d181 = d01
                y182 = y02
                m182 = m02
                d182 = d02

            startTime18 = pd.datetime(year = y181, month = m181, day = d181)
            endTime18 = pd.datetime(year = y182, month = m182, day = d182)



            date_list18 = []
            df_list18 = []
            allDates18 = pd.date_range(start=startTime18, end = endTime18)

        
            for oneDate18 in allDates18:
                oneDate18 = oneDate18.date().strftime("%Y-%m-%d") 
    
                oneDayData18 = auth2_client.time_series('foods/log/caloriesIn',user_id="-",base_date=oneDate18,period='1d')

                df18 = pd.DataFrame(oneDayData18['foods-log-caloriesIn'])
                    
                date_list18.append(oneDate18)
                    
                df_list18.append(df18)
                    

            final_df18 = pd.concat(df_list18, axis = 0)

            if typ == 102:
                if naam == 202:
                    filename18 = input("please enter the name you want put for FitBit Foods Calories Intake data file: ") 
                elif naam == 201:
                    filename18 = "Fitbit_Foods_Calories_Intake"

                if locQuery == 151:
                    file18 = input("please enter location where you want to put the file: ")
                else:
                    file18 = loc    
                final_df18.to_csv(file18+ filename18 + '.csv', index = False)

            elif typ == 101:
                final_df18.to_excel(writer, sheet_name = 'Fitbit_Foods_Calories_Intake')
                writer.save()
            print(colored("you have successfully retrieved (18) food calories intake data, please keep track of it", 'green', attrs=['reverse', 'blink']) )
            
        except ValueError or KeyError:
            print()
            user1 = int(input(colored("you do not have any recorded value of (18) Food in your fitbit account or you might have put wrong date, press (99) to exit the program or press (199) to continue:  ", 'red', attrs=['reverse', 'blink'])))
            print()

        except HTTPTooManyRequests:
            print()
            user1 = int(input(colored("you have exceeded the requests limit which is 150 and you are being stopped at number (18) Food, please try again after an hour. \nplease look over green lines in terminal where it showed which data you have retrieved successfully, \nit will be helpful when you need to start getting data again from where it stopped.  \nplease press (99) to exit the program or press (199) to continue: ", 'red', attrs=['reverse', 'blink'])))
            print()
        except HTTPBadRequest:
            print()
            user1 = int(input(colored("you might not have this (18) food data named recorded data in your fitbit records. \nplease press (99) to exit the program or press (199) to continue: ", 'red', attrs=['reverse', 'blink'])))
            print()
        if user1 == 99:
            break

    if user == 19 or user == 0 or (user == 88 and user3 <= user4 and user3 == 19):
        user3 = user3 + 1
        try:
            if user ==19:
                y191 = int(input("please enter the start date year: "))
                m191 = int(input("please enter the start date month: "))
                d191 = int(input("please enter the start day date: "))
                y192 = int(input("please enter the end date year: "))
                m192 = int(input("please enter the end date month: "))
                d192 = int(input("please enter the end day date: "))
            else:
                y191 = y01
                m191 = m01
                d191 = d01
                y192 = y02
                m192 = m02
                d192 = d02

            startTime19 = pd.datetime(year = y191, month = m191, day = d191)
            endTime19 = pd.datetime(year = y192, month = m192, day = d192)



            date_list19 = []
            df_list19 = []
            allDates19 = pd.date_range(start=startTime19, end = endTime19)

       
            for oneDate19 in allDates19:
                oneDate19 = oneDate19.date().strftime("%Y-%m-%d") 
    
                oneDayData19 = auth2_client.time_series('foods/log/water',user_id="-",base_date=oneDate19,period='1d')

                df19 = pd.DataFrame(oneDayData19['foods-log-water'])
                    
                date_list19.append(oneDate19)
                    
                df_list19.append(df19)
                    

            final_df19 = pd.concat(df_list19, axis = 0)

            if typ == 102:
                if naam == 202:
                    filename19 = input("please enter the name you want put for FitBit Water Intake data file: ") 
                elif naam == 201:
                    filename19 = "Fitbit_Water_Intake"

                if locQuery == 151:
                    file19 = input("please enter location where you want to put the file: ")
                else:
                    file19 = loc    
                final_df19.to_csv(file19+ filename19 + '.csv', index = False)

            elif typ == 101:
                final_df19.to_excel(writer, sheet_name = 'Fitbit_Water_Intake')
                writer.save()
            print(colored("you have successfully retrieved (19) water intake data, please keep track of it", 'green', attrs=['reverse', 'blink']) )
            
        except ValueError or KeyError:
            print()
            user1 = int(input(colored("you do not have any recorded value of (19) Water in your fitbit account or you might have put wrong date, press (99) to exit the program or press (199) to continue:  ", 'red', attrs=['reverse', 'blink'])))
            print()

        except HTTPTooManyRequests:
            print()
            user1 = int(input(colored("you have exceeded the requests limit which is 150  and you are being stopped at number (19) Water, please try again after an hour. \nplease look over green lines in terminal where it showed which data you have retrieved successfully, \nit will be helpful when you need to start getting data again from where it stopped.  \nplease press (99) to exit the program or press (199) to continue: ", 'red', attrs=['reverse', 'blink'])))
            print()
        except HTTPBadRequest:
            print()
            user1 = int(input(colored("you might not have this (19) water data named recorded data in your fitbit records. \nplease press (99) to exit the program or press (199) to continue: ", 'red', attrs=['reverse', 'blink'])))
            print()
        if user1 == 99:
            break

    if user == 20 or user == 0 or (user == 88 and user3 <= user4 and user3 == 20):
        user3 =user3 + 1
        try:
            if user == 20:
                y201 = int(input("please enter the start date year: "))
                m201 = int(input("please enter the start date month: "))
                d201 = int(input("please enter the start day date: "))
                y202 = int(input("please enter the end date year: "))
                m202 = int(input("please enter the end date month: "))
                d202 = int(input("please enter the end day date: "))
            else:
                y201 = y01
                m201 = m01
                d201 = d01
                y202 = y02
                m202 = m02
                d202 = d02

            startTime20 = pd.datetime(year = y201, month = m201, day = d201)
            endTime20 = pd.datetime(year = y202, month = m202, day = d202)



            date_list20 = []
            df_list20 = []
            allDates20 = pd.date_range(start=startTime20, end = endTime20)
        
            for oneDate20 in allDates20:
                oneDate20 = oneDate20.date().strftime("%Y-%m-%d") 
                
                oneDayData20 = auth2_client.time_series('activities/floors',user_id="-",base_date=oneDate20,period='1d')

                df20 = pd.DataFrame(oneDayData20['activities-floors'])
                    
                date_list20.append(oneDate20)
                    
                df_list20.append(df20)
                    

            final_df20 = pd.concat(df_list20, axis = 0)
                
            if typ == 102:
                if naam == 202:
                    filename20 = input("please enter the name you want put for FitBit Floors data file: ") 
                elif naam == 201:
                    filename20 = "Fitbit_Floors"

                if locQuery == 151:
                    file20 = input("please enter location where you want to put the file: ")
                else:
                    file20 = loc    
                final_df20.to_csv(file20+ filename20 + '.csv', index = False)

            elif typ == 101:
                final_df20.to_excel(writer, sheet_name = 'Fitbit_Floors')
                writer.save()
            print(colored("you have successfully retrieved (20) Floors data, please keep track of it", 'green', attrs=['reverse', 'blink']) )
            
        except ValueError or KeyError:
            print()
            user1 = int(input(colored("you do not have any recorded value of (20) Floors in your fitbit account or you might have put wrong date, press (99) to exit the program or press (199) to continue:  ", 'red', attrs=['reverse', 'blink'])))
            print()

        except HTTPTooManyRequests:
            print()
            user1 = int(input(colored("you have exceeded the requests limit which is 150 and you are being stopped at number (20) Floors, please try again after an hour. \nplease look over green lines in terminal where it showed which data you have retrieved successfully, \nit will be helpful when you need to start getting data again from where it stopped.  \nplease press (99) to exit the program or press (199) to continue: ", 'red', attrs=['reverse', 'blink'])))
            print()
        except HTTPBadRequest:
            print()
            user1 = int(input(colored("you might not have this (20) Floors data named recorded data in your fitbit records. \nplease press (99) to exit the program or press (199) to continue: ", 'red', attrs=['reverse', 'blink'])))
            print()
        if user1 == 99:
            break

    if user == 21 or user == 0 or (user == 88 and user3 <= user4 and user3 == 21):
        user3 =user3 + 1
        try:
            if user == 21:
                y211 = int(input("please enter the start date year: "))
                m211 = int(input("please enter the start date month: "))
                d211 = int(input("please enter the start day date: "))
                y212 = int(input("please enter the end date year: "))
                m212 = int(input("please enter the end date month: "))
                d212 = int(input("please enter the end day date: "))
            else:
                y211 = y01
                m211 = m01
                d211 = d01
                y212 = y02
                m212 = m02
                d212 = d02

            startTime21 = pd.datetime(year = y211, month = m211, day = d211)
            endTime21 = pd.datetime(year = y212, month = m212, day = d212)



            date_list21 = []
            df_list21 = []
            allDates21 = pd.date_range(start=startTime21, end = endTime21)
        
            for oneDate21 in allDates21:
                oneDate21 = oneDate21.date().strftime("%Y-%m-%d") 
                
                oneDayData21 = auth2_client.time_series('activities/elevation',user_id="-",base_date=oneDate21,period='1d')

                df21 = pd.DataFrame(oneDayData21['activities-elevation'])
                    
                date_list21.append(oneDate21)
                    
                df_list21.append(df21)
                    

            final_df21 = pd.concat(df_list21, axis = 0)
                
            if typ == 102:
                if naam == 202:
                    filename21 = input("please enter the name you want put for FitBit Elevation data file: ") 
                elif naam == 201:
                    filename21 = "Fitbit_Elevation"

                if locQuery == 151:
                    file21 = input("please enter location where you want to put the file: ")
                else:
                    file21 = loc    
                final_df21.to_csv(file21+ filename21 + '.csv', index = False)

            elif typ == 101:
                final_df21.to_excel(writer, sheet_name = 'Fitbit_Elevation')
                writer.save()
            print(colored("you have successfully retrieved (21) Elevation data, please keep track of it", 'green', attrs=['reverse', 'blink']) )
            
        except ValueError or KeyError:
            print()
            user1 = int(input(colored("you do not have any recorded value of (21) Elevation in your fitbit account or you might have put wrong date, press (99) to exit the program or press (199) to continue:  ", 'red', attrs=['reverse', 'blink'])))
            print()

        except HTTPTooManyRequests:
            print()
            user1 = int(input(colored("you have exceeded the requests limit which is 150 and you are being stopped at number (21) Elevation, please try again after an hour. \nplease look over green lines in terminal where it showed which data you have retrieved successfully, \nit will be helpful when you need to start getting data again from where it stopped.  \nplease press (99) to exit the program or press (199) to continue: ", 'red', attrs=['reverse', 'blink'])))
            print()
        except HTTPBadRequest:
            print()
            user1 = int(input(colored("you might not have this (21) Elevation data named recorded data in your fitbit records. \nplease press (99) to exit the program or press (199) to continue: ", 'red', attrs=['reverse', 'blink'])))
            print()
        if user1 == 99:
            break

    if user == 22 or user == 0 or (user == 88 and user3 <= user4 and user3 == 22):
        user3 = user3 + 1
        try:
            if user ==22:
                y221 = int(input("please enter the start date year: "))
                m221 = int(input("please enter the start date month: "))
                d221 = int(input("please enter the start day date: "))
                y222 = int(input("please enter the end date year: "))
                m222 = int(input("please enter the end date month: "))
                d222 = int(input("please enter the end day date: "))
            else:
                y221 = y01
                m221 = m01
                d221 = d01
                y222 = y02
                m222 = m02
                d222 = d02

            startTime22 = pd.datetime(year = y221, month = m221, day = d221)
            endTime22 = pd.datetime(year = y222, month = m222, day = d222)



            date_list22 = []
            df_list22 = []
            allDates22 = pd.date_range(start=startTime22, end = endTime22)

        
            #to collect data from day to day
            for oneDate22 in allDates22:
                
                oneDate22 = oneDate22.date().strftime("%Y-%m-%d")
                
                oneDayData22 = auth2_client.intraday_time_series('activities/floors',base_date=oneDate22, detail_level='1min')

                df22 = pd.DataFrame(oneDayData22['activities-floors-intraday']['dataset'])
                
                date_list22.append(oneDate22)

                df_list22.append(df22)

            final_df_list22 = []

            # it will get all the interative data  
            for date22, df22 in zip(date_list22, df_list22):
                if len(df22) == 0:
                    continue
                df22.loc[:,'date'] = pd.to_datetime(date22)
                final_df_list22.append(df22)

            # it will conactinate the data
            final_df22 = pd.concat(final_df_list22,axis = 0)
            final_df22.tail() 

            if typ == 102:
                if naam == 202:
                    filename22 = input("please enter the name you want put for FitBit Floors Intraday data file: ") 
                elif naam == 201:
                    filename22 = "Fitbit_Floors_Intraday"

                if locQuery == 151:
                    file22 = input("please enter location where you want to put the file: ")
                else:
                    file22 = loc    
                final_df22.to_csv(file22+ filename22 + '.csv', index = False)

            elif typ == 101:
                final_df22.to_excel(writer, sheet_name = 'Fitbit_Floors_IntraDay')
                writer.save()
            print(colored("you have successfully retrieved (22) floors intraday data, please keep track of it", 'green', attrs=['reverse', 'blink']) )
            
        except ValueError or KeyError:
            print()
            user1 = int(input(colored("you do not have any recorded value of (22) Floors Intrday data in your fitbit account or you might have put wrong date, press (99) to exit the program or press (199) to continue:  ", 'red', attrs=['reverse', 'blink'])))
            print()

        except HTTPTooManyRequests:
            print()
            user1 = int(input(colored("you have exceeded the requests limit which is 150 and you are being stopped at number (22) Floors Intraday, please try again after an hour. \nplease look over green lines in terminal where it showed which data you have retrieved successfully, \nit will be helpful when you need to start getting data again from where it stopped.  \nplease press (99) to exit the program or press (199) to continue: ", 'red', attrs=['reverse', 'blink'])))
            print()
        except HTTPBadRequest:
            print()
            user1 = int(input(colored("you might not have this (22) Floors Intraday data named recorded data in your fitbit records. \nplease press (99) to exit the program or press (199) to continue: ", 'red', attrs=['reverse', 'blink'])))
            print()
        if user1 == 99:
            break

    if user == 23 or user == 0 or (user == 88 and user3 <= user4 and user3 == 23):
        try:
            if user ==23:
                y231 = int(input("please enter the start date year: "))
                m231 = int(input("please enter the start date month: "))
                d231 = int(input("please enter the start day date: "))
                y232 = int(input("please enter the end date year: "))
                m232 = int(input("please enter the end date month: "))
                d232 = int(input("please enter the end day date: "))
            else:
                y231 = y01
                m231 = m01
                d231 = d01
                y232 = y02
                m232 = m02
                d232 = d02

            startTime23 = pd.datetime(year = y231, month = m231, day = d231)
            endTime23 = pd.datetime(year = y232, month = m232, day = d232)



            date_list23 = []
            df_list23 = []
            allDates23 = pd.date_range(start=startTime23, end = endTime23)

        
            #to collect data from day to day
            for oneDate23 in allDates23:
                
                oneDate23 = oneDate23.date().strftime("%Y-%m-%d")
                
                oneDayData23 = auth2_client.intraday_time_series('activities/elevation',base_date=oneDate23, detail_level='1min')

                df23 = pd.DataFrame(oneDayData23['activities-elevation-intraday']['dataset'])
                
                date_list23.append(oneDate23)

                df_list23.append(df23)

            final_df_list23 = []

            # it will get all the interative data  
            for date23, df23 in zip(date_list23, df_list23):
                if len(df23) == 0:
                    continue
                df23.loc[:,'date'] = pd.to_datetime(date23)
                final_df_list23.append(df23)

            # it will conactinate the data
            final_df23 = pd.concat(final_df_list23,axis = 0)
            final_df23.tail() 

            if typ == 102:
                if naam == 202:
                    filename23 = input("please enter the name you want put for FitBit Elevation Intraday data file: ") 
                elif naam == 201:
                    filename23 = "Fitbit_Elevation_Intraday"

                if locQuery == 151:
                    file23 = input("please enter location where you want to put the file: ")
                else:
                    file23 = loc    
                final_df23.to_csv(file23+ filename23 + '.csv', index = False)

            elif typ == 101:
                final_df23.to_excel(writer, sheet_name = 'Fitbit_Elevation_IntraDay')
                writer.save()
            print(colored("you have successfully retrieved (23) Elevation intraday data, please keep track of it", 'green', attrs=['reverse', 'blink']) )
            
        except ValueError or KeyError:
            print()
            user1 = int(input(colored("you do not have any recorded value of (23) Elevation intraday data in your fitbit account or you might have put wrong date, press (99) to exit the program or press (199) to continue:  ", 'red', attrs=['reverse', 'blink'])))
            print()

        except HTTPTooManyRequests:
            print()
            user1 = int(input(colored("you have exceeded the requests limit which is 150 and you are being stopped at number (23) Elevation IntraDay, please try again after an hour. \nplease look over green lines in terminal where it showed which data you have retrieved successfully, \nit will be helpful when you need to start getting data again from where it stopped.  \nplease press (99) to exit the program or press (199) to continue: ", 'red', attrs=['reverse', 'blink'])))
            print()
        except HTTPBadRequest:
            print()
            user1 = int(input(colored("you might not have this (23) Elevation IntraDay data named recorded data in your fitbit records. \nplease press (99) to exit the program or press (199) to continue: ", 'red', attrs=['reverse', 'blink'])))
            print()
        if user1 == 99:
            break

    if user == 99 or user1 == 99:
        if typ == 101:
            try:
                writer.close()
                user2 = int(input("please press (99) again to exit the program or press (199) to continue: "))
                if user2 == 99:
                    break
            except IndexError:
                print()
                user2 = int(input(colored("At least one sheet must be available, please try to get the data, press (99) again to exit the program or press (199) to continue ", 'red', attrs=['reverse', 'blink'])))
                print()
                if user2 == 99:
                    break        
        elif typ == 102:
            break
    
    
