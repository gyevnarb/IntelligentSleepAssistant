# How to API

GET ip:port/data => get all sensor data

POST ip:port/data => post new sensor data entry

GET ip:port/data/<yyyy-mm-dd> => get all sensor data from a date

GET ip:port/sleep => get all sleep data from Fitbit api

GET ip:port/sleep/<date> => get sleep data from a set date
  
GET ip:port/processedData => get latest processed data

POST ip:port/processedDat => update processed data (this should be a PUT but i'm a big dumby)
