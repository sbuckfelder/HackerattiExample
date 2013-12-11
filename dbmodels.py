import pymongo
import datetime
import random

def main():
    #populateDB()
    return

def getMongoData():
    #helper function to keep all of the MongoDB info together
    client = pymongo.MongoClient()
    db = client['hackDB']
    data = db['testData']
    return data

def getTableData(interval):
    dataDict = dataSlice(interval)
    return dataDict

def populateDB():
    #Populate a MongoDB with test data- removes all previous data first
    data = getMongoData()
    data.remove()

    #Data Start Date and empty list to be populated
    dateStamp = datetime.datetime(2013,10,1)
    recordList = []

    #Create a list of numRcords records to be added to the test DB
    numRecords = 500
    for x in range(0,numRecords):
        randMins = random.randrange(0,60)
        randValue = random.randrange(0,100)
        dateStamp = dateStamp + datetime.timedelta(minutes = randMins)
        recordList.append({"TimeStamp" : dateStamp, "Value" : randValue})

    #Add to Test DB
    data.insert(recordList)
    
    return

def dataSlice(interval):
    #get data from DB
    data = getMongoData()
    myCursor = data.find().sort('TimeStamp')

    #chose timedelta
    if interval == "Min" :
        timeBucket = datetime.timedelta(minutes = 1)
    elif interval == "Hour" :
        timeBucket = datetime.timedelta(hours = 1)
    elif interval == "Day" :
        timeBucket = datetime.timedelta(days = 1)
    elif interval == "Week" :
        timeBucket = datetime.timedelta(weeks = 1)
    elif interval == "Month" :
        timeBucket = datetime.timedelta(weeks = 4)
    elif interval == "Year" :
        timeBucket = datetime.timedelta(weeks = 52)        

    #get list of bucket dictionaries populate with begin and end timestamps
    lastItem = myCursor[myCursor.count()-1]
    firstItem = myCursor[0]
    timeDiff = lastItem['TimeStamp']-firstItem['TimeStamp'] #timedelta
    tempBucket = firstItem['TimeStamp']
    bucketList = []
    while tempBucket < lastItem['TimeStamp']:
        tempDict = {}
        tempDict['BeginTime'] = tempBucket
        tempBucket = tempBucket + timeBucket
        tempDict['EndTime'] = tempBucket
        tempCursor = data.find({"TimeStamp": {"$gte": tempDict['BeginTime'],"$lt": tempDict['EndTime'] }})
        value = 0
        count = 0
        for record in tempCursor:
            value = value + record['Value']
            count = count + 1
        tempDict['Count'] = count
        tempDict['SumValue'] = value
        tempDict['ColumnLabel'] = interval + ' starting ' + str(tempDict['BeginTime'])
        bucketList.append(tempDict)
        

    return bucketList

if __name__ == '__main__' :
    main()
