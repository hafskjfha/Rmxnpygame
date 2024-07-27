from flask import Flask, render_template, request, jsonify
from d import Game

app = Flask(__name__)
game = Game()
# 스택을 전역 변수로 정의
stack = []
@app.route('/', methods=['GET','POST'])
def home():
    global stack
    stack = []
    return render_template('index.html')

@app.route('/stack', methods=['GET'])
def get_stack():
    return jsonify(stack)

@app.route('/submit', methods=['POST'])
def submit():
    if request.is_json:
        data = request.get_json()
        new_element = data.get('inputBox')
        if new_element:
            # 스택에 원소 추가, 최대 5개로 제한
            if len(stack) >= 4:
                stack.pop(0)
            stack.append(new_element)
            return jsonify({'success': True, 'stack': stack,"letter":f"{new_element[-1]}"})
        else:
            return jsonify({'error': 'No input provided'}), 400
    else:
        return jsonify({'error': 'Request must be JSON'}), 400


@app.route('/api/su',methods=['POST','GET'])
def check():
    if request.is_json:
        data = request.get_json()
        valu = data.get('inputBox')
        if valu in ('하이','쿵쾅'):
            return jsonify({"success": True})
        else:
            return jsonify({"success": False,"reason":'어쩔 ㅋ'})

@app.route('/api/com',methods=['POST',"GET"])
def com_sel_word():
    if 1==1:
        return jsonify({'word':'computer lose!','game':'userwin'})
        #return jsonify({'word':'이리듐','game':'comwin'})
    return jsonify({'word':'이러쿵저러쿵','game':'ing'})

@app.route('/api/st',methods=['GET','POST'])
def start_letter_ch():
    return jsonify({'letter':'하'})

if __name__ == '__main__':
    app.run(debug=True)
