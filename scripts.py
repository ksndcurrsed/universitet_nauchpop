import requests

class parse:
    def __init__(self, course: str):
        self.course = course
    
    
    def schedule(self, course):
        linkresp = 'http://www.fa.ru/fil/kaluga/student/Documents/%d0%a0%d0%b0%d1%81%d0%bf%d0%b8%d1%81%d0%b0%d0%bd%d0%b8%d0%b5/'+ course + '%20%d0%ba%d1%83%d1%80%d1%81.pdf'
        response = requests.get(linkresp)
        with open('расписание.pdf', 'wb') as file:
            file.write(response.content)
        return 'сделано'

                            
