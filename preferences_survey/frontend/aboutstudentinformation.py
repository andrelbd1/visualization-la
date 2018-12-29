import json, datetime

from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_core_components as dcc

from app import app

from frontend import frontend
from backend import backend, feedbackmessage

feedmsg = feedbackmessage.feedbackmessage()
control = backend.backend()
interface = frontend.frontend()

_page_name = "aboutstudentinformation"

layout = html.Div([
    interface.survey_warning("warning_"+_page_name),
    interface.survey_student_information(),
    interface.survey_send("send_"+_page_name)
])


@app.callback(
    Output('warning_'+_page_name, 'children'),
    [Input('send_'+_page_name, 'href')])
def warning_body_about_you(input1):
    global feedmsg    
    if feedmsg.get_clicks() > 0:
        if input1 == None:
            return feedmsg.warning_message()

    feedmsg.add_clicks()
    return ""

@app.callback(
    Output('aboutstudentinformation_cache', 'children'),
    [Input('user_interaction_access_students_logs', 'value'),
     Input('user_interaction_access_students_logs_others', 'value'),
     Input('user_interaction_access_students_logs_presentation', 'value')])
def record_about_student_information(input1,input2,input3):
    
    inputs = [{'user_interaction_access_students_logs':input1},
              {'user_interaction_access_students_logs_others':input2},
              {'user_interaction_access_students_logs_presentation':input3},
              {'page':_page_name}
              ]
    
    return json.dumps(inputs)

@app.callback(
    Output('send_'+_page_name, 'href'),
    [Input('user_cache', 'children'),
     Input('user_interaction_access_students_logs', 'value'),
     Input('user_interaction_access_students_logs_others', 'value'),
     Input('user_interaction_access_students_logs_presentation', 'value')])
def update_body_about_student_information(input1,input2,input3,input4):
    if input1 == None:
        return '/'

    if input2 == '':
        return None
    else:
        return "aboutvisualization"