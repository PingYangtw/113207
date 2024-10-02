# 匯入Blueprint模組
import os
import threading
import time
import json
import urllib.request
import azure.cognitiveservices.speech as speechsdk
from flask import render_template, Blueprint, request, session, jsonify
from concurrent.futures import ThreadPoolExecutor
from openai import OpenAI
from datetime import datetime
from utils import db

# 產生問題服務藍圖
question_bp = Blueprint('question_bp', __name__)

#--------------------------
# 在問題服務藍圖加入路由
#--------------------------

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", "OPENAI_API_KEY"))
Recipes_image_path = "/static/images/openai"

speech_config = speechsdk.SpeechConfig(
    subscription=os.environ.get("SPEECH_KEY", "SPEECH_KEY"),
    region="southeastasia"  # 區域
)

speech_config.speech_synthesis_voice_name = "zh-TW-HsiaoChenNeural"

#問題一
@question_bp.route('/question_n1')
def question1_selfList(): 
    if "google_id" in session:
        name=session['name']
        userImage=session['user_image']
        uid=session['uid']
    else:
        name='0'
        userImage='0'
        uid='0'

    return render_template('/question/question_n1.html', name=name, userImage=userImage, uid=uid)

#問題二
@question_bp.route('/question_n2')
def question2_selfList(): 
    if "google_id" in session:
        name=session['name']
        userImage=session['user_image']
        uid=session['uid']
    else:
        name='0'
        userImage='0'
        uid='0'
    
    return render_template('/question/question_n2.html', name=name, userImage=userImage, uid=uid)

#問題三-一
@question_bp.route('/question_n2_1')
def question2_1_selfList(): 
    if "google_id" in session:
        name=session['name']
        userImage=session['user_image']
        uid=session['uid']
    else:
        name='0'
        userImage='0'
        uid='0'

    return render_template('/question/question_n2_1.html', name=name, userImage=userImage, uid=uid)

#問題三
@question_bp.route('/question_n3')
def question3_selfList(): 
    if "google_id" in session:
        name=session['name']
        userImage=session['user_image']
        uid=session['uid']
    else:
        name='0'
        userImage='0'
        uid='0'

    return render_template('/question/question_n3.html', name=name, userImage=userImage, uid=uid)

#問題四
@question_bp.route('/question_n4')
def question4_selfList(): 
    if "google_id" in session:
        name=session['name']
        userImage=session['user_image']
        uid=session['uid']
    else:
        name='0'
        userImage='0'
        uid='0'

    return render_template('/question/question_n4.html', name=name, userImage=userImage, uid=uid)

#問題五
@question_bp.route('/question_n5')
def question5_selfList(): 
    if "google_id" in session:
        name=session['name']
        userImage=session['user_image']
        uid=session['uid']
    else:
        name='0'
        userImage='0'
        uid='0'

    return render_template('/question/question_n5.html', name=name, userImage=userImage, uid=uid)

# #結果(money)
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
#             cursor.execute("INSERT INTO body.cookbook (\"Uid\", title, summary, \"prepare\", \"prepareMoney\", \"cookTime\", \"cookStep\", nutrition, diet, \"cookImage\", \"cookImageDescribe\", \"isPublish\", diet_req, main_req, nutrition_req, cook_time_req, special_diet_req, create_time, update_time) VALUES (%s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, '0', %s, %s, %s, %s, %s, %s, %s)",
#                                 (uid, title, summary, prepareMoney_str, total, cookTime, cookStep_str, nutrition, diet_str, image_name, imagedescribe, tagInputValue1, tagInputValue2, tagInputValue3, tagInputValue4_1, tagInputValue5, current_time, current_time))
#             conn.commit()
#             conn.close()
            
#             return render_template('/question/resultRecipe.html', data=json_data, data2=json_data2, image_name=image_name, Recipes_image_path=Recipes_image_path, current_time=current_time)
#         except Exception as e:
#             # 印出錯誤原因
#             print('-'*30)
#             print(e)
#             print('-'*30)        
#             # 渲染失敗畫面
#             return render_template('/question/resultRecipe.html', name=name)
#     return render_template('/question/resultRecipe.html', name=name)

