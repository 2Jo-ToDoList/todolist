from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)

# 데이터베이스 기본설정
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, 'todolist.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# 데이터베이스 모델정의
class ToDo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    todo = db.Column(db.String(200), nullable=False)  # 할일
    date = db.Column(db.Date, nullable=False)  # 날짜
    completed = db.Column(db.Boolean, default=False,
                          nullable=False)  # 완료 여부 체크

    def __repr__(self):
        return f'<ToDo {self.todo}>'


# 데이터베이스 테이블 생성
with app.app_context():
    db.create_all()


# 기본 홈 화면
@app.route('/')
def home():
    todo_list = ToDo.query.all()
    return render_template('todo.html', data=todo_list)

# 할 일 추가
@app.route('/todo', methods=['POST'])
def todo_create():
    todo_content = request.form.get('todo')
    date = request.form.get('date')
    if todo_content and date:
        new_todo = ToDo(todo=todo_content,
                        date=datetime.strptime(date, '%Y-%m-%d'))
        db.session.add(new_todo)
        db.session.commit()
    return redirect(url_for('home'))

# 체크박스 체크여부따라 completed값 변경
@app.route('/update_todo_status', methods=['POST'])
def update_todo_status():
    # id와 체크여부 값 받기
    todo_id = request.form.get('id')
    isChecked = request.form.get('isChecked')

    # 체크여부에 따라 값 대입
    isChecked = isChecked == 'true'

    #
    todo = ToDo.query.get(todo_id)
    todo.completed = isChecked
    db.session.commit()
    return redirect(url_for('home'))

# 일정 삭제
@app.route('/delete')
def todo_delete():
    todo_msg_receive = request.args.get("todo_msg")
    if todo_msg_receive:
        todo_list = ToDo.query.get(todo_msg_receive)
        if todo_list:
            db.session.delete(todo_list)
            db.session.commit()

    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
