# 匯入Blueprint模組
import os
import time
import json
import urllib.request
from flask import render_template
from flask import Blueprint
from flask import request
from openai import OpenAI
from datetime import datetime
from utils import db

from utils import db

# 產生問題服務藍圖
question_bp = Blueprint('question_bp', __name__)

#--------------------------
# 在問題服務藍圖加入路由
#--------------------------

Recipes_image_path = ""
# client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", "OPENAI_API_KEY"))
# Recipes_image_path = "http://127.0.0.1:5000/static/images/openai"

#問題一
@question_bp.route('/question_n1')
def question1_selfList(): 
    return render_template('/question/question_n1.html', data='王小明')

#問題二
@question_bp.route('/question_n2')
def question2_selfList(): 
    return render_template('/question/question_n2.html', data='王小明')

#問題三-一
@question_bp.route('/question_n2_1')
def question2_1_selfList(): 
    return render_template('/question/question_n2_1.html', data='王小明')

#問題三
@question_bp.route('/question_n3')
def question3_selfList(): 
    return render_template('/question/question_n3.html', data='王小明')

#問題四
@question_bp.route('/question_n4')
def question4_selfList(): 
    return render_template('/question/question_n4.html', data='王小明')

#問題五
@question_bp.route('/question_n5')
def question5_selfList():
    return render_template('/question/question_n5.html', data='王小明')

#結果(money)
# @question_bp.route('/resultRecipe', methods=['GET', 'POST'])
# def resultRecipe_selfList(): 
#     if request.method == 'POST':
#         try:
#             tagInputValue1 = request.form.get('tagInputValue1')
#             tagInputValue2 = request.form.get('tagInputValue2')
#             tagInputValue3 = request.form.get('tagInputValue3')
#             tagInputValue4_1 = request.form.get('tagInputValue4_1')
#             tagInputValue5 = request.form.get('tagInputValue5')

#             content = f"飲食法:{tagInputValue1}; 主要食材:{tagInputValue2}; 營養需求:{tagInputValue3}; 烹調時間:{tagInputValue4_1}分鐘以內; 過敏成分或不吃的食物:{tagInputValue5}"

#             def wait_on_run(run, thread):
#                 while run.status == "queued" or run.status == "in_progress":
#                     run = client.beta.threads.runs.retrieve(
#                         thread_id=thread.id,
#                         run_id=run.id,
#                     )
#                     time.sleep(0.5)
#                 return run
            
#             # 食譜助理
#             thread = client.beta.threads.create()
#             message = client.beta.threads.messages.create(
#                 thread_id=thread.id,
#                 role="user",
#                 content=content,
#             )
#             run = client.beta.threads.runs.create(
#                 thread_id=thread.id,
#                 assistant_id='asst_uq2gPIFYGBn1gCda10ExVyj1',
#             )
#             run = wait_on_run(run, thread)
#             messages = client.beta.threads.messages.list(
#                 thread_id = thread.id
#             )
#             for message in reversed(messages.data):
#                 data = message.content[0].text.value

#             json_data = json.loads(data)    
#             print(json_data)

#             title = json_data["recipe"]["title"]
#             summary = json_data["recipe"]["summary"]
#             prepare = json_data["recipe"]["prepare"]
#             cookTime = json_data["recipe"]["cookTime"]
#             cookStep = json_data["recipe"]["cookStep"]
#             nutrition = json_data["recipe"]["nutrition"]
#             diet = json_data["recipe"]["diet"]
#             imagedescribe = json_data["imagedescribe"]
            
#             prepare_str = ', '.join(prepare)
#             cookStep_str = ', '.join(cookStep)
#             diet_str = ', '.join(diet)

#             # 估價助理
#             thread = client.beta.threads.create()
#             message = client.beta.threads.messages.create(
#                 thread_id=thread.id,
#                 role="user",
#                 content=prepare_str,
#             )
#             run = client.beta.threads.runs.create(
#                 thread_id=thread.id,
#                 assistant_id='asst_g2WebXcfXJBxfFP9VzMbBKQd',
#             )
#             run = wait_on_run(run, thread)
#             messages = client.beta.threads.messages.list(
#                 thread_id = thread.id
#             )
#             for message in reversed(messages.data):
#                 data2 = message.content[0].text.value
            
#             json_data2 = json.loads(data2)
#             print(json_data2)

#             prepareMoney = json_data2["prepareMoney"]
#             prepareMoney_str = ', '.join(prepareMoney)
#             total = json_data2["total"]

#             # 生成圖片
#             response = client.images.generate(
#                 model="dall-e-3",
#                 prompt = "食物在畫面的正中心，不能出現未說明的食材" + imagedescribe,
#                 n = 1,
#                 quality="standard",
#                 size = "1024x1024",
#             )
#             image_url = response.data[0].url
#             current_time = datetime.now()
#             image_name = "image" + current_time.strftime('%Y-%m-%d-%H-%M-%S') + ".png"
#             file_name = "static/images/openai/" + image_name
#             urllib.request.urlretrieve(image_url, file_name)

