import pygame
import sys
from pygame.locals import *
import logging
# 로깅 설정
#logging.basicConfig(level=logging.INFO, filename='game_log.txt', filemode='a', format='%(asctime)s - %(message)s')
logging.basicConfig(level=logging.INFO, filename='game_log.txt', filemode='a', format='%(asctime)s - %(levelname)s - %(message)s')


# Pygame 초기화
pygame.init()

# 창 설정
screen_width = 640
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))

# 색상 정의
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# 폰트 설정
def load_font(font_name, size):
    try:
        font = pygame.font.Font(font_name, size)
    except FileNotFoundError:
        print("폰트 파일을 찾을 수 없습니다.")
        font = pygame.font.SysFont(None, size)
    return font

# 기본 폰트 설정
#my_font = pygame.font.Font(None, 24)  # 기본 폰트
my_font = load_font('NanumGothic.ttf', 24)
# 텍스트 입력 및 시간 바 그리기 함수
def draw_text(text, font, surface, x, y):
    text_obj = font.render(text, True, WHITE)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)

# 시간 관리
clock = pygame.time.Clock()
time_limit = 10  # 시간 제한 (초)

# 게임 루프
running = True
input_text = ''
start_ticks = pygame.time.get_ticks()  # 타이머 시작

while running:
    screen.fill(BLACK)

    # 이벤트 처리
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            logging.info(f'key: {event.key}, text: {input_text}')
            if event.key == K_RETURN:
                draw_text(input_text, my_font, screen, screen_width / 2+90, screen_height / 2 )
                print(input_text)  # 입력된 텍스트 처리
                input_text = ''  # 텍스트 초기화
                start_ticks = pygame.time.get_ticks()
            elif event.key == K_BACKSPACE:
                input_text = input_text[:-1]
            else:
                input_text += event.unicode
    #draw_text('ddd', my_font, screen, screen_width / 2+30, screen_height / 2+30 )
    # 입력창 중앙에 표시
    draw_text(f"입력: {input_text}", my_font, screen, screen_width / 2, screen_height / 2)

    # 시간 바 그리기
    elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000  # 경과 시간 계산 (초)
    time_left = max(0, time_limit - elapsed_time)  # 남은 시간
    time_bar_width = (time_left / time_limit) * 200  # 시간 바 너비
    pygame.draw.rect(screen, RED, (screen_width / 2 - 100, screen_height / 2 + 30, time_bar_width, 20))

    if time_left == 0:
        draw_text("시간 초과! 패배하셨습니다.", my_font, screen, screen_width / 2, screen_height / 2 + 60)
        running = False

    pygame.display.flip()
    clock.tick(30)  # 초당 프레임 수

pygame.time.wait(2000)  # 2초간 대기 후 종료
pygame.quit()
