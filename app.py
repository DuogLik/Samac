from flask import Flask, render_template, request, redirect, url_for, session
import csv
from datetime import datetime
import os
import subprocess

app = Flask(__name__)
app.secret_key = 'secret_key'

questions = [
    {
        'question': '1. Sa mạc lớn nhất thế giới là gì?',
        'options': ['A. Sahara', 'B. Gobi'],
        'answer': 'A'
    },
    {
        'question': '2. Cây nào phổ biến ở sa mạc?',
        'options': ['A. Cây thông🌲', 'B. Xương rồng🌵'],
        'answer': 'B'
    },
    {
        'question': '3. Loài động vật nào có khả năng sống lâu không có nước?',
        'options': ['A. Lạc đà🐪', 'B. Chó🐶😂'],
        'answer': 'A'
    },
    {
        'question': '4. Hôm nay của chị thế nào?🤗',
        'options': ['A. Chị được tặng quà nè🎁', 'B. Chị nhớ đến em😘😎😊😍'],
        'answer': 'B'
    },
    {
        'question': '5. Chị có thấy thú vị ko?',
        'options': ['A. Trẻ con😢', 'B. Cũng hay (và chị thích nó)😊'],
        'answer': 'B'
    },
    {
        'question': '6. Em là ng rất thích lắng nghe nên có j chị cứ nói với em nhé💗',
        'options': ['A. Chị ko thích (Chị rất bận)😞', 'B. Chị sẽ cân nhắc🥳'],
        'answer': 'B'
    },
]

# Hàm lưu tất cả các lựa chọn vào file CSV
def save_results_to_csv(answers, start_time):
    filename = 'game_results.csv'
    start_time_str = start_time.strftime('%Y-%m-%d %H:%M:%S')

    with open(filename, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if file.tell() == 0:
            # Ghi tiêu đề cột nếu file trống
            writer.writerow(['Câu hỏi', 'Câu trả lời đã chọn', 'Câu trả lời đúng', 'Kết quả', 'Thời gian'])

        for answer in answers:
            writer.writerow([
                answer['question'], 
                answer['selected_answer'], 
                answer['correct_answer'], 
                'Đúng' if answer['selected_answer'] == answer['correct_answer'] else 'Sai',
                start_time_str
            ])
    
    # Đẩy file CSV lên GitHub
    push_to_github()

def push_to_github():
    # Chuyển đến thư mục chứa repo của bạn
    os.chdir('/path/to/your/repo')  # Đường dẫn đến thư mục chứa repo

    # Thực hiện các lệnh git để commit và push
    subprocess.call(['git', 'add', 'game_results.csv'])
    subprocess.call(['git', 'commit', '-m', 'Update game results'])
    subprocess.call(['git', 'push'])

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'question_index' not in session:
        session['question_index'] = 0
        session['answers'] = []  # Lưu tất cả câu trả lời
        session['start_time'] = datetime.now()  # Lưu thời gian bắt đầu

    question_index = session['question_index']
    message = None

    if request.method == 'POST':
        selected_answer = request.form['answer']
        
        # Lưu câu trả lời đã chọn (dù đúng hay sai)
        session['answers'].append({
            'question': questions[question_index]['question'],
            'selected_answer': selected_answer,
            'correct_answer': questions[question_index]['answer']
        })

        # Ghi lại ngay câu trả lời vào CSV (kể cả đúng hay sai)
        save_results_to_csv([{
            'question': questions[question_index]['question'],
            'selected_answer': selected_answer,
            'correct_answer': questions[question_index]['answer']
        }], session['start_time'])

        # Kiểm tra đáp án
        if selected_answer == questions[question_index]['answer']:
            session['question_index'] += 1
            if session['question_index'] >= len(questions):  # Hết câu hỏi
                return redirect(url_for('result'))
        else:
            message = 'Sai òi! Thử lại nào🍀'

    return render_template('index.html', question=questions[session['question_index']], message=message)

@app.route('/result')
def result():
    session.pop('question_index', None)  # Reset chỉ số câu hỏi
    return render_template('result.html')

if __name__ == '__main__':
    app.run(debug=True)
