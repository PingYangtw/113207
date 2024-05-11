#-----------------------
# 匯入模組
#-----------------------
import os
import time
import urllib.request
from flask import Flask, render_template 
from openai import OpenAI
from datetime import datetime
from utils import db

#-----------------------
# 匯入各個服務藍圖
#-----------------------
from services.robott.app import robott_bp
from services.question.app import question_bp
from services.goal.app import goal_bp
from services.community.app import community_bp
from services.task.app import task_bp
from services.profile.app import profile_bp

#-------------------------
# 產生主程式, 加入主畫面
#-------------------------
app = Flask(__name__)

#主畫面
@app.route('/')
def index():
    connection = db.get_connection() 
    
    cursor = connection.cursor()     
    cursor.execute('SELECT "knowTitle", "knowContent" FROM body.knowledge ORDER BY RANDOM() LIMIT 1;')
    
    data = cursor.fetchone()   

    connection.close()

    return render_template('/home/home.html', data=data) 

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", "openai-api-key"))

#json-data
@app.route('/json-data')
def json_data():
    thread = client.beta.threads.create()

    # Create a message to append to our thread
    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content="營養需求：無糖；餐點時段：午餐；主要食材：馬鈴薯；烹調時間：無要求；特殊飲食需求：素食",
    )

    # Execute our run
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id='asst_SrcfhWBYSD0L1CMhGPSpeEoV',
    )

    def wait_on_run(run, thread):
        while run.status == "queued" or run.status == "in_progress":
            run = client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id,
            )
            time.sleep(0.5)
        return run

    run = wait_on_run(run, thread)

    # Retrieve all the messages added after our last user message
    messages = client.beta.threads.messages.list(
        thread_id = thread.id
    )

    for message in reversed(messages.data):
        data = message.content[0].text.value

    response = client.images.generate(
        prompt = "番茄炒蛋，以新鮮番茄和有機蛋為主角，搭配橄欖油，色彩鮮艷，濃淡相間，散發清新氣息。",
        n = 1,
        size = "256x256",
    )

    image_url = response.data[0].url

    file_name = "static/images/openai/" + "image" + datetime.now().strftime('%Y-%m-%d-%H-%M-%S') + ".png"
    urllib.request.urlretrieve(image_url, file_name)


    return render_template('/json-data.html',  data=data)

    

#-------------------------
# 在主程式註冊各個服務
#-------------------------
app.register_blueprint(robott_bp, url_prefix='/robott')
app.register_blueprint(question_bp, url_prefix='/question')
app.register_blueprint(goal_bp, url_prefix='/goal')
app.register_blueprint(community_bp, url_prefix='/community')
app.register_blueprint(task_bp, url_prefix='/task')
app.register_blueprint(profile_bp, url_prefix='/profile')

#-------------------------
# 啟動主程式
#-------------------------
if __name__ == '__main__':
    app.run(port=5000, debug=True)