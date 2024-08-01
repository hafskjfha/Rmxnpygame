from flask import Flask, render_template, request, jsonify, send_file
from d import Game
from collections import deque
import os

current_dir = os.path.dirname(__file__)

app = Flask(__name__)
game = Game()
# 스택을 전역 변수로 정의
stack = deque()
letterK=''
sub_letterK=''
@app.route('/', methods=['GET','POST'])
def home():
    global stack,game
    stack = deque()
    game.chin=0
    return render_template('index.html')

@app.route('/stack', methods=['GET'])
def get_stack():
    return jsonify(list(stack))

@app.route('/submit', methods=['POST'])
def submit():
    global letterK,sub_letterK
    if request.is_json:
        data = request.get_json()
        new_element = data.get('inputBox')
        if new_element:
            # 스택에 원소 추가, 최대 4개로 제한
            if len(stack) >= 4:
                stack.pop()
            stack.appendleft(new_element)
            if (k:=game.duem(new_element[-1]))!=new_element[-1]:
                letterK=new_element[-1]
                game.used_words.add(new_element)
                sub_letterK=k
                return jsonify({'success': True, 'stack': list(stack),"letter":f"{new_element[-1]}({k})",'chin':game.chin})
            else:
                letterK=new_element[-1]
                game.used_words.add(new_element)
                sub_letterK=letterK
                return jsonify({'success': True, 'stack': list(stack),"letter":f"{new_element[-1]}",'chin':game.chin})
        else:
            return jsonify({'error': 'No input provided'}), 400
    else:
        return jsonify({'error': 'Request must be JSON'}), 400


@app.route('/api/su',methods=['POST','GET'])
def check():
    global letterK,sub_letterK
    if request.is_json:
        data = request.get_json()
        valu:str = data.get('inputBox')
        if valu[0] not in (letterK,sub_letterK):
            return jsonify({"success": False,"reason":''})
        k=game.check_word_len(valu)
        if k=='5x':
            return jsonify({"success": False,"reason":'한글자 금지'})
        k=game.check_word_in_db(valu)
        if k=='3x':
            return jsonify({"success": False,"reason":'사전에 없음'})
        k=game.word_used(valu)
        if k=='4x':
            return jsonify({"success": False,"reason":'이미 사용한 단어'})
        k=game.check_start_kill(valu)
        if k=='6x':
            return jsonify({"success": False,"reason":'시작 한방 금지'})
        game.chin+=1
        return jsonify({"success": True})



@app.route('/api/com',methods=['POST',"GET"])
def com_sel_word():
    global letterK,sub_letterK
    com_word,statez=game.com_select_word(letterK,sub_letterK)
    if statez=='user_win':
        return jsonify({'word':'computer lose!','game':'userwin'})
    elif statez=='com_win':
        return jsonify({'word':f'{com_word}','game':'comwin'})
    return jsonify({'word':f'{com_word}','game':'ing','chin':game.chin})

@app.route('/api/st',methods=['GET','POST'])
def start_letter_ch():
    global letterK,sub_letterK,stack
    game.chin=0
    game.used_words=set()
    stack=deque()
    letterz='니'#game.start_word_rand()
    sub_letterz=game.duem(letterz)
    if letterz==sub_letterz:
        letterK=letterz
        sub_letterK=letterK
        return jsonify({'letter':letterz})
    else:
        letterK=letterz
        sub_letterK=sub_letterz
        return jsonify({'letter':f'{letterz}({sub_letterz})'})

@app.route('/img/blue.png')
def get_image():
    # 이미지 파일 경로
    image_path = os.path.join(current_dir, '.\\img\\blue.png')
    return send_file(image_path, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
