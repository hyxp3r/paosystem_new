from paosystem.celery import app
from .service import send
from .studyload import StudyLoad
import io
import base64

@app.task
def send_spam_email(user_email):
    send(user_email)

@app.task
def make_study_load(file):

    print("Start")

    byte_data = file['file'].encode(encoding='utf-8')
      
    b = base64.b64decode(byte_data)
      
    b = io.BytesIO(b)

    print(StudyLoad(b).makeLoad())
    
    

