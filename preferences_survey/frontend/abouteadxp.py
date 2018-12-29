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

_page_name = "abouteadxp"

layout = html.Div([
    interface.survey_warning("warning_"+_page_name),
    interface.survey_ead_xp(),
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
    Output('abouteadxp_cache', 'children'),
    [Input('user_job_ead', 'value'),
     Input('user_time_experience', 'value'),
     Input('user_organization_worked', 'value'),
     Input('user_subject', 'value'),
     Input('user_ead_modality', 'value'),
     Input('user_avas_performed', 'value'),
     Input('user_avas_resources', 'value'),
     Input('user_students_age', 'value'),
     Input('user_students_scholarship', 'value'),
     Input('user_students_scholarship_degree', 'value'),
     Input('user_students_meaningful', 'value')])
def record_ead_xp(input1,input2,input3,input4,input5,input6,input7,input8,input9,input10,input11):
    
    inputs = [{'user_job_ead':input1},
              {'user_time_experience':input2},
              {'user_organization_worked':input3},
              {'user_subject':input4},
              {'user_ead_modality':input5},
              {'user_avas_performed':input6},
              {'user_avas_resources':input7},
              {'user_students_age':input8},
              {'user_students_scholarship':input9},
              {'user_students_scholarship_degree':input10},
              {'user_students_meaningful':input11},
              {'page':_page_name}
              ]
    
    return json.dumps(inputs)

@app.callback(
    Output('send_'+_page_name, 'href'),
    [Input('user_cache', 'children'),
     Input('user_job_ead', 'value'),
     Input('user_time_experience', 'value'),
     Input('user_organization_worked', 'value'),
     Input('user_subject', 'value'),
     Input('user_ead_modality', 'value'),
     Input('user_avas_performed', 'value'),
     Input('user_avas_resources', 'value'),
     Input('user_students_age', 'value'),
     Input('user_students_scholarship', 'value'),
     Input('user_students_scholarship_degree', 'value'),
     Input('user_students_meaningful', 'value')])
def update_body_ead_xp(input1,input2,input3,input4,input5,input6,input7,input8,input9,input10,input11,input12):
    if input1 == None:
        return '/'

    if input2 == '':
        return None
    else:
        return "aboutlogs"