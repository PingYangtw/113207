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