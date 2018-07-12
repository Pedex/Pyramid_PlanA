from argparse import _AppendAction

import pymongo
from random import randint
import datetime

client = pymongo.MongoClient("localhost", 27017) #Class from PyMongo module
db = client["rothe_plana"]

# Initialize database settings for employers and events collections:
employersCollect = db["employers"]
eventsCollect = db["events"]

#-----------------------------------------------------
#Employer database managment:
#-----------------------------------------------------

#Inserts passed dictionary objects of employer profiles:

def insertNewEmployer(new_employer_profile):
    while True:
        try:
            readyProfile = new_employer_profile.copy()
            readyProfile['employer_id'] = randint(100, 999)
            employersCollect.insert_one(readyProfile)
        except pymongo.errors.DuplicateKeyError:
            continue
        break

#Get and return list of employer ids to identify and render template elements.
def getListOfEmployerIDs():
    cursor = employersCollect.find({}, {"employer_id": 1, "name": 1, "_id": 0})
    employerIdList = []
    for elementID in cursor:
        employerIdList.append(elementID)
    return employerIdList

def getEmployerData(em_id):
    cursor = employersCollect.find({"employer_id": int(em_id)}, {"employer_id": 1, "employer_type": 1, "name": 1, "_id": 0})
    employerIdList = []
    for elementID in cursor:
        employerIdList.append(elementID)
    return employerIdList[0]

def updateEmployerData(captured, em_id):
    employersCollect.update_one({'employer_id': em_id}, {"$set": captured}, upsert=False)

def deleteEmployer(e_id):
    employersCollect.remove({"employer_id": int(e_id)})
    eventsCollect.remove({"event_employer_id": int(e_id)})



# -----------------------------------------------------
# Events database managment:
# -----------------------------------------------------

def deleteEvent(e_id):
    eventsCollect.remove({"event_id": int(e_id)})



def getEmployerByEventID(eID):
    cursor = eventsCollect.find({"event_id": int(eID)}, {"event_employer_id": 1, "_id": 0})
    employerIdList = []
    for elementID in cursor:
        employerIdList.append(elementID)
    employerId = employerIdList[0]["event_employer_id"]
    cursor = employersCollect.find({"employer_id": int(employerId)}, {"name": 1, "_id": 0})
    employerIdL = []
    for element in cursor:
        employerIdL.append(element)
    return employerIdL[0]["name"]


def getCoveredWeeks(begin_dt, end_dt):
    start, end = begin_dt.date(), end_dt.date()
    l = []
    for i in range((end-start).days + 1):
        d = (start+datetime.timedelta(days=i)).isocalendar()[:2] # e.g. (2011, 52)
        yearweek = '{} {}'.format(d[0], d[1])
        l.append(yearweek)
    sortL=sorted(set(l))
    sortedList = []
    for item in sortL:
        sortedList.append((item[4:]+" "+item[0:4]).lstrip())
    return sortedList


    #first_week, last_week = begin_date.isocalendar(), end_date.isocalendar()



#Inserts passed dictionary objects of event data:
def insertNewEvent(new_event_data):
    while True:
        try:
            readyEventData = new_event_data.copy()
            readyEventData['event_id'] = randint(10000000, 99999999)
            eventsCollect.insert_one(readyEventData)
        except pymongo.errors.DuplicateKeyError:
            continue
        break

def getEmployerNameByID(em_id):
    emList = []
    cursor = employersCollect.find({"employer_id": int(em_id)},
                                {"name": 1, "_id": 0})
    for elementID in cursor:
        emList.append(elementID)
    return emList[0]

