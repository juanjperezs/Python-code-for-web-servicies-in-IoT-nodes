# Python file that runs in the data server.
# The program gets the data from the mqtt broker
# and saves the data in a database.

import mysql.connector 
import paho.mqtt.client as mqtt
import json
import datetime



#ON_CONNECT 
def on_connect(mqttc, obj, flags, rc):
    print("rc: " + str(rc))

# ON_MESSAGE 
def on_message(mqttc, obj, msg):
    #TO INSERT FOR A PARTICULAR TOPIC BASED ON DB 
    #global connection
    #SQL CONNECTOR 
    mydb = mysql.connector.connect(
        host="localhost",
        user="x",
        password="x",
    )
 
    mycursor = mydb.cursor()
    print(msg.payload.decode("utf-8"))
    d=json.loads(msg.payload.decode("utf-8"))
    ts = datetime.datetime.now()
    Topic = msg.topic #d.get("Topic")
    print(Topic)
    Lista_Topic = Topic.split("/")
    Nariz_ID = Lista_Topic[0]
    Basededatos = Lista_Topic[1]
    Tabla = Lista_Topic[2]
    print(Lista_Topic)
    print(Nariz_ID)
    print(Basededatos)
    print(Tabla)
    Index = d.get("Index")
    Sample = d.get("Sample time")
    Power = d.get("Power")
    Mq135 = d.get("Mq135")
    Mq2 = d.get("Mq2")
    Mq3 = d.get("Mq3")
    Mq4 = d.get("Mq4")
    Mq5 = d.get("Mq5")
    Mq9 = d.get("Mq9")
    Mq7 = d.get("Mq7")
    Mq8 = d.get("Mq8")
    TempDS = d.get("TempDS")
    TempDHT = d.get("TempDHT")
    Humidity = d.get("Humidity")
    Sample_Name = d.get("Sample Name")
    Date = str(datetime.datetime.now().isoformat(timespec='minutes') )
    
    print("Topic "+ Topic)
    print("Index "+ str(Index))
    print("Sample "+ str(Sample))
    print("Power "+ str(Power))
    print("Mq135 "+ str(Mq135))
    print("Mq2 "+ str(Mq2))
    print("Mq3 "+ str(Mq3))
    print("Mq4 "+ str(Mq4))
    print("Mq5 "+ str(Mq5))
    print("Mq9 "+ str(Mq9))
    print("Mq7 "+ str(Mq7))
    print("Mq8 "+ str(Mq8))
    print("TempDS "+ str(TempDS))
    print("TempDHT "+ str(TempDHT))
    print("Humidity "+ str(Humidity))
    print("Sample Name "+ str(Sample_Name))
    print("Nariz_ID"+Nariz_ID)
    print("Date"+Date)
    
    
    ts = datetime.datetime.now()

    if Index==1:
		
        #CREATE DATABASE IF NOT EXISTS
        sqldrop = "CREATE DATABASE IF NOT EXISTS " + Basededatos
        print(sqldrop)
        mycursor.execute(sqldrop)
        result = mycursor.fetchall()
        print("result:")
        print(result)

        #OPEN DATABASE
        sqldrop = "USE " + Basededatos
        print(sqldrop)
        mycursor.execute(sqldrop)
        result = mycursor.fetchall()
        print("result:")
        print(result)

        
        #DROP TABLE IF EXISTS
        sqldrop = "DROP TABLE IF EXISTS " + Tabla
        print(sqldrop)
        mycursor.execute(sqldrop)
        result = mycursor.fetchall()
        print("result:")
        print(result)

        #CREATE TABLE IF NOT EXISTS
        create_table_query = "CREATE TABLE IF NOT EXISTS " 
        create_table_query += Tabla
        create_table_query += " (Ind int, Sample int, Power int, Mq135 int, Mq2 int, Mq3 int, Mq4 int, Mq5 int, Mq9 int, Mq7 int, Mq8 int, TempDS DECIMAL(5,2), TempDHT DECIMAL(5,2), Humidity DECIMAL(5,2), Sample_Name VARCHAR(10), Nariz_ID VARCHAR(10), Fecha VARCHAR(20), PRIMARY KEY (Ind))"
        print(create_table_query)
        mycursor.execute(create_table_query)
        result = mycursor.fetchall()
        print("result:")
        print(result)

        #CHECK IF THE TABLE EXISTS
        stmt="SHOW TABLES LIKE '" + Tabla +"'"
        print(stmt)
        mycursor.execute(stmt)
        result = mycursor.fetchall()
        print("result:")
        print(result)
    
    else:
        Nariz_ID = ""
        Date = ""
	
    #OPEN DATABASE
    sqldrop = "USE " + Basededatos
    print(sqldrop)
    mycursor.execute(sqldrop)
    result = mycursor.fetchall()
    print("result:")
    print(result)
    
    #INSERT A NEW FILE
    sql = "INSERT INTO "+ Tabla + " (Ind,Sample,Power,Mq135,Mq2,Mq3,Mq4,Mq5,Mq9,Mq7,Mq8,TempDS,TempDHT,Humidity,Sample_Name,Nariz_ID,Fecha) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    val = (Index,Sample,Power,Mq135,Mq2,Mq3,Mq4,Mq5,Mq9,Mq7,Mq8,TempDS,TempDHT,Humidity,Sample_Name,Nariz_ID,Date)
    print("sql is ",sql)
    print("val is ",val)
    mycursor.execute(sql, val)
    mydb.commit()
    print(mycursor.rowcount, "record inserted.")
    mydb.close()

# ON_PUBLISH 
def on_publish(mqttc, obj, mid):
    print("mid: " + str(mid))

#ON_ SUBSCRIBE
def on_subscribe(mqttc, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))
#ON_LOG
def on_log(mqttc, obj, level, string):
    print(string)



# If you want to use a specific client id, use
# mqttc = mqtt.Client("client-id")
# but note that the client id must be unique on the broker. Leaving the client
# id parameter empty will generate a random id for you.
mqttc = mqtt.Client()
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish
mqttc.on_subscribe = on_subscribe

# Uncomment to enable debug messages
# mqttc.on_log = on_log
mqttc.username_pw_set("x", "x")
mqttc.connect("localhost", 1883, 60)
mqttc.subscribe("#", 0)

mqttc.loop_forever()


#INSERT
# ~ Index = 1
# ~ Sample = 2
# ~ Power = 3
# ~ Mq135 = 4
# ~ Mq2 = 5
# ~ Mq3 = 6
# ~ Mq4 = 7
# ~ Mq5 = 8
# ~ Mq9 = 9
# ~ Mq7 = 10
# ~ Mq8 = 11
# ~ TempDS = 25.38
# ~ TempDHT = 27.99
# ~ Humidity = 50.67



