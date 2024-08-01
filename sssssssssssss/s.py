from hangul_system import join_jamos, split_syllables
import os
from tqdm import tqdm
from typing import Tuple,List
current_dir = os.path.dirname(__file__)
id_file=os.path.join(current_dir, '.\\id_list (1).txt')
with open(id_file,'r',encoding='utf-8') as f:
  p=f.read().split()
jj=list(set([o[0] for o in p if o]))

ch_list1 = ['ㅏ','ㅐ','ㅗ','ㅚ','ㅜ','ㅡ'] #두음 1
ch_list2 = ['ㅑ','ㅕ','ㅖ','ㅛ','ㅠ','ㅣ'] #두음 2
ch_list3 = ['ㅕ','ㅛ','ㅠ','ㅣ'] #두음 3

def change_rieul_to_nieun(word):
    try:
      jamos = split_syllables(word)  # 단어를 자모 단위로 분리
      jamos_list = list(jamos)  # 자모 단위로 분리된 것을 리스트로 변환
      if jamos_list[1] in ch_list1 and jamos_list[0] == 'ㄹ':
        jamos_list[0] = 'ㄴ'
      elif (jamos_list[1] in ch_list2 and jamos_list[0] == 'ㄹ') or (jamos_list[1] in ch_list3 and jamos_list[0] == 'ㄴ'):
        jamos_list[0] = 'ㅇ'
      modified_word_sub = join_jamos(jamos_list)
      return modified_word_sub

    except IndexError:
       return word

def revers_duem(letter:str) -> Tuple[str]:
    """
    글자를 역으로 두음법칙화 시켜 반환 합니다.

    입력:
    letter <str> :  역두음법칙을 시킬 글자

    반환:
    revers_letters <tuple> :원래 글자,역두음법칙이 적용된 글자들

    예시:
    >>>Find_word._revers_duem('역')

    ('역','력','녁')

    >>>Find_word._revers_duem('는')

    ('는','른')
    """
    duem_list1:List[str] = ch_list1
    duem_list2:List[str] = ch_list2
    duem_list3:List[str] = ch_list3

    jamos_list:List[str] = list(split_syllables(letter))
    revers_duem_letter:List[str] = [letter]
    if len(jamos_list) < 2:
      return letter
    else:
      if jamos_list[0] == 'ㄴ' and jamos_list[1] in duem_list1:
        jamos_list[0] = 'ㄹ'
        i_letter:str = join_jamos(jamos_list)
        revers_duem_letter.append(i_letter)
        jamos_list[0] = 'ㄴ'
      if jamos_list[0] == 'ㅇ' and jamos_list[1] in duem_list2:
        jamos_list[0] = 'ㄹ'
        i_letter:str = join_jamos(jamos_list)
        revers_duem_letter.append(i_letter)
        jamos_list[0] = 'ㅇ'
      if jamos_list[0] == 'ㅇ' and jamos_list[1] in duem_list3:
        jamos_list[0] = 'ㄴ'
        i_letter:str = join_jamos(jamos_list)
        revers_duem_letter.append(i_letter)
        jamos_list[0] = 'ㅇ'

      return tuple(revers_duem_letter)
sb=[]
#print(jj[:10])
# for k in tqdm(jj):
#   m=revers_duem(k)
#   yy=[]
#   n=[h for h in p if h[0] in m]
#   if n:
#     sb.extend(m)
# sb=list(set(sb))
# with open('start_letters.txt','w',encoding='utf-8') as wf:
#   wf.write('\n'.join(sb))
# bb=os.path.join(current_dir, '.\\not_onecut_letter.txt')
# with open(bb,'w',encoding='utf-8')as wf:
#   sb.sort()
#   wf.write('\n'.join(sb))
#print(revers_duem('잇'))