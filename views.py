from django.http import HttpResponse
from django.template import Template, Context
from django.template.loader import get_template
from dbmodels import getTableData
from tsforms import UserInterval
import pymongo

def graphAndTable(request):
    t = get_template('DatabaseChart.html')
    form = UserInterval()
    interval = 'Month'
    if request.method == "GET" and 'interval' in request.GET:
        interval = request.GET['interval']
    tableData = getTableData(interval)
    html = t.render(Context({'data' : tableData, 'form' : form, 'interval' : interval}))
    #print(html)  FOR DEBUG
    return HttpResponse(html)

        

          