@question_bp.route('/resultRecipe', methods=['POST'])
def resultRecipe_selfList(): 
    name=session['name']
    uid=session['uid']
    userImage=session['user_image']
        
    if request.method == 'POST':
        try:
            tagInputValue1 = request.form.get('tagInputValue1')
            tagInputValue2 = request.form.get('tagInputValue2')
            tagInputValue3 = request.form.get('tagInputValue3')
            tagInputValue4_1 = request.form.get('tagInputValue4_1')
            tagInputValue5 = request.form.get('tagInputValue5')

            content = f"飲食法:{tagInputValue1}; 主要食材:{tagInputValue2}; 營養需求:{tagInputValue3}; 烹調時間:{tagInputValue4_1}分鐘以內; 過敏成分或不吃的食物:{tagInputValue5}"

            print(content)
            
            def wait_on_run(run, thread):
                while run.status == "queued" or run.status == "in_progress":
                    run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
                    time.sleep(0.5)
                return run

            # 食譜助理執行緒
            def recipe_assistant():
                thread = client.beta.threads.create()
                message = client.beta.threads.messages.create(thread_id=thread.id, role="user", content=content)
                run = client.beta.threads.runs.create(thread_id=thread.id, assistant_id='asst_uq2gPIFYGBn1gCda10ExVyj1')
                run = wait_on_run(run, thread)
                messages = client.beta.threads.messages.list(thread_id=thread.id)
                for message in reversed(messages.data):
                    data = message.content[0].text.value
                print(json.loads(data))
                return json.loads(data)

            # 估價助理執行緒
            def pricing_assistant(prepare_str):
                thread = client.beta.threads.create()
                message = client.beta.threads.messages.create(thread_id=thread.id, role="user", content=prepare_str)
                run = client.beta.threads.runs.create(thread_id=thread.id, assistant_id='asst_g2WebXcfXJBxfFP9VzMbBKQd')
                run = wait_on_run(run, thread)
                messages = client.beta.threads.messages.list(thread_id=thread.id)
                for message in reversed(messages.data):
                    data2 = message.content[0].text.value
                print(json.loads(data2))
                return json.loads(data2)

            # 生成圖片執行緒
            def generate_image(imagedescribe):
                response = client.images.generate(
                    model="dall-e-3",
                    prompt="食物在畫面的正中心，不能出現未說明的食材" + imagedescribe,
                    n=1,
                    quality="hd",
                    size="1024x1024",
                )
                image_url = response.data[0].url
                current_time = datetime.now()
                image_name = "image" + current_time.strftime('%Y-%m-%d-%H-%M-%S') + ".png"
                file_name = "static/images/openai/" + image_name
                urllib.request.urlretrieve(image_url, file_name)
                return image_name
            
            # 生成音檔執行緒
            def generate_audio(text):
                # 在/static/mp3/uid資料夾下生成音檔
                audio_path = f"static/mp3/{uid}"

                if not os.path.exists(audio_path):
                    os.makedirs(audio_path)

                # 檔案名稱，uid+時間戳
                current_time = datetime.now()
                filename = f"{uid}-{current_time.strftime('%Y-%m-%d-%H-%M-%S')}.mp3"
                file_path = f"{audio_path}/{filename}"

                # 在每個句號後面加入 3 秒的停頓
                text_with_pause = text.replace('。', '。<break time="3000ms"/>')

                # 將文本轉換為 SSML 格式
                ssml_text = f"""
                <speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="zh-TW">
                    <voice name="zh-TW-HsiaoChenNeural">
                        {text_with_pause}
                    </voice>
                </speak>
                """

                # 輸出配置
                audio_config = speechsdk.audio.AudioOutputConfig(filename=file_path)
                synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

                # 生成
                result = synthesizer.speak_ssml_async(ssml_text).get()

                if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
                    return filename
                else:
                    error_message = f"Error synthesizing speech: {result.error_details}"
                    print(error_message)
                    if result.cancellation_details.reason == speechsdk.CancellationReason.Error:
                        print(f"Error details: {result.cancellation_details.error_details}")
                    raise Exception(error_message)

            with ThreadPoolExecutor() as executor:
                # 同時執行多個任務
                recipe_future = executor.submit(recipe_assistant)
                recipe_data = recipe_future.result()

                title = recipe_data["recipe"]["title"]
                summary = recipe_data["recipe"]["summary"]
                prepare = recipe_data["recipe"]["prepare"]
                cookTime = recipe_data["recipe"]["cookTime"]
                cookStep = recipe_data["recipe"]["cookStep"]
                nutrition = recipe_data["recipe"]["nutrition"]
                diet = recipe_data["recipe"]["diet"]
                imagedescribe = recipe_data["imagedescribe"]

                prepare_str = ', '.join(prepare)
                cookStep_str = ', '.join(cookStep)
                nutrition_str = ', '.join(nutrition)
                diet_str = ', '.join(diet)

                pricing_future = executor.submit(pricing_assistant, prepare_str)
                pricing_data = pricing_future.result()

                prepareMoney = pricing_data["prepareMoney"]
                prepareMoney_str = ', '.join(prepareMoney)
                total = pricing_data["total"]

                image_future = executor.submit(generate_image, imagedescribe)
                image_name = image_future.result()

                # 在每一個cookStep開頭加上步驟編號
                cookStep_audiostr = ''
                for i, step in enumerate(cookStep, 1):
                    cookStep_audiostr += f"步驟{i}, {step}。"

                audio_future = executor.submit(generate_audio, cookStep_audiostr)
                audio_name = audio_future.result()

            current_date = datetime.now().strftime("%Y-%m-%d")
            

            # DB
            def db_insert():
                conn = db.get_connection()
                cursor = conn.cursor()
                cursor.execute("INSERT INTO body.cookbook (\"Uid\", title, summary, \"prepare\", \"prepareMoney\", \"cookTime\", \"cookStep\", \"cookStep_mp3\",  nutrition, diet, \"cookImage\", \"cookImageDescribe\", \"isPublish\", diet_req, main_req, nutrition_req, cook_time_req, special_diet_req, create_time, update_time) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, '0', %s, %s, %s, %s, %s, now(), now())",
                    (uid, title, summary, prepareMoney_str, total, cookTime, cookStep_str, audio_name, nutrition_str, diet_str, image_name, imagedescribe, tagInputValue1, tagInputValue2, tagInputValue3, tagInputValue4_1, tagInputValue5))
                
                cursor.execute('''
                    SELECT "Cookid" 
                    FROM body.cookbook 
                    WHERE title = %s AND "Uid" = %s 
                    ORDER BY "Cookid" DESC 
                    LIMIT 1;
                               ''', (title, uid))
                
                recipe_id = cursor.fetchone()[0]

                conn.commit()
                conn.close()

                return recipe_id

            recipe_id = db_insert()

            return jsonify({'recipe_id': recipe_id})
        
        except Exception as e:
            # 印出錯誤原因
            print('-'*30)
            print(e)
            print('-'*30)
            # 渲染失敗畫面
            # logging.error("Error occurred", exc_info=True)
            # logging.basicConfig(filename='../error.log', level=logging.ERROR)
            # 渲染錯誤畫面並返回錯誤信息
            return render_template('/question/error.html', error_message=str(e))


