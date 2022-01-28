import sqlite3
import requests
from geopy.geocoders import Nominatim
import sys
import json
import typer
conn = sqlite3.connect("database.db")
conn.execute("""
CREATE TABLE IF NOT EXISTS ADMIN(
USERNAME TEXT NOT NULL, 
PASSWORD TEXT NOT NULL)
""")
conn.close()
app = typer.Typer()
def wronginput():
    print("-----------------------------")
    print("     Program Terminated")
    print("-----------------------------")
    return sys.exit()
def latlong():
        print("Enter Latitude and Longitude")
        latitude = str(input('Please enter the latitude: '))
        longitude = str(input('Please enter the longitude: '))
        api_key = str(input("Please enter api key: "))
        return ("https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&exclude=hourly,minutely&appid={}".format(latitude,longitude,api_key))
def cityname():
        print("Please enter City Name:")
        import requests
        import urllib.parse
        address = str(input("Enter city: "))
        address = address.capitalize()
        try:
            r = ('https://nominatim.openstreetmap.org/search/' + str(urllib.parse.quote(address)) +'?format=json')
            response = requests.get(r).json()
            #print("city name",response)
            latitude = response[0]["lat"]
            longitude = response[0]["lon"]
        except:
            print("****************************************")
            print("city name must be wrong")
            print("****************************************")
            print("Enter 1 to try again else enter any key to exit\n")
            try:
                if(int(input()) == 1):
                    getforecast()
            except:
                print("\nProgram Terminated")
                sys.exit()
        #print(latitude,longitude)
        api_key = str(input("Please enter api key: "))
        return ("https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&exclude=hourly,minutely&appid={}".format(latitude,longitude,api_key))

def urladdress():
        choose_option = {'1':latlong, '2': cityname}
        print("Press 1 to get forecast by latitude and longitude \nPress 2 to get forecast by cityname")
        try:
            key = input("please choose the value: ")
            base = choose_option[key]()
            return base
        except KeyError:
            print("Wrong input!!! Try again\n")
            return urladdress()
def getdata(url):
        m = requests.get(url)
        n = m.text
        #print("the value of n", n)
        load = json.loads(n)
        try: 
            load['cod']
            print("Wrong inputs given please try again")
            print("Press 'CTRL+C' to exit application at any time ")
            getforecast()
        except KeyError:
            print("Data Retrived Sucessfully")
            return load
def convert(timestamp):
        import datetime
        value = datetime.datetime.fromtimestamp(timestamp)
        return str(value)          
def getforecast():
        data = getdata(urladdress())
        print('\n')
        print("Forecast is available for 7 days from current date")
        print('\n')
        print("Please choose date Carefully in 'YYYY-MM-DD' format")
        print("\n")
        date = str(input())
        count=0
        for i in data['daily']:
            qw  = list(map(str,convert(timestamp = i['dt']).split()))
            if(str(qw[0]) == date):
                count+=1
                print("-------------------------------------------------------------")
                print("             Date: ",qw[0])
                print("             Humidity: ", i['humidity'])
                print("             Pressure: ", i['pressure'])
                print('             temp average: ',i['temp']['day'])
                print("             Wind Speed: ", i['wind_speed'])
                print("             wind Degree ",i['wind_deg'])
                print("             UV index ",i['uvi'])
                print('-------------------------------------------------------------')
        if(count==0):
            print("\nWrong Date Entered\n")
        print("\nEnter 1 to get another forecast 2 to login else enter any key to exit")
        temp = str(input())
        if(temp == '1'):
            getforecast()
        if(temp == '2'):
            login()
        else:
            
            wronginput()    
@app.command()         
def login():
    print("To exit the application press 'CTRL+C' anytime")
    print('\n')
    print('-----------LOGIN PAGE---------')
    print('\n')
    name = str(input('Please enter the username: '))
    password = str(input('please enter the password: '))
    uname=name
    pwd=password
    #applying empty validation
    if uname=='' or pwd=='':
        print("fill the empty field!!!")
    else:
      #open database
      conn = sqlite3.connect('database.db')
      #select query
      cursor = conn.execute('SELECT USERNAME,PASSWORD FROM ADMIN WHERE USERNAME="%s" and PASSWORD="%s"'%(name,password))
      temp = cursor.fetchone()
      if(temp!=None):
         print("----------------------------------------------")
         print("               Login success                  ")
         print("----------------------------------------------")
         conn.close()
         getforecast()
         
      else:
          print("Wrong username or password!!!")
          print("\n")
          print("enter 1 to input again else press any key")
          print("\n")
          given = input("please give input: ")
          print('\n') 
          if(given == '1'):
              login()
          else:
              sys.exit()
@app.command()
def createuser():
    conn = sqlite3.connect('database.db')
    name = str(input('Please enter the username '))
    cursor = conn.execute('SELECT * from ADMIN where USERNAME="%s"'%(name))
    if(cursor.fetchone()):
        print('username already exists')
        print("enter 1 to input again\n")
        print("enter 2 for login page\n")
        print("enter any other key to exit\n")
        given = input("please give input ") 
        if(given == '1'):
            createuser()
        if(given == '2'):
            login()
        else:
            sys.exit()    
    password =  str(input('please enter the password '))
    cpassword = str(input('please confirm the password '))
    if(password != cpassword):
        print("passwords do not match.....")
        print("please try again")
        sys.exit()
    if(name=='' or password==''):
        print("field left empty!!!")
        createuser()
    else:
        conn.execute('insert into ADMIN (USERNAME, PASSWORD) VALUES ("%s","%s")'%(name,password))
        conn.commit()
        conn.close()
        print('-------------------------------')
        print("Account registered successfully")
        print("Redirecting to login page")
        print('-------------------------------')
        login()
@app.command()
def deleteuser():
    name = str(input('Please enter the username: '))
    password = str(input('please enter the password: '))
    #applying empty validation
    if name=='' or password=='':
        print("fill the empty field!!!")
    else:
      #open database
      conn = sqlite3.connect('database.db')
      #select query
      cursor = conn.execute('SELECT USERNAME,PASSWORD FROM ADMIN WHERE USERNAME="%s" and PASSWORD="%s"'%(name,password))
      temp = cursor.fetchone()
      if(temp!=None):
         conn.execute('DELETE FROM ADMIN WHERE USERNAME="%s" and PASSWORD="%s"'%(name,password))
         conn.commit()
         conn.close()
         print("----------------------------")
         print("SUCCESSFULLY DELETED")
         print("----------------------------")
         print("Redirecting to starting page")
         start()
@app.command()
def start():
    print('\n')
    print("Press 1 to Create User")
    print("Press 2 to Login")
    print("Press 3 to Delete user")
    print('-------------------------')        
    choose_start = {'1':createuser, '2':login,'3':deleteuser}
    try:
        start = input('Enter your choice: ')
        print('-------------------------')
        choose_start[start]()              
    except KeyError:
        print("\n")
        print("Wrong Input Given")
        wronginput()

if __name__ == "__main__":
    app()       
              