#Libraries to be installed for successful app run
json, requests, geopy, sys, sqlite3, typer.

#Introduction
This application gives weather forecast of a specific city 
which can be choosen with latitude and longitude or by cityname.
The available forecast is for next days which can be accessed with
by typing the date.

#How to make appliction run
after ensuring that dependencies are correctly installed,
one can type
1) python weather_forecast.py --help
it will access the set the arguments that can be entered.
The app can be accessed by following commands also,

:- python weather_forecast.py start
This command will start the application.

:- python weather_forecast.py createuser
This command will help you creater a user.

:- python weather_forecast.py login
This command will take you directly to the login page.

:- python weather_forecast.py deleteuser
This command will help you to delete a user.

#What makes it work
The apps works mainly with the help of openweathermap.org which helps you get
the weather data with api, which is recieved by python with the help 
of requests library.
Another api was used that helps to get lattitude and longitde when
city name is entered.  
The User creation, deletion and login is made with the help of sqlite 
database that comes with python