# #結果測試(free)
# @question_bp.route('/resultRecipe', methods=['GET', 'POST'])
# def resultRecipe_selfList(): 
#     if request.method == 'POST':
#         try:
#             json_data = {'recipe': {'title': '地中海風情的巧克力蛋糕', 'summary': '這款地中海風味的巧克力蛋糕熱量低，糖分含量低，十分適合健康飲食的你。特別添加了新鮮的藍莓和 橄欖油，讓口感更加滿足，又不失健康。', 'prepare': ['低脂巧克力100克', '全麥麵粉150克', '無糖可可粉50克', '橄欖油60克', '赤藻糖醇70克', '無鋁泡打粉5克', '雞蛋2個', '新鮮藍莓100克'], 'cookTime': '60', 'cookStep': ['將巧克力放入微波爐叮融，備用', '全麥麵粉、無糖可可粉和無鋁泡打粉過篩後，混合均勻', '將 雞蛋打入大碗中，加入橄欖油和赤藻糖醇一起打發', '將巧克力融液加入雞蛋油糖糊 中，拌勻', '分前將乾粉類慢慢加入巧克力糊中，邊翻邊拌', '拌至無粉顆粒後，放 入新鮮的藍莓，稍稍翻拌均勻後倒入已經舖好烘焙紙的模具中，平整表面', '將模具 放入已經預熱好的烤箱中，中層，上下火180度，烤45分鐘左右即可'], 'nutrition': '每份（100克）含碳水化合物68%，蛋白質15%，脂肪17%，纖維質10%。', 'diet': ['1']}, 'imagedescribe': '你現在看到的是一款地中海風味的巧克力蛋糕，主要食材有新鮮的巧克力、橄欖油和藍莓。這款蛋糕採用藍莓和橄欖油做裝飾，使整體顏色呈 現出豐富的層次感，營造出地中海的海洋風情。在健康與美味之間取得完美的平衡。 以綠色和藍色的色調搭配木紋桌面，營造出自然、清新的地中海氛圍。'}

