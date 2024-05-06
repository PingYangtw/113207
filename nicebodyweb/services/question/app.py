# 匯入Blueprint模組
from flask import render_template
from flask import Blueprint

# 產生問題服務藍圖
question_bp = Blueprint('question_bp', __name__)

#--------------------------
# 在問題服務藍圖加入路由
#--------------------------

#問題一
@question_bp.route('/question_n1')
def question1_selfList(): 
    return render_template('/question/question_n1.html', data='王小明')

#問題二
@question_bp.route('/question_n2')
def question2_selfList(): 
    return render_template('/question/question_n2.html', data='王小明')

#問題三
@question_bp.route('/question_n3')
def question3_selfList(): 
    return render_template('/question/question_n3.html', data='王小明')

#問題三-一
@question_bp.route('/question_n3_1')
def question3_1_selfList(): 
    return render_template('/question/question_n3_1.html', data='王小明')

#問題四
@question_bp.route('/question_n4')
def question4_selfList(): 
    return render_template('/question/question_n4.html', data='王小明')

#問題五
@question_bp.route('/question_n5')
def question5_selfList(): 
    return render_template('/question/question_n5.html', data='王小明')