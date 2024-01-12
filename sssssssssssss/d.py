from ha_sy import join_jamos, split_syllables
import pandas as pd
from openpyxl import Workbook
import random
import re

print('starting...')
print('reading DB....')
df = pd.read_excel('C:/Users/win/Downloads/sssssssssssss/Ndb.xlsx') #db엑셀 읽기
chin = 0
po = 0
file_path = 'C:/Users/win/Downloads/sssssssssssss/result_words3.txt'
file_path2 = 'C:/Users/win/Downloads/sssssssssssss/sdasd.txt'
ch_list1 = ['ㅏ','ㅐ','ㅗ','ㅚ','ㅜ','ㅡ'] #두음 1
ch_list2 = ['ㅑ','ㅕ','ㅖ','ㅛ','ㅠ','ㅣ'] #두음 2
ch_list3 = ['ㅕ','ㅛ','ㅠ','ㅣ'] #두음 3
use_word_list = []
player_win = 0
compter_win = 0

def change_rieul_to_nieun(word):
    try:
      if ")" in word:
        #print('cut')
        return '한방'
      else:
        jamos = extract_last_character(word) #끝글자 분리
        jamos = split_syllables(jamos)  # 단어를 자모 단위로 분리
        jamos_list = list(jamos)  # 자모 단위로 분리된 것을 리스트로 변환
        if jamos_list[1] in ch_list1 and jamos_list[0] == 'ㄹ':
          jamos_list[0] = 'ㄴ'
        elif (jamos_list[1] in ch_list2 and jamos_list[0] == 'ㄹ') or (jamos_list[1] in ch_list3 and jamos_list[0] == 'ㄴ'):
          jamos_list[0] = 'ㅇ'
        modified_word_sub = join_jamos(jamos_list)
        return modified_word_sub
    		#modified_word_sub = join_jamos(jamos_list)  # 변경된 자모들을 다시 합쳐 단어로 변환

    except IndexError:
       return None

    		#return modified_word_sub

def extract_last_character(text):
  if text:  # 입력된 텍스트가 비어있지 않은 경우
      last_character = text[-1]# 마지막 글자 추출
      return last_character
  else:
      return "입력된 텍스트가 없습니다."

def check_word_in_DB(word):
    try:
        if word in df['id'].values:    # 'id' 컬럼에 단어가 있는지 확인
            return True
        else:
            #print('사전에 없는 단어 입니다.')
            return False
    except Exception as e:
        #print(f"에러 발생: {e}")
        return False  # 예외 발생 시 False

def extract_first_character(text):
    if text:  # 입력된 텍스트가 비어있지 않은 경우
        first_character = text[0]  # 첫번째 글자 추출
        return first_character
    else:
        return "입력된 텍스트가 없습니다."

