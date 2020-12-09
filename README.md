# Data-Extraction-from-Fitbit


--Here is the information on how to use this package provided, Please read it very carefully.

STOP 1: Intsalling python: 
--Fistly, We will need to install python in our machine if it is not installed already.
--Go to https://www.python.org/downloads/ 
--you can manually download that too by just typing in google search engine and it will show you this website. 
--Then download an appropriate version of python according to your machine.
--after installing python move to next stop.

STOP 2: Using python IDEs for better implementations. 
--Now that we have downloaded python, we will move ahead to download IDEs for better implementations. 
--We have many IDEs to use python, We have Microsoft Visul Studio, PyCharm, IDLE, Spyder, Eclipse, DrPythom, and many more.
--We can download any of those, I particularly used Microsoft Visual Studio because I already have it installed.
--Now, you can download any of those from the list.
--After downloading and installing it, you are now able to open and use Python files we have attached in this package.

STOP 3: Opening and Using attached Python files to implenment:
--We have some python files in our package.
--Please put these two files together in the same directory if you are copying and pasting somewhere: 'extractionFromFitbitApi.py' and 'gather_keys_oauth2.py' 
--Open both of these files in IDE.

STOP 4: Intalling necessary packages from python library:
--Open terminal if ubuntu or command prompt if windows, install fitbit, fitbit.api, pandas, datetime, matplotlib, cherrypy, datetime, numpy, sys, termcolor,
  os, threading, traceback, webbrowser, and base64 packages.
--install those by typing  ( pip install 'packages names') in trminal or command prompt. 
--if you get a moduleNotFound error, it means you are missing that package, you can download that package by using the same procedure.

STOP 5: Setting up fitbit app to get data:
--Go to https://dev.fitbit.com/
--then Log in using your fitbit account credentials
--then go to Manage >> Register An App >> 
--check the image I have attached in the folder called 'instruction for registering app' image, it has some necessary information
--use http://127.0.0.1:8080/ as collback url. 
--OAuth 2.0 Application Type must be personal
--once everything is done, submit/save it
--now you will see something like in the image I have attached, called 'saved app'.
--once registration is done, open any python IDE to open code files.

STOP 6: Running main file:
--once everything is done, run extractionFromFitbitApi.py
--script also has some instruction on how to use that if having a little confusion.
--instructions are provided when using the script.
--CLIENT ID and CLIENT SECRET are necessary, so we will need that infomration when using the script.

STOP 7: Getting results:
--When running the script, enter CLIENT ID and CLIENT SECRET.
--It will direct you to a default webrowser, please log in to your fitbit account and allow all the data to be safe while using the script.
--when done, a message will pop up showing you can close the window.
--from there you can move back to the script and it will ask you to choose either .csv file type or .xlsx file which is regular excel file.
--you can move forward with the information provided in the script from there. 
--you can choose location and file names for every file type, please put a slash after puting location if there is none and you do not need any extensions
  when naming files. 
--We also have options to choose automated file names, or you can write manually for each when using .csv file type option; 
  for .xlsx, we have option to choose file name, it will provide different sheets in one file, so sheets names will be automated. 
--you can get 23 types of data, which will include Some intraday data, and normal data. 
--you can only get data if you have that in your fitbit account, if not then, you will recieve messages showing the reason for not getting that data.
--you must exit the program as instructed in the script.
--The fitbit app has request limit of 150, which means, if we try to get a variety of data for a larger time period, then it will stop you at some point 
  and will tell you to wait for an hour to retrieve other data. In this case, you will need to wait for an hour, but you can keep track of the data
  you have retrieved by looking over the outputs that shows which data you have successfully retrieved and which one you got errors in.
--I color coded some information in script output: red means imprtant and errors, greed means success.
--Again, remeber to exit the script to retrieve data files correctly. And please try to put correct information to avoid unexpected errors.
--If getting other errors, be sure to contact as soon as possible.  
--that is all.


Statistical analysis:
--we gathered Fitbit data first.
Single stats:
--plotting data, and performed some basic statistical computations using Python in Google Colab.

Paired stats:
--We implemented methods for calculating different types of paired statistics
--Through this process, we first performed some data preprocessing
--We then found the Pearson correlation coefficient
--Finally, we performed Principal Component Analysis (PCA), a process which consists of multiple steps including singular value decomposition (SVD)

Prediction:
--we generated a machine learning algorithm that is capable of making predictions based upon input data
--In the process, we carried out all of the required steps involved in creating a successful prediction model
--After the model has been created, we trained it using our dataset
--Finally, we graphed our results and tested out our predictions



 
