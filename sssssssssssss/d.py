from hangul_system import join_jamos, split_syllables
import re,sys,os,random
from typing import Set,List,Dict,Tuple

current_dir = os.path.dirname(__file__)
id_file=os.path.join(current_dir, '.\\id_list (1).txt')
print('starting...')
print('reading DB....')
po = 0
start_letter_file = os.path.join(current_dir, '.\\start_letters.txt')#'시작 글자 모음'
not_onecut_letter_file=os.path.join(current_dir, '.\\not_onecut_letter.txt')#한방 글자가 아닌 것 모음
com_word_file =os.path.join(current_dir, '.\\sdasd.txt') #'컴퓨터 단어 db'
player_win = 0
compter_win = 0

class Game:
    def __init__(self) -> None:
        self.ch_list1 = ['ㅏ','ㅐ','ㅗ','ㅚ','ㅜ','ㅡ'] #두음 1
        self.ch_list2 = ['ㅑ','ㅕ','ㅖ','ㅛ','ㅠ','ㅣ'] #두음 2
        self.ch_list3 = ['ㅕ','ㅛ','ㅠ','ㅣ'] #두음 3
        with open(id_file,'r',encoding='utf-8') as f:
          self.DB=set(f.read().split())
        with open(start_letter_file,'r',encoding='utf-8') as f:
          self.start_letters = f.read().split()
        self.set_start_letters=set(self.start_letters)
        with open(com_word_file,'r',encoding='utf-8') as f:
          self.com_word_db = f.read().split()
        with open(not_onecut_letter_file,'r',encoding='utf-8') as f:
          self.not_onecut=f.read().split()
        self.used_words=set()
        self.chin=0
    
    def duem(self,letter:str) -> str:
      """
      두음법칙 함수 입니다.

      Arguments:
        letter: 두음 법칙될 글자 

      Return:
        str: 두음 법칙된 글자
      """
      try:
        jamos:str = split_syllables(letter)
        jamos_list:List[str]=list(jamos)
        if jamos_list[1] in self.ch_list1 and jamos_list[0]=='ㄹ':
          jamos_list[0]='ㄴ'
        elif (jamos_list[1] in self.ch_list2 and jamos_list[0]=='ㄹ') or (jamos_list[1] in self.ch_list3 and jamos_list[0]=='ㄴ') :
          jamos_list[0]='ㅇ'
        modified_word_sub:str = join_jamos(jamos_list)
        return modified_word_sub
        
      except:
        return letter
      
    def extract_last_character(self,text:str) -> str:
      """
      끝글자 추출하는 함수

      Arguments:
        text: 추출할 글자
      
      Return:
        str:추출된 글자
      """
      if text:
        last_character:str=text[-1]
        return last_character
      else:
        return None
    
    def extract_first_character(self,text:str)->str:
      """
      앞글자 추출하는 함수

      Arguments:
        text: 추출할 글자

      Return :
        str 추출된 글자
      """
      if text:
        return text[0]
      else:
        return None

    def check_word_in_db(self,word:str) -> str:
      """
      단어가 사전에 있는 단어인지 검사하는 함수

      Arguments:
        word: 검사할 단어

      Return:
        사전에 있는가?
        True : 3y
        False : 3x
      """
      try:
          if word in self.DB:
            return '3y'
          else:
            return '3x'
      except:
        return None
            
    def start_word_rand(self)->str:
      """
      시작 단어 추출함수

      Return :
        str : 시작 글자
      """
      pattern = re.compile("[^ㄱ-ㅎㅏ-ㅣ가-힣]+")
      valid_words:List[str] = [word for word in self.start_letters if not pattern.search(word)]
      if valid_words:
        return random.choice(valid_words)
      else:
        return None

    def word_used(self,word:str)->str:
      """
      해당 단어가 사용된적 있는지 검사하는 함수

      Arguments:
        word: 검사할 단어

      Return :
        사용된적 있나?
        True : 4x
        False : 4y
      """
      if word in self.used_words:
        return '4x'
      else:
        return '4y'

    def check_word_len(self,word:str)->str:
      """
      한글자인지 확인 하는 함수

      Arguments:
        word: 검사할 단어

      Return :
        1글자 인가?
        True: 5x
        False : 5y
      """
      if len(word)>1:
        return '5y'
      else:
        return '5x'

    def com_select_word(self,last_character:str, sub_last_character:str)->Tuple[str]:
      """
      컴퓨터가 단어를 선택하는 함수

      Arguments:
        last_character: 이어야 하는 글자
        sub_last_character: 이어야 하는 글자 (두음법칙 된거)

      Retrun:
        튜플 ('컴퓨터가 사용할 단어','게임 상태'):
          컴퓨터가 이을 단어가 없다: ('','user_win')
          컴퓨터가 한방 단어를 사용해 승리하였다: ('단어','com_win')
          컴퓨터가 일반 단어를 사용하였다: ('단어','ing')
      """
      sel_words=[word for word in self.com_word_db if word[0] in (last_character,sub_last_character) and word not in self.used_words]
      if not sel_words:
        return ('','user_win')
      if self.chin>3:
        onecut=[word for word in sel_words if word[-1] not in self.not_onecut]
        if onecut:
          return (random.choice(onecut),'com_win')
        else:
          self.chin+=1
          k=random.choice(sel_words)
          self.used_words.add(k)
          return (k,'ing')
      else:
        self.chin+=1
        k=random.choice(sel_words)
        self.used_words.add(k)
        return (k,'ing')
      
    def check_start_kill(self,word:str)->str:
      """
      시작 한방 인지 확인하는 함수

      Arguments:
        word : 시작한방인지 검사할 단어

      Return:
        str(bool)
        시작한방 아님: 6y
        시작한방 맞음: 6x
      """
      if self.chin>1:
        return '6y'
      else:
        sub=self.duem(word[-1])
        if word[-1] in self.not_onecut or sub in self.not_onecut:
          return '6y'
        return '6x'



"""

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


"""
#main function
####
"""while True :
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
            sys.exit()
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
    if wait == 'off' : break"""