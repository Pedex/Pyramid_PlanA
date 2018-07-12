import colander
import itertools
from deform import Form, exception, Button, widget
from .datadbhandler import getListOfEmployerIDs




class Schema1(colander.Schema):
    locale_name = 'de'
    counter = itertools.count()
    diclist = getListOfEmployerIDs()
    typeChoices = (('', '-Auswählen-'),
                   ('fliesenleger', 'Fliesenleger'),
                   ('fahrer', 'Fahrer')
                   )
    name = colander.SchemaNode(colander.String())
    employer_type = colander.SchemaNode(colander.String(), title="Beschäftigung",
                                        widget=widget.SelectWidget(values=typeChoices)
                                        )

    _LOCALE_ = colander.SchemaNode(
        colander.String(),
        widget=widget.HiddenWidget(),
        default=locale_name)





class Schema2(colander.Schema):
    locale_name = 'de'
    counter = itertools.count()
    diclist = getListOfEmployerIDs()
    artChoices = (('', '-Auswählen-'),
                  ('baustelle', 'Baustelle'),
                  ('urlaub', 'Urlaub')
                  )
    tList = []
    for dicEl in diclist:
        val = dicEl["name"]
        tList.append((dicEl["employer_id"], val))
    employerTuple = tuple(tList)

    event_title = colander.SchemaNode(colander.String(), title="Titel")
    event_type = colander.SchemaNode(colander.String(), title="Ereignis-Art",
                                     widget=widget.SelectWidget(values=artChoices))
    mitarbeiter = colander.SchemaNode(colander.String(), widget=widget.SelectWidget(values=employerTuple))
    beginDate = colander.SchemaNode(colander.Date(), title="Begin-Datum", widget=widget.DateInputWidget())
    beginTime = colander.SchemaNode(colander.Time(), title="Begin-Zeit", widget=widget.TimeInputWidget())
    endDate = colander.SchemaNode(colander.Date(), title="End-Datum", widget=widget.DateInputWidget())
    endTime = colander.SchemaNode(colander.Time(), title="End-Zeit", widget=widget.TimeInputWidget())
    event_notes = colander.SchemaNode(colander.String(), title="Anmerkung", widget=widget.TextAreaWidget(rows=2))


class SchemaEvent(colander.Schema):
    locale_name = 'de'
    counter = itertools.count()
    diclist = getListOfEmployerIDs()
    artChoices = (('', '-Auswählen-'),
                  ('baustelle', 'Baustelle'),
                  ('urlaub', 'Urlaub')
                  )
    tList = []
    for dicEl in diclist:
        val = dicEl["name"]
        tList.append((dicEl["employer_id"], val))
    employerTuple = tuple(tList)

    event_title = colander.SchemaNode(colander.String(), title="Titel")
    event_id = colander.SchemaNode(colander.Int(), title="Event ID")
    event_type = colander.SchemaNode(colander.String(), title="Ereignis-Art",
                                     widget=widget.SelectWidget(values=artChoices))
    mitarbeiter = colander.SchemaNode(colander.String(), widget=widget.SelectWidget(values=employerTuple))
    beginDate = colander.SchemaNode(colander.Date(), title="Begin-Datum", widget=widget.DateInputWidget())
    beginTime = colander.SchemaNode(colander.Time(), title="Begin-Zeit", widget=widget.TimeInputWidget())
    endDate = colander.SchemaNode(colander.Date(), title="End-Datum", widget=widget.DateInputWidget())
    endTime = colander.SchemaNode(colander.Time(), title="End-Zeit", widget=widget.TimeInputWidget())
    event_notes = colander.SchemaNode(colander.String(), title="Anmerkung",
                                      widget=widget.TextAreaWidget(rows=2))


class SchemaEmployer(colander.Schema):
    locale_name = 'de'
    counter = itertools.count()
    diclist = getListOfEmployerIDs()
    typeChoices = (('', '-Auswählen-'),
                   ('fliesenleger', 'Fliesenleger'),
                   ('fahrer', 'Fahrer')
                   )
    name = colander.SchemaNode(colander.String())
    employer_type = colander.SchemaNode(colander.String(), title="Beschäftigung",
                                        widget=widget.SelectWidget(values=typeChoices)
                                        )
    employer_id = colander.SchemaNode(colander.Int(), title="Mitarbeiter-ID")
    _LOCALE_ = colander.SchemaNode(
        colander.String(),
        widget=widget.HiddenWidget(),
        default=locale_name)
