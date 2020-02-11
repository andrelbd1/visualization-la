import pandas as pd
import os, sys
import json

from datetime import datetime
from app.eduvis.constants import LST_VIEW_INFORMATION
from app.eduvis.constants import SUB_TOPIC
from app.eduvis.backend.connection_db import Connection_DB

class User:    
    _conn = Connection_DB()

    def __init__(self,conn):
        self._conn = conn        

    def get_name(self, user_id):
        res_db = self._conn.select("user",(int(user_id),))
        name = res_db[0][1]
        return name

    def get_static_dashboard_id(self, user_id, name='default'):
        if name == 'default':
            name = "Dashboard Default Fixo"

        res_db = self._conn.select("dashboard_name",(int(user_id),name))
        dash_id = res_db[0][0]
        return dash_id

    def get_customizable_dashboard_id(self, user_id, name='default'):
        if name == 'default':
            name = "Dashboard Default Customizável"

        res_db = self._conn.select("dashboard_name",(int(user_id),name))        
        dash_id = res_db[0][0]        
        return dash_id

    def initalize_dashboard(self,user_id,type_dash,language):
        now = datetime.now()
        current_time = now.strftime("%Y-%m-%d %H:%M:%S")
        name = ""
        if type_dash == 0:
            name = "Dashboard Default Fixo"
        elif type_dash == 1:
            name = "Dashboard Default Customizável"

        dash_id = self._conn.insert("tb_dashboard",(user_id, name, type_dash, language, current_time), True)

        lst_dashboard_topic_chart = []
        lst_dashboard_topic_chart.append((dash_id, 15, 1, "", 1))
        lst_dashboard_topic_chart.append((dash_id, 27, 2, "", 1))
        lst_dashboard_topic_chart.append((dash_id, 30, 3, "", 1))
        lst_dashboard_topic_chart.append((dash_id, 40, 4, "", 1))
        lst_dashboard_topic_chart.append((dash_id, 42, 5, "", 1))
        lst_dashboard_topic_chart.append((dash_id, 55, 6, "", 1))
        lst_dashboard_topic_chart.append((dash_id, 64, 7, "", 1))
        lst_dashboard_topic_chart.append((dash_id, 70, 8, "", 1))
        lst_dashboard_topic_chart.append((dash_id, 76, 9, "", 1))
        lst_dashboard_topic_chart.append((dash_id, 88, 10, "", 1))
        lst_dashboard_topic_chart.append((dash_id, 117, 11, "", 1))
        lst_dashboard_topic_chart.append((dash_id, 126, 12, "", 1))
        lst_dashboard_topic_chart.append((dash_id, 153, 13, "", 1))
        self._conn.insert_many("tb_dashboard_topic_chart",lst_dashboard_topic_chart)
        

    def record_about_user(self,data,id=None):
        if id == None:
            now = datetime.now()
            current_time = now.strftime("%Y-%m-%d %H:%M:%S")            
            user_id = self._conn.insert("tb_user",(data['nomecompleto'],data['idade'],data['localorigem'],data['localtrabalho'],data['areaformacao'],data['escolaridade'],data['profissao'], current_time), True)
            
            self._conn.insert("tb_user_background",(user_id, int(data['avaxp']), "", "", "", "", "", "", "", "", "", "", "", "", ""))
            self.initalize_dashboard(user_id, 0, 1) #Adding Static Dashboard
            self.initalize_dashboard(user_id, 1, 1) #Adding Customizable Dashboard
            
            lst_evaluate_topic = []
            for i in range(1,len(SUB_TOPIC)+1):
                lst_evaluate_topic.append((user_id,i,""))
            
            self._conn.insert_many("tb_evaluate",lst_evaluate_topic)

            return user_id
        else:            
            self._conn.update("tb_user", (data['nomecompleto'],data['idade'],data['localorigem'],data['localtrabalho'],data['areaformacao'],data['escolaridade'],data['profissao'],id))
            self._conn.update("tb_user_background", (int(data['avaxp']), "", "", "", "", "", "", "", "", "", "", "", "", "", id))
        

    def record_ava_xp(self,data,id):
        self._conn.update("tb_user_background", (1, data['papeisavas'], data['tempoexpavas'], data['instituicao'], data['disciplinas'], data['avaxp'], data['avasusados'], data['recursosusados'], data['idadealunos'], data['inforelevante'], "", "", "", "", id))        

    def record_data(self,data,id):
        lst_evaluate_topic = []
        for i in range(1,len(SUB_TOPIC)+1): #Get all evaluations for each subtopics
            lst_evaluate_topic.append((data[str(i)],id,i))
        
        self._conn.update("user_background_data", (data['gostariadado'], data['comoapresentar'],id))        
        self._conn.update_many("tb_evaluate",lst_evaluate_topic)

    def record_visualization_xp(self,data,id):        
        self._conn.update("user_background_visualization", (data['frequencialeitura'], data['frequenciacria'],id))

    def record_evaluation_dashboard(self,type_dash,data,id):
        keys = list(data.keys())
        lst_feedbacks = []
        for key in keys:
            topic = int(key.split("@")[0].replace('T',''))
            chart = key.split("@")[1]+'@'+key.split("@")[2]
            feedback = data[key]
            lst_feedbacks.append((feedback, id, type_dash, topic, chart))

        self._conn.update_many("dashboard_feedback",lst_feedbacks)
        