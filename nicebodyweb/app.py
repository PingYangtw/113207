#-----------------------
# 匯入模組
#-----------------------
from flask import Flask, render_template 

#-----------------------
# 匯入各個服務藍圖
#-----------------------
from services.robott.app import robott_bp
from services.question.app import question_bp

#-------------------------
# 產生主程式, 加入主畫面
#-------------------------
app = Flask(__name__)

#主畫面
@app.route('/')
def index():
    return render_template('/home/home.html') 

#主畫面
@app.route('/json-data')
def json_data():
    data = [{
        "recipe": {
            "title": "番茄蛋減糖魔法餐",
            "summary": "「番茄蛋糖減魔法餐」是一道精心設計的午餐，以減糖為主要特色，主要以新鮮的番茄和有機蛋為食材，烹飪時間僅需30分鐘以內。這道料理不僅美味清新，更符合營養需求，提供豐富的蛋白質，適量的脂肪，並極低的糖分。橄欖油的加入使得整體口感更加豐富。每份約含250卡路里，是一款輕盈無負擔的午餐選擇，滿足味蕾的同時也保證營養均衡。「番茄蛋糖減魔法餐」，讓您在享受美味的同時輕鬆追求減糖生活。",
            "prepare": [
            "新鮮番茄2顆",
            "有機蛋4顆",
            "新鮮香菜1把，切碎",
            "橄欖油2湯匙",
            "鹽和胡椒調味"
            ],
            "cookTime": "0~30分鐘",
            "cookStep": [
            "將番茄切成小丁狀備用。",
            "在鍋中用橄欖油加熱，加入切碎的番茄煮至軟爛。",
            "打入蛋，蓋上鍋蓋，用中小火蒸煮約5分鐘，直到蛋白凝固，但蛋黃仍然微嫩。",
            "撒上切碎的香菜，撒上適量的鹽和胡椒調味。",
            "輕輕攪拌混合，即可上桌享用。"
            ],
            "nutrition": "每份熱量約250卡路里，蛋白質豐富，脂肪含量適中，糖分極低，是一道減糖又營養豐富的午餐選擇。"
        }
    }]

    return render_template('/json-data.html',  data=data) 

#-------------------------
# 在主程式註冊各個服務
#-------------------------
app.register_blueprint(robott_bp, url_prefix='/robott')
app.register_blueprint(question_bp, url_prefix='/question')

#-------------------------
# 啟動主程式
#-------------------------
if __name__ == '__main__':
    app.run(port=5000, debug=True)