#             title = json_data["recipe"]["title"]
#             summary = json_data["recipe"]["summary"]
#             prepare = json_data["recipe"]["prepare"]
#             cookTime = json_data["recipe"]["cookTime"]
#             cookStep = json_data["recipe"]["cookStep"]
#             nutrition = json_data["recipe"]["nutrition"]
#             diet = json_data["recipe"]["diet"]
#             imagedescribe = json_data["imagedescribe"]
            
#             cookStep_str = ', '.join(cookStep)
#             diet_str = ', '.join(diet)

#             json_data2 = {'prepareMoney': ['低脂巧克力100克：xxx元', '全麥麵粉150克：xxx元', '無糖可可粉50克：xxx元', '橄欖油60克：xxx元', '赤藻糖醇70克：xxx元', '無鋁泡打粉5 克：xxx元', '雞蛋2個：xxx元', '新鮮藍莓100克：xxx元'], 'total': 'XXX'}

#             prepareMoney = json_data2["prepareMoney"]
#             prepareMoney_str = ', '.join(prepareMoney)
#             total = json_data2["total"]

#             image_name = 'image2024-05-17-10-42-34.png'
            
#             # DB
#             # def db_insert():
#             #     conn = db.get_connection()
#             #     cursor = conn.cursor()
#             #     cursor.execute("INSERT INTO body.cookbook (\"Uid\", title, summary, \"prepare\", \"prepareMoney\", \"cookTime\", \"cookStep\", nutrition, diet, \"cookImage\", \"cookImageDescribe\", \"isPublish\", diet_req, main_req, nutrition_req, cook_time_req, special_diet_req, create_time, update_time) VALUES (1,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, '0', %s, %s, %s, %s, %s, %s, %s)",
#             #                         (title, summary, prepareMoney_str, total, cookTime, cookStep_str, nutrition, diet_str, image_name, imagedescribe, 'test', 'test', 'test', 'test', 'test', '2024-05-17', '2024-05-17'))
#             #     conn.commit()
#             #     conn.close()
            
#             # threading.Thread(target=db_insert).start()
#             current_date = datetime.now().strftime("%Y-%m-%d")

#             return render_template('/question/resultRecipe.html', data=json_data, data2=json_data2, image_name=image_name, Recipes_image_path=Recipes_image_path, current_time=current_date)
#         except Exception as e:
#             # 印出錯誤原因
#             print('-'*30)
#             print(e)
#             print('-'*30)        
#             # 渲染失敗畫面
#             return render_template('/question/resultRecipe.html', name=name)
#     return render_template('/question/resultRecipe.html', name=name)