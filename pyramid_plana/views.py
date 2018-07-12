from pyramid.view import (
    view_config,
    view_defaults
    )
from pyramid.response import Response
from .datadbhandler import getListOfEmployerIDs, getListOfEvents, insertNewEmployer, prepareEventForInsert, getEventData, getEmployerData, updateEmployerData, updateEventData, getEmployerByEventID, deleteEvent, deleteEmployer
import datetime
import json
from .forms import Schema1, Schema2, SchemaEvent, SchemaEmployer
from deform import Form, exception, Button, widget
import colander
import itertools
from pkg_resources import resource_filename
from pyramid.i18n import get_localizer
from pyramid.threadlocal import get_current_request


class homeViews(object):
    def __init__(self, request):
        self.request = request


    @view_config(route_name="home",request_method="POST", renderer="json")
    def postAnswer(self):
        startPostEvent = datetime.datetime.strptime(self.request.POST["start_date"], "%d.%m.%Y")
        endPostEvent = datetime.datetime.strptime(self.request.POST["end_date"], "%d.%m.%Y")
        startPostEvent = datetime.datetime(2018,7,20)
        endPostEvent = datetime.datetime(2018,8,4)
        return json.dumps(getListOfEvents(startPostEvent, endPostEvent), indent=4, sort_keys=True, default=str)

    @view_config(route_name='home', renderer='templates/default_planner.jinja2')
    def weekPlannerView(request):
       #Test variabeles:
       current_eventList = [{"employer":"Peter", "typeColor":"blue","width": "20%","padding":"30%"}]
       #---------------------------endTests--------------------
       diclist = getListOfEmployerIDs()
       current_view = {"type": "weekView", "begin_date": 3,"end_date": 3}
       current_dateList = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag"]
       getData = {"start_date": datetime.date(2018,7,9), "end_date": datetime.date(2018,7,14)}
       start_date = getData["start_date"]
       end_date = getData["end_date"]

       #Calculate the current_datelist from current_view with dates
       def daterange(start_date, end_date):
          for n in range(int((end_date - start_date).days)):
             yield start_date + datetime.timedelta(n)
       hard_dateList = []
       for single_date in daterange(start_date, end_date):
          hard_dateList.append(single_date.strftime("%a, %d %B %Y"))

       # You may use: today + datetime.timedelta(days=-today.weekday(), weeks=1)
       return {'current_view': current_view,
               'employers': diclist,
               'viewedDateCollums': hard_dateList
              }
    @view_config(route_name="multiweek", renderer="templates/default_planner_multiweek1.jinja2")
    def multiweek(self):
        if self.request.matchdict['amountWeeks']:
            amountOfWeeks = int(self.request.matchdict['amountWeeks'])
        else:
            amountOfWeeks = 2
        diclist = getListOfEmployerIDs()
        amountOfCollums = amountOfWeeks*6
        calcWidth = 100/amountOfCollums
        locale_name = 'de'
        counter = itertools.count()

        schema1 = Schema1()
        submit = Button(name="submit", title="Absenden", type="submit", value=None, disabled=False, css_class=None)
        form1 = Form(schema1, buttons=(submit,), formid='form1',
                            counter=counter)

        schema2 = Schema2()
        submit = Button(name="submit", title="Absenden", type="submit", value=None, disabled=False, css_class=None)
        form2 = Form(schema2, buttons=(submit,), formid='form2',
                            counter=counter)

        schemaem = SchemaEmployer()
        submit = Button(name="submit", title="Absenden", type="submit", value=None, disabled=False, css_class=None)
        formem = Form(schemaem, buttons=(submit,), formid='formem',
                     counter=counter)


        schemaev = SchemaEvent()
        submit = Button(name="submit", title="Absenden", type="submit", value=None, disabled=False, css_class=None)
        formev = Form(schemaev, buttons=(submit,), formid='formev',
                     counter=counter)


        #Looking for Submit from forms and redirecting:

        html = []
        captured = None

        if 'submit' in self.request.POST:
            posted_formid = self.request.POST['__formid__']
            for (formid, form) in [('form1', form1), ('form2', form2),('formem', formem), ('formev', formev)]:
                if formid == posted_formid:
                    try:
                        controls = self.request.POST.items()
                        captured = form.validate(controls)
                        if formid == "form1":
                            insertNewEmployer(captured)
                        elif formid == "form2":
                            prepareEventForInsert(captured)
                        elif formid == "formem":
                            updateEmployerData(captured, int(captured["employer_id"]))
                        elif formid == 'formev':
                            updateEventData(captured, int(captured["event_id"]))
                        html.append(form.render(captured))
                    except exception.ValidationFailure as e:
                        # the submitted values could not be validated
                        html.append(e.render())
                        i = html
                else:
                    html.append(form.render())
        else:
            for form in form1, form2:
                html.append(form.render())

        html1 = ''.join(html[0])
        html2 = ''.join(html[1])
        return {"amountOfWeeks": amountOfWeeks,
                "amountOfCollums": amountOfCollums,
                "daysInWeek": 6,
                'employers': diclist,
                "requestDayDivWidth": calcWidth,
                "requestWeekDivWidth": calcWidth*6,
                "amountOfEmployers":len(diclist),
                'form1': html1,
                'form2': html2,
                'captured': repr(captured),
                }


    @view_config(route_name="multiweekPost", request_method="POST", renderer="json")
    def newPost(self):
        current_viewWeeks = self.request.POST.mixed()
        return json.dumps(getListOfEvents(current_viewWeeks), indent=4, sort_keys=True, default=str)
    @view_config(route_name="multiweekForm", request_method="POST", renderer="json")
    def newForm(self):
        diclist = getListOfEmployerIDs()
        import itertools
        locale_name = 'de'
        counter = itertools.count()

        schemaem = SchemaEmployer()
        submit = Button(name="submit", title="Absenden", type="submit", value=None, disabled=False, css_class=None)
        formem = Form(schemaem, buttons=(submit,), formid='formem',
                     counter=counter)

        schemaev = SchemaEvent()
        submit = Button(name="submit", title="Absenden", type="submit", value=None, disabled=False, css_class=None)
        formev = Form(schemaev, buttons=(submit,), formid='formev',
                     counter=counter)

        html = ""
        captured = None

        readOnly = True
        if self.request.POST["readonly"]=="false":
            readOnly = False

        if 'submit' in self.request.POST:
            posted_formid = self.request.POST['__formid__']
            for (formid, form) in [('formem', formem), ('formev', formev)]:
                if formid == posted_formid:
                    try:
                        controls = self.request.POST.items()
                        captured = form.validate(controls)
                        if formid == "formem":
                            updateEmployerData(captured, int(captured["employer_id"]))
                        elif formid == "formev":
                            updateEventData(captured, int(captured["event_id"]))
                        html.append(form.render(captured))
                    except exception.ValidationFailure as e:
                        # the submitted values could not be validated
                        html.append(e.render())
                else:
                    html.append(form.render())
        else:
            for formDic in [{"id":'formem', "form": formem}, {"id":'formev', "form": formev}]:
                readData = colander.null
                if self.request.POST["requestType"]=="employer":
                    if formDic["id"] == "formem":
                        readData = getEmployerData(self.request.POST["identifier"])
                        html = (formDic["form"].render(readData, readonly=readOnly))
                elif self.request.POST['requestType']=="event":
                    if formDic["id"] == "formev":
                        readData = getEventData(int(self.request.POST["identifier"]))
                        html = (formDic["form"].render(readData, readonly=readOnly))


        html1 = ''.join(html)
        return {
            "form": html1,
        }

    @view_config(route_name="multiweekDelete", request_method="POST", renderer="json")
    def delete(self):
        id = self.request.POST["identifier"]
        if self.request.POST["object"] == "employer":
            deleteEmployer(id)
        elif self.request.POST['object'] == "event":
            deleteEvent(id)