def start_word_rand(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            words = file.read().split()

            # 자음과 모음 패턴 정의 (한글 기준)
            pattern = re.compile("[^ㄱ-ㅎㅏ-ㅣ가-힣]+")

            # 자음과 모음을 제외한 단어들을 추출하여 리스트에 저장
            valid_words = [word for word in words if not pattern.search(word)]

            # 랜덤으로 단어 선택
            if valid_words:
                selected_word = random.choice(valid_words)
                return selected_word
            else:
                return "해당 파일에는 자음과 모음을 제외한 단어가 없습니다."

    except FileNotFoundError:
        return "파일을 찾을 수 없습니다."
    except Exception as e:
        return f"에러 발생: {e}"

def select_word(file_path, last_character, sub_last_character,chin):

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            words = file.read().split()

            # 선택된 단어들을 저장할 리스트
            selected_words = []
            onecut_words = []
            select_wordss = []
            all_onecut_words = []
            ect_words = []
            for word in words:
                if '(' in word :
                  all_onecut_words.append(word)
                else :
                   ect_words.append(word)
            #print(all_onecut_words)
            
            for word in all_onecut_words:
                if word.startswith(last_character) or word.startswith(sub_last_character):
                    onecut_words.append(word)
            for word in ect_words:
                if word.startswith(last_character) or word.startswith(sub_last_character):
                    select_wordss.append(word)
            #print(onecut_words)
            #print(select_wordss)
            #for word in words:
                # last_character 또는 sub_last_character로 시작하는 단어일 때
                #if word.startswith(last_character) or word.startswith(sub_last_character):
                    #select_wordss.append(word)
                    #if '한방' in word:
                      #if chin > 3:
                        #onecut_words.append(word)

                    #else:
                        # '한방'이 붙어있지 않은 경우 선
                        #selected_words.append(word)
            #print(select_wordss)
            #for word in select_wordss:
                #if ')' in word:
                  #onecut_words.append(word)
                #else :
                  #selected_words.append(word)
            #print(onecut_words)
            #print(selected_words)
            if not select_wordss:
                #print('s')
                return None

            
            if chin > 3 :
                if not onecut_words:
                    jjj = random.choice(select_wordss)
                    return jjj
                else :
                    jjj = random.choice(onecut_words)
                    return jjj
            else :
                jjj = random.choice(select_wordss)
                return jjj
               
            

            # 랜덤으로 선택된 단어 반환
            #if not onecut_words :
              #return random.choice(selected_words)
            #else :
              #return random.choice(onecut_words)



    except FileNotFoundError:
        return "파일을 찾을 수 없습니다."
    except Exception as e:
        return f"에러 발생: {e}"

def add_unique_word(word, word_list):
    if word in word_list:  # 입력한 단어가 이미 리스트에 있다면
        return '중복'
    else:  # 입력한 단어가 리스트에 없다면
        #word_list.append(word)
        return "suc"

def check_length(word):
    if len(word) == 1:  # 입력한 단어의 길이가 1이면
        return "one"
    else:  # 입력한 단어의 길이가 1보다 크면
        return "ok"

def print_last_sub(last_character,sub_last_character):
  if last_character == sub_last_character:
    print(f'>{last_character}')
    return True
  elif last_character == ')':
    print('(한방) 컴퓨터 win!')
    return 'OVER'
  elif last_character != sub_last_character :
    print(f'>{last_character}({sub_last_character})')
    return False
  elif last_character == '한방':
    print('(한방)')
    return 'OVER'

def extract_words_starting_with(letter):
    try:
        #df = pd.read_excel('Ndb.xlsx')  # 엑셀 파일 불러오기
        words = df[df['id'].str.startswith(letter)]['id'].tolist()

        return words  # 시작하는 단어들을 담은 리스트 반환

    except FileNotFoundError:
        return "파일을 찾을 수 없습니다."
    except Exception as e:
        return []


def possibility_word_check(word,word_list,chin,last_character):
  alphabet_list = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z','a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
  for char in alphabet_list:
    if char in word:
      print('다시 입력하십시오.')
      return False
  word_first = extract_first_character(word)
  sl = 0
  sub_last_character = change_rieul_to_nieun(last_character)
  if word_first == last_character or word_first == sub_last_character:
    sl += 1
  else:
    if last_character == sub_last_character :
      print(f'{last_character}로 시작하는 단어를 입력하세요.')
    else :
      print(f'{last_character}({sub_last_character})로 시작하는 단어를 입력하세요.')
    return False
  last_character = extract_last_character(word)
  sub_last_character = change_rieul_to_nieun(last_character)
  len_ch = check_length(word)
  if len_ch == 'one':
    print('두글자 이상을 입력하세요.')
    return False
  elif len_ch == 'ok':
    ch_db = check_word_in_DB(word)
    if ch_db == True:
      duplication_check =  add_unique_word(word,word_list)
      if duplication_check != '중복':
        if last_character == sub_last_character:
          sss = extract_words_starting_with(last_character)
          ssss = extract_words_starting_with(sub_last_character)
          if (not sss and not ssss) and chin >= 2 :
            print('플레이어의 승리')
            return 'LOSE'
          elif (not sss and not ssss)and chin < 2 :
            print(f'시작 한방 금지 <{word}>')
            return False
          else:
            return word
        elif last_character != sub_last_character:
          sss1 = extract_words_starting_with(last_character)
          sss2 = extract_words_starting_with(sub_last_character)
          if (not sss1 and not sss2) and chin >= 2 :
            print('플레이어의 승리')
            return 'LOSE'
          elif (not sss1 and not sss2) and chin < 2 :
            print(f'시작 한방 금지 <{word}>')
            return False
          else :
            return word
      else :
        print(f'<{word}>는 중복된 단어입니다.')
        return False
    else :
      print(f'<{word}>는 사전에 없는 단어 입니다.')
      return False
  else :
    return False



#main function
####
while True :
    chin = 0
    use_word_list = []
    po = 0
    last_character = start_word_rand(file_path)
    while True:
        if last_character == None:
            last_character = start_word_rand(file_path)
        else:
            sub_last_character = change_rieul_to_nieun(last_character)
            break
    if last_character == sub_last_character:
        print('시작 단어:',last_character)
    else :
        print(f'시작단어: {last_character}({sub_last_character})')
    while True :
        input_word = input('>>>')
        if input_word != 'ㅈㅈ' and input_word != 'off':
            check_check = possibility_word_check(input_word,use_word_list,chin,last_character)
        elif input_word == 'ㅈㅈ' :
            print('게임 종료')
            compter_win += 1
            break
        elif input_word == 'off' :
            break
        else :
            pass
        if check_check == False :
            pass
        elif check_check == 'LOSE' :
            player_win += 1
            break
        elif check_check == input_word :
            last_character = extract_last_character(input_word)
            sub_last_character = change_rieul_to_nieun(last_character)
            chin +=1
            print(chin)
            print_last_sub(last_character,sub_last_character)
            use_word_list.append(input_word)
            while True :
                compter_select_word = select_word(file_path2,last_character,sub_last_character,chin)
                com_duplication = add_unique_word(compter_select_word,use_word_list)
                if compter_select_word == None :
                    break
                elif po > 4 :
                    break
                elif com_duplication != '중복':
                    print('>>>',compter_select_word)
                    use_word_list.append(compter_select_word)
                    break
                elif com_duplication == '중복':
                    po += 1
            if compter_select_word == None and po > 4 :
                print('K')
                print('플레이어의 승리')
                player_win += 1
                break
            elif compter_select_word != None:
                last_character = extract_last_character(compter_select_word)
                sub_last_character = change_rieul_to_nieun(last_character)
                ck = print_last_sub(last_character,sub_last_character)
                if ck == 'OVER':
                    compter_win += 1
                    break
                chin += 1
                po = 0
                print(chin)
        else :
            pass
    win_rate_com = round(((compter_win/(compter_win + player_win))*100),3)
    win_rate_player = round(((player_win/(compter_win + player_win))*100),3)
    print('컴퓨터: {0}승 {1}패 ,승률 ,{2:.3f}%'.format(compter_win , (compter_win+player_win)-compter_win , win_rate_com))
    print('플레이어: {0}승 {1}패 ,승률 {2:.3f}%'.format(player_win , (compter_win+player_win)-player_win , win_rate_player))

    if input_word == 'off':
        break
    else:
        while True:
            wait = input()
            if wait == 'st' or wait == '시작' : break
            elif wait == 'off' : break
            else: pass
    if wait == 'off' : break