#              # DB
#             conn = db.get_connection()
#             cursor = conn.cursor()
#             cursor.execute("INSERT INTO body.cookbook (\"Uid\", title, summary, \"prepare\", \"prepareMoney\", \"cookTime\", \"cookStep\", nutrition, diet, \"cookImage\", \"cookImageDescribe\", \"isPublish\", diet_req, main_req, nutrition_req, cook_time_req, special_diet_req, create_time, update_time) VALUES (1,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, '0', %s, %s, %s, %s, %s, %s, %s)",
#                                 (title, summary, prepareMoney_str, total, cookTime, cookStep_str, nutrition, diet_str, image_name, imagedescribe, tagInputValue1, tagInputValue2, tagInputValue3, tagInputValue4_1, tagInputValue5, current_time, current_time))
#             conn.commit()
#             conn.close()
            
#             return render_template('/question/resultRecipe.html', data=json_data, data2=json_data2, image_name=image_name, Recipes_image_path=Recipes_image_path, current_time='2024-05-17')
#         except Exception as e:
#             # 印出錯誤原因
#             print('-'*30)
#             print(e)
#             print('-'*30)        
#             # 渲染失敗畫面
#             return render_template('/question/resultRecipe.html', data='王小明')
#     return render_template('/question/resultRecipe.html', data='王小明')

#結果測試(free)
@question_bp.route('/resultRecipe', methods=['GET', 'POST'])
def resultRecipe_selfList(): 
    if request.method == 'POST':
        try:
            json_data = {'recipe': {'title': '蔬菜蒸餃', 'summary': '這道蔬菜蒸餃是一種創意十足的美味料理，主要選用新鮮的青菜和豆腐作為餡料，搭配嫩滑的餃子皮，口感清爽又營養豐富。此外，這道料理能夠符合234飲食法需求，提供均衡的營養配比。', 'prepare': ['餃子皮: 300克', '大白菜: 150克', '豆腐: 100克', '紅蘿蔔: 50克', '香菇: 50克', '蔥: 2根'], 'cookTime': '60', 'cookStep': ['將大白菜和豆腐放入攪拌機中攪打成泥狀 ，取出備用。', '將紅蘿蔔和香菇切成末，蔥切碎，加入大白菜和豆腐泥中，攪拌均勻。', '將餃子皮包入蔬菜餡料，擀成餃子形狀。', '將餃子 放入蒸籠，加熱蒸15分鐘即可。'], 'nutrition': '這道蔬菜蒸餃提供均衡的營養配比，含有碳水化合物30%、蛋白質20%、脂質8%、維生素A、維生素C和膳食纖維。', 'diet': ['4']}, 'imagedescribe': '這道蔬菜蒸餃以清新的綠色蔬菜和豆腐製作，烹飪後呈現出養生美味的菜餚種類。餃子 整齊擺放在蒸籠中，餃子皮散發出微微的透明感，搭配點綴蔬菜碎末的綠色蔬菜餃子煞是好看。背景環境以多種蔬菜和水蒸氣炊煮的場景為主，營 造出溫馨家庭的氛圍。'}

            title = json_data["recipe"]["title"]
            summary = json_data["recipe"]["summary"]
            prepare = json_data["recipe"]["prepare"]
            cookTime = json_data["recipe"]["cookTime"]
            cookStep = json_data["recipe"]["cookStep"]
            nutrition = json_data["recipe"]["nutrition"]
            diet = json_data["recipe"]["diet"]
            imagedescribe = json_data["imagedescribe"]
            
            cookStep_str = ', '.join(cookStep)
            diet_str = ', '.join(diet)

            json_data2 = {'prepareMoney': ['餃子皮: 300克：45元', '大白菜: 150克：12元', '豆腐: 100克：10元', '紅蘿蔔: 50克：5元', '香菇: 50克：15元', '蔥: 2根：20元'], 'total': '107'}

            prepareMoney = json_data2["prepareMoney"]
            prepareMoney_str = ', '.join(prepareMoney)
            total = json_data2["total"]

            image_name = 'image2024-05-17-10-42-34.png'
            
            # DB
            # conn = db.get_connection()
            # cursor = conn.cursor()
            # cursor.execute("INSERT INTO body.cookbook (\"Uid\", title, summary, \"prepare\", \"prepareMoney\", \"cookTime\", \"cookStep\", nutrition, diet, \"cookImage\", \"cookImageDescribe\", \"isPublish\", diet_req, main_req, nutrition_req, cook_time_req, special_diet_req, create_time, update_time) VALUES (1,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, '0', %s, %s, %s, %s, %s, %s, %s)",
            #                     (title, summary, prepareMoney_str, total, cookTime, cookStep_str, nutrition, diet_str, image_name, imagedescribe, 'test', 'test', 'test', 'test', 'test', '2024-05-17', '2024-05-17'))
            # conn.commit()
            # conn.close()
            

            return render_template('/question/resultRecipe.html', data=json_data, data2=json_data2, image_name=image_name, Recipes_image_path=Recipes_image_path, current_time='2024-05-17')
        except Exception as e:
            # 印出錯誤原因
            print('-'*30)
            print(e)
            print('-'*30)        
            # 渲染失敗畫面
            return render_template('/question/resultRecipe.html', data='王小明')
    return render_template('/question/resultRecipe.html', data='王小明')