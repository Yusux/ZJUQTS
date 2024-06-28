import json
import requests
import re
from .zjuam import ZJUAM

URL_ALT = 'https://alt.zju.edu.cn'
URL_DAPI = 'dapi/v2'
URL_TES = 'tes/evaluation_plan_service'

class ALT(ZJUAM):
    """
    ALT is a class derived from ZJUAM that helps you login to ALT
    and do operations related to ALT.
    """

    def __init__(
        self,
        username: str,
        password: str
    ):
        super().__init__(username, password)
        self.session = requests.Session()
        self.token = None
    
    def login(self):
        # using the ipd got to login
        try:
            self.session.cookies.update({'iPlanetDirectoryPro': self.ipd_fetch()})
        except:
            raise
        
        try:
            response = self.session.get(
                'https://zjuam.zju.edu.cn/cas/login?service=' + URL_ALT + '/ua/login?platform=WEB&target=%2F',
                allow_redirects=False
            )
        except:
            raise Exception('alt: Failed to access the login page')
        
        try:
            # just follow the redirect
            for _ in range(2):
                response = self.session.get(
                    response.headers['Location'],
                    allow_redirects=False
                )
            
            # check the url to get token
            url = response.headers['Location']
            if 'token' not in url:
                raise Exception('alt: Failed to get the token')
            self.token = re.search(r'token=(.*?)$', url).group(1)
            self.session.headers.update({
                'Authorization': f'Bearer {self.token}',
                'Content-Type': 'application/json'
            })
        except:
            raise Exception('alt: Failed to get the user token')
    
    def get_todo_courses_list(self):
        try:
            response = self.session.post(
                URL_ALT + '/' + URL_DAPI + '/' + URL_TES + '/page_my_todo_plan_course_list',
                # data='{"pageNum":0,"pageSize":1}'
                data=json.dumps({"pageNum": 0, "pageSize": 4})
            )
            return response.json()
        except:
            raise Exception('alt: Failed to get the todo courses list')
    
    def find_plan_course(self, plan_course_id: str):
        try:
            response = self.session.post(
                URL_ALT + '/' + URL_DAPI + '/' + URL_TES + '/find_plan_courses_by_user',
                data=json.dumps({"planCourseId": plan_course_id})
            )
            return response.json()
        except:
            raise Exception('alt: Failed to get the plan courses list')
    
    def insert_document(self, group_id: str):
        try:
            response = self.session.post(
                URL_ALT + '/' + URL_DAPI + '/autoform/document_service/insert_document',
                data=json.dumps({
                    "groupId": group_id,
                    "value": {
                        "oadpflA": 5,
                        "cHfvSga": 5,
                        "iuFCIOj": 5,
                        "FtFBhMR": 5,
                        "UuWdHvl": 5
                    }
                })
            )
            return response.json()
        except:
            raise Exception('alt: Failed to insert the document')
    
    def save_plan_course(self, course_id: str, form_id: str, tea_sid: str):
        try:
            response = self.session.post(
                URL_ALT + '/' + URL_DAPI + '/' + URL_TES + '/save_plan_courses_by_user',
                data=json.dumps({
                    "planCourseId": course_id,
                    "teaching": True,
                    "formId": form_id,
                    "teaSid": tea_sid
                })
            )
            return response.json()
        except:
            raise Exception('alt: Failed to save the plan course')