def prepareEventForInsert(captured_event):
    capture_copy = captured_event.copy()
    del capture_copy["beginDate"]
    del capture_copy["beginTime"]
    del capture_copy["endDate"]
    del capture_copy["endTime"]
    del capture_copy["mitarbeiter"]
    capture_copy["event_employer_id"]=captured_event["mitarbeiter"]
    capture_copy["event_begin_date"] = datetime.datetime.combine(captured_event["beginDate"], captured_event["beginTime"])# + datetime.timedelta(hours=1)
    capture_copy["event_end_date"] = datetime.datetime.combine(captured_event["endDate"], captured_event["endTime"]) #+ datetime.timedelta(hours=1)
    capture_copy["event_coversWeeks"] = getCoveredWeeks(capture_copy["event_begin_date"], capture_copy["event_end_date"])
    resultDic = capture_copy
    insertNewEvent(resultDic)





def prepareEventForShow(event_dic_list):
    event_dic = event_dic_list[0]
    event_copy = event_dic.copy()
    del event_copy["event_begin_date"]
    del event_copy["event_end_date"]
    del event_copy["event_employer_id"]
    newEventDic = event_copy
    year,month, day, hours, minutes = event_dic["event_begin_date"].year, event_dic["event_begin_date"].month, event_dic["event_begin_date"].day, event_dic["event_begin_date"].hour, event_dic["event_begin_date"].minute
    yearEnd, monthEnd, dayEnd, hoursEnd, minutesEnd = event_dic["event_end_date"].year, event_dic["event_end_date"].month, event_dic["event_end_date"].day, event_dic["event_end_date"].hour, event_dic["event_end_date"].minute
    newEventDic["beginTime"] = datetime.time(hours, minutes)
    newEventDic["endTime"] = datetime.time(hoursEnd, minutesEnd)
    newEventDic["beginDate"] = datetime.date(year, month, day)
    newEventDic["endDate"] = datetime.date(yearEnd, monthEnd, dayEnd)
    newEventDic["mitarbeiter"] = getEmployerNameByID(event_dic["event_employer_id"])

    return newEventDic

def getEventData(event_id):
    cursor = eventsCollect.find({"event_id": event_id},
                                {"event_title": 1, "event_type": 1, "event_id": 1, "event_notes": 1,
                                 "event_begin_date": 1, "event_end_date": 1, "event_employer_id": 1,
                                 "event_coversWeeks": 1, "_id": 0})
    eventList = []
    for elementID in cursor:
        eventList.append(elementID)
    return prepareEventForShow(eventList)
#Get and return list of events to identify and render template elements.
def getListOfEvents(current_viewWeeks):
    dateList = []
    if type(current_viewWeeks["week[]"]) is str:
        dateList.append(str(current_viewWeeks["week[]"])+" "+str(current_viewWeeks["year[]"]))
    else:
        for f, b in zip(current_viewWeeks["week[]"], current_viewWeeks["year[]"]):
            stringO = str(f)+" "+str(b)
            dateList.append(stringO)
    eventList = []
    for weekYear in dateList:
        cursor = eventsCollect.find({"event_coversWeeks": weekYear},{"event_title": 1, "event_type": 1, "event_id": 1, "event_notes": 1,"event_begin_date": 1, "event_end_date": 1, "event_employer_id": 1,"event_coversWeeks": 1, "_id": 0})
        for elementID in cursor:
            eventList.append(elementID)

    return eventList

def updateEventData (captured_event, eID):
    eID = int(eID)
    capture_copy = captured_event.copy()
    del capture_copy["beginDate"]
    del capture_copy["beginTime"]
    del capture_copy["endDate"]
    del capture_copy["endTime"]
    del capture_copy["mitarbeiter"]
    capture_copy["event_employer_id"] = captured_event["mitarbeiter"]
    capture_copy["event_begin_date"] = datetime.datetime.combine(captured_event["beginDate"],
                                                                 captured_event["beginTime"]) # + datetime.timedelta(hours=1)
    capture_copy["event_end_date"] = datetime.datetime.combine(captured_event["endDate"],captured_event["endTime"]) #+ datetime.timedelta(hours=1)
    capture_copy["event_coversWeeks"] = getCoveredWeeks(capture_copy["event_begin_date"],capture_copy["event_end_date"])

    converted_dic = capture_copy
    eventsCollect.update_one({'event_id': eID}, {"$set": converted_dic}, upsert=False)




