import pygame
import pygame.mixer
import asyncio
import time
import io
import datetime
import json
import random
import os
import sys
import websockets
import chardet
from game.sprite import characters
from game.sprite import skills
from game.sprite import tiles
from game.sprite import ui
from game.dataload import *
from game.transitions import *
from urllib.request import urlopen
from PIL import Image, ImageDraw
import numpy as np
#import unicode


# 0:초기화 / 1:다음 게임 준비 / 2: 게임 시작 / 3: 플레이 / 4: 게임 종료
GAME_STATE_INIT = 0
GAME_STATE_READY = 1
GAME_STATE_START = 2
GAME_STATE_PLAYING = 3
GAME_STATE_OVER = 4


FPS = 60

# 스크린 전체 크기 지정
#SCREEN_WIDTH = 598
SCREEN_WIDTH = 570
SCREEN_HEIGHT = 1060


# second setting
# SCREEN_WIDTH = 475
# SCREEN_HEIGHT = 844
# first setting
#SCREEN_WIDTH = 575
#SCREEN_HEIGHT = 944

LAND_TOP_HEIGHT = SCREEN_HEIGHT * 0.5
LAND_BOTTOM_HEIGHT = LAND_TOP_HEIGHT + 179

LEFT_CASTLE_POSITION = (-18, LAND_TOP_HEIGHT)
RIGHT_CASTLE_POSITION = (SCREEN_WIDTH - 85, LAND_TOP_HEIGHT)

LEFT_SPAWN_POSITION = (SCREEN_WIDTH * 0.01, LAND_TOP_HEIGHT + 100)
RIGHT_SPAWN_POSITION = (SCREEN_WIDTH - (SCREEN_WIDTH * 0.07), LAND_TOP_HEIGHT + 100)

LOG_POSITION = (SCREEN_WIDTH * 0.6, SCREEN_HEIGHT * 0.4)

MAX_SKILL_COUNT = 5

# 커스텀 이벤트 생성
EVENT_SOCKET_MSG = pygame.USEREVENT+1

# socket msg code
MSG_CODE_COMMENT = 1
MSG_CODE_LIKE = 2
MSG_CODE_DONATION = 3
MSG_CODE_SHARE = 4
MSG_CODE_SET_CANDIDATES = 5
MSG_CODE_NOTICE = 6

# 게임 플레이 설정
SPRITE_TYPE_CHARACTER = 1
SPRITE_TYPE_STRUCTURE = 2
SPRITE_TYPE_SKILL = 3

class Game:
    def __init__(self):
        # 게임 초기화
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption("TIKTOK WAR GAME")        

        #print(pygame.font.get_fonts())  # 사용 가능한 시스템 폰트 목록 출력 - 한글 지원x
        
        # 상태 변수 설정
        # ready
        self.is_end_ready_animation = False
        self.is_rank_updated = False
        self.is_set_candidate = False 
        self.is_set_tiles = False
        self.is_set_castle = False  
        # start
        self.is_set_timer = False
        # over
        self.is_end_over_animation = False
        self.is_update_rank = False
        self.is_clear_game_data = False
        
        self.state = GAME_STATE_INIT
        
        # 게임 결과 변수
        self.is_draw = False
        self.draw_result = False
        self.winner = None
        self.loser = None

        # 게임 환경 설정
        self.SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) #화면 크기 설정
        #self.SCREEN_SURFACE = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock() 
        self.FPS = FPS
        self.COLOR_BLUE = (24, 154, 211)
        self.COLOR_BLACK = (0, 0, 0)
        self.COLOR_WHITE = (255, 255, 255)
        self.COLOR_YELLOW = (255, 228, 0)
        self.COLOR_BLUE_LIGHT = (103, 153, 255)
        self.COLOR_BLUE_DEEP = (1, 0, 255)
        self.COLOR_BLUE_DARK = (0, 34, 102)
        self.COLOR_GREEN_LIGHT = (183, 240, 177)
        self.COLOR_RED_LIGHT = (255, 167, 167)
        self.COLOR_GREY_LIGHT = (213, 213, 213)
        self.COLOR_PURPLE = (95, 0, 255)
        self.main_font_60 = pygame.font.Font("game/res/font/NanumBarunGothic.ttf", 60)
        self.main_font_30 = pygame.font.Font("game/res/font/NanumBarunGothic.ttf", 30)   
        self.main_font_20 = pygame.font.Font("game/res/font/NanumBarunGothic.ttf", 20) 
        self.main_font_15 = pygame.font.Font("game/res/font/NanumBarunGothic.ttf", 15) 
        self.main_font_14 = pygame.font.Font("game/res/font/NanumBarunGothic.ttf", 14) 
        self.main_font_13 = pygame.font.Font("game/res/font/NanumBarunGothic.ttf", 13) 
        self.main_font_11 = pygame.font.Font("game/res/font/NanumBarunGothic.ttf", 11)

        self.main_bold_font_14 = pygame.font.Font("game/res/font/NanumBarunGothicBold.ttf", 14) 
        self.main_bold_font_13 = pygame.font.Font("game/res/font/NanumBarunGothicBold.ttf", 13) 

        self.arialbd_font_13 = pygame.font.Font("game/res/font/arialbd.ttf", 13) 
        

        self.sebang_font_30_bold = pygame.font.Font("game/res/font/SEBANGGothicBold.ttf", 30)
        #text = main_font.render("Test Text", True, COLOR_BLACK)     # 문자열, antialias, 글자색
        
        self.message_queue = []     # 웹소켓 전송 메시지큐
        self.join_queue = []        # 게임 참여 큐
        self.donation_queue = []    # 도네이션 큐
        self.notice_queue = []    # 공지사항 큐
        
        ### 시간 관련 변수 ###
        self.auto_player_spawn_term = 500 # 160      자동 플레이어 생성 주기
        self.auto_player_spawn_time = 0   #          자동 플레이어 생성 딜레이 시간
        self.game_timer_term = 60 * 7     # 게임 플레이 제한 시간 - 240초 => 4분
        self.notice_term = 5              # 공지 노출 시간(단위:s)
        self.notice_time = 0              # 현재 공지 노출된 시간 

        # sprite group 설정
        self.sprite_group = pygame.sprite.Group()
        self.left_group = pygame.sprite.Group()
        self.right_group = pygame.sprite.Group()
        self.skill_group = pygame.sprite.Group()
        self.tile_group = pygame.sprite.Group()
        self.ui_group = pygame.sprite.Group()

        self.tile_size = (50, 50)
        self.menu_size = ((SCREEN_WIDTH / MAX_SKILL_COUNT) * 0.7, (SCREEN_WIDTH / MAX_SKILL_COUNT) * 0.7)
        #self.menu_size = (150, 150)
        self.donation_size = (SCREEN_WIDTH / 7, SCREEN_WIDTH / 7)
        self.profile_size = (SCREEN_WIDTH / 25, SCREEN_WIDTH / 25)
        self.log_profile_size = (SCREEN_WIDTH / 50, SCREEN_WIDTH / 50)
        self.soldier_size = (60, 60)
        self.knight_size = (90, 90)
        self.lightning_size = (100, 268)
        self.devil_size = (400, 400)
        self.castle_size = (100, 180)


        # 리소스 불러오기
        import_soldier_left(self.soldier_size)
        import_soldier_right(self.soldier_size)

        import_knight_right(self.knight_size)
        import_knight_left(self.knight_size)

        import_lightning_images(self.lightning_size)
        import_devil_images(self.devil_size)

        import_castle_left(self.castle_size)
        import_castle_right(self.castle_size)

        import_ground_images(self.tile_size)
        

        # 효과음 로드
        self.sound_map = import_sound()
       

        # skill 로드
        self.skills = []
        f = open("game/data/skills.txt", 'r', encoding='UTF-8')
        while True:
            line = f.readline()
            if not line: break            
            obj = json.loads(line)
            self.skills.append(obj)
        import_menu_images(self.menu_size, self.skills)
        print("[[ Complete load skills data. ]]")    
        f.close()



        # 대결 후보 리스트 로드
        self.candidates = []
        f = open("game/data/city.txt", 'r', encoding='UTF-8')
        while True:
            line = f.readline()
            if not line: break            
            self.candidates.append(line.replace('\n', ''))
        print("[[ Complete load cnadidates data. ]]")
        #print(self.candidates)
        f.close()


        # 랭킹 정보 로드
        self.rank_list = []
        self.rank = {}
        f = open("game/data/city_rank.txt", 'r', encoding='UTF-8')
        while True:
            line = f.readline()
            if not line: break            
            obj = json.loads(line)
            self.rank[obj.get('name')] = obj            
            #print("[LOAD RANK]: %s => %d %d " % (obj.get('name'), obj.get('win'), obj.get('lose')))
        print("[[ Complete load rank data. ]]")
        #print(self.rank)
        f.close()      


        # 게임 플레이 변수
        self.join_map = {}
        self.left_name = ""
        self.right_name = ""
        self.now_notice = None
        self.donation_state = True
        self.notice_state = True
        self.destroyed_castle = None    # 파괴된 성


        self.invalid_join_cnt = 0       # 현재 경기 진행중이지 않은 지역을 계속해서 입력하는 경우의 수
        self.none_join_like_cnt = 0     # 참가 하지않고 좋아요만 누른 경우의 수
        self.duplicate_join_cnt = 0     # 참가 메시지를 계속해서 입력하는 경우의 수
        self.invalid_join_limit = 10
        self.none_join_like_limit = 10
        self.duplicate_join_limit = 10

        self.state = GAME_STATE_READY
        print("[[ END INIT GAME ]]")

   

    async def animation(self):
       
        auto_player_num = 0
        current_time = 0
        while True:
            #print('animation')
            last_time, current_time = current_time, time.time()
            await asyncio.sleep(1 / FPS - (current_time - last_time))  # tick
            
            mt = self.clock.tick(FPS) / 1000 # 1000을 나누어줘서 초단위로 변경하여 반환
            
            # ================================== READY ==================================
            if self.state == GAME_STATE_READY:
                
                            
                # 다음 게임 안내 애니메이션
                #   - < ㅁㅁ vs ㅁㅁ >  => 이와 유사하게 애니메이션 연출

                # 순위 업데이트
                if self.is_rank_updated == False:
                    self.update_rank()
                    self.is_rank_updated = True

                # 대결 지역 선정 - 메모리에서 가져다가 사용한다.
                # 랜덤 함수 사용                 
                if self.is_set_candidate == False:
                    tmp_arr = list(range(len(self.candidates)))
                    left_idx = random.randint(0, len(tmp_arr) - 1)
                    self.left_name = self.candidates[left_idx]
                    del tmp_arr[left_idx]

                    right_idx = random.randint(0, len(tmp_arr) - 1)
                    self.right_name = self.candidates[right_idx]
                    del tmp_arr[right_idx]

                    if self.left_name == self.right_name:
                        continue

                    json_obj = {
                        "code": MSG_CODE_SET_CANDIDATES,
                        "left_name": self.left_name,
                        "right_name": self.right_name
                    }
                    json_str = json.dumps(json_obj, ensure_ascii=False)
                    self.message_queue.append(json_str)

                    self.is_set_candidate = True
                    print("[[ Set Candidates ]]")


                if self.is_set_tiles == False:
                    self.set_tiles()
                    self.is_set_tiles = True
                    print("[[ Set Tiles ]]")
                
                # 양측 성 데이터 생성
                if self.is_set_castle == False:
                    new_left_castle = characters.CastleSprite(size=self.castle_size, position=LEFT_CASTLE_POSITION, movement=(0,0), group='left',
                                                            hp=3000, power=0, name=self.left_name, images=castle_images_left, game=self)
                    self.left_castle = new_left_castle
                    self.left_group.add(new_left_castle)
                    self.sprite_group.add(new_left_castle)
                    

                    new_right_castle = characters.CastleSprite(size=self.castle_size, position=RIGHT_CASTLE_POSITION, movement=(0,0), group='right',
                                                            hp=3000, power=0, name=self.right_name, images=castle_images_right, game=self)
                    self.right_castle = new_right_castle
                    self.right_group.add(new_right_castle)
                    self.sprite_group.add(new_right_castle)
                    self.is_set_castle = True
                    print("[[ Set Castle ]]")

                
                
                # 모든 처리가 완료되면 game state START로 변경
                if self.is_end_ready_animation and self.is_set_candidate and self.is_rank_updated and self.is_set_castle:
                    self.state = GAME_STATE_START
                    print("[[ Complete Ready Process ]]")

            
            # ================================== START ==================================
            if self.state == GAME_STATE_START:
                # is_set_timer = False
                # 타이머 시작
                # 모든 처리가 완료되면 game state PLAYING으로 변경
                self.start_ticks = pygame.time.get_ticks()
                self.state = GAME_STATE_PLAYING
                print("[[ SET TIMER ]]")
                print("[[ Complete Start Process ]]")
               


            
            # ================================== PLAYING ==================================
            if self.state == GAME_STATE_PLAYING:
                
                # 승,패 확인
                #   - 승패가 결정나면 game state를 OVER로 변경

                # 유닛 자동 생성 
                if self.auto_player_spawn_time == self.auto_player_spawn_term - 300 + 300:
                    #print("[SPAWN PLAYER AUTO]")
                    self.spawn_soldier('left', None)
                    self.spawn_soldier('right', None)
                    self.auto_player_spawn_time = 0
                    auto_player_num += 1                
                else:
                    self.auto_player_spawn_time += + 1

            # ==========================================================================


            # ================================== OVER ==================================
            if self.state == GAME_STATE_OVER:
                #print("[[ GAME OVER ]]")
                #print("%s:[%s] / %s:[%s]" % (self.left_castle.name, self.left_castle.hp, self.right_castle.name, self.right_castle.hp))     
                # is_end_over_animation = False
                # is_update_rank = False
                # is_clear_game_data = False
                
                # 승패 결정
                if self.is_update_rank == False:                    
                    left_rank_info = self.rank[self.left_castle.name]
                    right_rank_info = self.rank[self.right_castle.name]
                    
                    now_time = time.time()
                    if self.left_castle.hp > self.right_castle.hp:
                        #print("[[ %s WIN!! ]]" % self.left_castle.name) 
                        self.winner = self.left_castle.name
                        self.loser = self.right_castle.name
                        self.is_draw = False               
                        left_rank_info['win'] = left_rank_info['win'] + 1                    
                        right_rank_info['lose'] = right_rank_info['lose'] + 1       
                        
                        left_rank_info['update_time'] = now_time
                        right_rank_info['update_time'] = now_time

                        # self.is_draw = True   
                        # left_rank_info['draw'] = left_rank_info['draw'] + 1                    
                        # right_rank_info['draw'] = right_rank_info['draw'] + 1          

                    elif self.left_castle.hp < self.right_castle.hp:
                        #print("[[ %s WIN!! ]]" % self.right_castle.name)   
                        self.winner = self.right_castle.name
                        self.loser = self.left_castle.name
                        self.is_draw = False                    
                        left_rank_info['lose'] = left_rank_info['lose'] + 1                    
                        right_rank_info['win'] = right_rank_info['win'] + 1

                        left_rank_info['update_time'] = now_time
                        right_rank_info['update_time'] = now_time
                        # self.is_draw = True   
                        # left_rank_info['draw'] = left_rank_info['draw'] + 1                    
                        # right_rank_info['draw'] = right_rank_info['draw'] + 1

                    else:
                        #print("[[ DRAW ]]")
                        self.is_draw = True   
                        left_rank_info['draw'] = left_rank_info['draw'] + 1                    
                        right_rank_info['draw'] = right_rank_info['draw'] + 1

                        left_rank_info['update_time'] = now_time
                        right_rank_info['update_time'] = now_time

                    self.rank[self.left_castle.name] = left_rank_info
                    self.rank[self.right_castle.name] = right_rank_info
                    print("updated rank")
                    # 랭킹 정보 갱신
                    #   - 랭킹 정보 파일 통으로 새로 쓰기
                    f = open("game/data/city_rank.txt", 'w', encoding='UTF-8')
                    for candidate in self.candidates:                             
                        f.write(json.dumps(self.rank[candidate], ensure_ascii=False) + '\n')
                    f.close()
                    print("updated rank file")
                    self.update_rank()

                    self.is_update_rank = True
                    self.draw_result = True
                    self.sound_map['stage_clear'].play()

                
                
                # left, right sprite 모두 제거 
                # 상태 확인을 위한 모든 전역 변수 확인 후 적절하게 초기화
                # 모든 작업 완료 후 game state READY로 변경
                if self.is_clear_game_data == False:
                    self.sprite_group.empty()
                    self.tile_group.empty()
                    self.left_group.empty()
                    self.right_group.empty()

                    self.is_end_ready_animation = False
                    self.is_set_candidate = False
                    self.is_rank_updated = False
                    self.is_set_tiles = False   
                    self.is_set_castle = False  
                    self.is_set_timer = False

                    self.join_map = {}
                    self.left_name = ""
                    self.right_name = ""
                    self.donation_state = True

                    self.is_clear_game_data = True
                    print("clear game data")

                if self.is_end_over_animation and self.is_update_rank and self.is_clear_game_data:
                    self.is_end_over_animation = False
                    self.is_update_rank = False
                    self.is_clear_game_data = False
                    self.state = GAME_STATE_READY
                    print("[[ Complete Game Over Process ]]")

                

                

            # <화면 그리기>
            # 모든 Sprite update
            self.sprite_group.update(mt, self)
            
            # 배경색
            self.SCREEN.fill(self.COLOR_BLUE) 

            # 설명 UI
            desc_rect_x = SCREEN_WIDTH * 0.08
            desc_rect_y = desc_rect_x
            desc_rect_width = SCREEN_WIDTH * 0.43
            desc_rect_fill = pygame.draw.rect(self.SCREEN, (255, 255, 228), [desc_rect_x+3, desc_rect_y+3, desc_rect_width-6, desc_rect_width * 0.8 - 6], 
                                        border_radius=0, border_top_left_radius=5, border_top_right_radius=5, border_bottom_left_radius=5, border_bottom_right_radius=5)
            desc_rect_border = pygame.draw.rect(self.SCREEN, (153, 56, 0), [desc_rect_x, desc_rect_y, desc_rect_width, desc_rect_width * 0.8], 
                                        width=3, border_radius=0, border_top_left_radius=10, border_top_right_radius=10, border_bottom_left_radius=10, border_bottom_right_radius=10)

            # 참가 설명 텍스트
            text_join_title = self.main_font_15.render("[ 참가 방법 ]", True, self.COLOR_BLACK)
            text_join_title_rect = text_join_title.get_rect()
            text_join_title_rect.centerx = desc_rect_fill.centerx
            
            text_join_desc = self.main_font_13.render("현재 경기중인 지역 2개중에서", True, self.COLOR_BLACK)
            text_join_desc_rect = text_join_desc.get_rect()
            text_join_desc_rect.centerx = desc_rect_fill.centerx        

            text_join_desc2 = self.main_font_13.render("참가하려는 지역 이름을 채팅으로 입력", True, self.COLOR_BLACK)
            text_join_desc_rect2 = text_join_desc2.get_rect()
            text_join_desc_rect2.centerx = desc_rect_fill.centerx   

            self.SCREEN.blit(text_join_title, (text_join_title_rect.x, desc_rect_y + 15))
            self.SCREEN.blit(text_join_desc, (text_join_desc_rect.x, desc_rect_y + 35))
            self.SCREEN.blit(text_join_desc2, (text_join_desc_rect2.x, desc_rect_y + 55))
            
            # 유닛 추가 설명 텍스트
            text_join_title = self.main_font_15.render("[ 참가 후 유닛 추가 ]", True, self.COLOR_BLACK)
            text_join_title_rect = text_join_title.get_rect()
            text_join_title_rect.centerx = desc_rect_fill.centerx
            text_join_desc = self.main_font_13.render("likes x 5 => 1 Soldier", True, self.COLOR_BLACK)
            text_join_desc_rect = text_join_desc.get_rect()
            text_join_desc_rect.centerx = desc_rect_fill.centerx        
            text_skill_desc = self.main_font_13.render("likes x 15 => 10% Lightning", True, self.COLOR_BLACK)
            text_skill_desc_rect = text_skill_desc.get_rect()
            text_skill_desc_rect.centerx = desc_rect_fill.centerx        

            text_knight_desc = self.main_font_13.render("likes x 15 => 1% Knight", True, self.COLOR_BLACK)
            text_knight_desc_rect = text_knight_desc.get_rect()
            text_knight_desc_rect.centerx = desc_rect_fill.centerx        
            self.SCREEN.blit(text_join_title, (text_join_title_rect.x, desc_rect_y + 95))
            self.SCREEN.blit(text_join_desc, (text_join_desc_rect.x, desc_rect_y + 118))
            self.SCREEN.blit(text_skill_desc, (text_skill_desc_rect.x, desc_rect_y + 141))
            self.SCREEN.blit(text_knight_desc, (text_knight_desc_rect.x, desc_rect_y + 164))

            # 랭킹 정보 출력
            rank_rect_x = SCREEN_WIDTH * 0.54
            rank_rect_y = desc_rect_y
            rank_rect_width = SCREEN_WIDTH * 0.43
            rank_rect_fill = pygame.draw.rect(self.SCREEN, (255, 255, 228), [rank_rect_x+3, rank_rect_y+3, rank_rect_width-6, rank_rect_width * 1.22 - 6], 
                                        border_radius=0, border_top_left_radius=5, border_top_right_radius=5, border_bottom_left_radius=5, border_bottom_right_radius=5)
            rank_rect_border = pygame.draw.rect(self.SCREEN, (153, 56, 0), [rank_rect_x, rank_rect_y, rank_rect_width, rank_rect_width * 1.22], 
                                        width=3, border_radius=0, border_top_left_radius=10, border_top_right_radius=10, border_bottom_left_radius=10, border_bottom_right_radius=10)

            # 랭크 타이틀
            text_rank_title = self.main_font_20.render("[  R A N K  ]", True, self.COLOR_BLUE_DARK)
            text_rank_title_rect = text_rank_title.get_rect()
            text_rank_title_rect.centerx = rank_rect_fill.centerx
            self.SCREEN.blit(text_rank_title, (text_rank_title_rect.x, rank_rect_y + 15))


            for idx, r in enumerate(self.rank_list):
                rank_text = self.main_font_15.render("%d위. %s  %s점"%(r['rank'], r['name'], r['score']), True, self.COLOR_BLACK)
                rank_text_rect = rank_text.get_rect()
                rank_text_rect.x = rank_rect_fill.x + (SCREEN_WIDTH * 0.03)

                interval = r['rank'] * 9 + (r['rank'] * 15)
                self.SCREEN.blit(rank_text, (rank_text_rect.x, (rank_rect_y + 15 + text_rank_title_rect.height*0.5) + interval))
                if idx == 9:
                    break

            for idx, r in enumerate(self.rank_list[10:]):
                rank_text = self.main_font_15.render("%d위. %s  %s점"%(r['rank'], r['name'], r['score']), True, self.COLOR_BLACK)
                rank_text_rect = rank_text.get_rect()
                rank_text_rect.x = rank_rect_fill.x + 10 + SCREEN_WIDTH * 0.21

                interval = (r['rank'] - 10) * 9 + ((r['rank'] - 10) * 15)
                self.SCREEN.blit(rank_text, (rank_text_rect.x, (rank_rect_y + 15 + text_rank_title_rect.height*0.5) + interval))
                
                    
            # 공지사항
            if self.now_notice != None:
                text_notice = self.main_bold_font_14.render(self.now_notice, True, self.COLOR_GREY_LIGHT)
                text_notice_rect = text_notice.get_rect()
                text_notice_rect.centerx = (SCREEN_WIDTH * 0.5)
                self.SCREEN.blit(text_notice, (text_notice_rect.x, SCREEN_HEIGHT * 0.5))



            # ================================== READY ==================================
            if self.state == GAME_STATE_READY:
                self.is_end_ready_animation = True
                



            # ================================== START ==================================
            if self.state == GAME_STATE_START:
                pass


            # ================================== PLAYING ==================================
            if self.state == GAME_STATE_PLAYING:
                
                # game play timer
                play_time_sec = int((pygame.time.get_ticks() - self.start_ticks) / 1000)                
                last_time = self.game_timer_term - play_time_sec
                min = int(last_time / 60)
                sec = int(last_time % 60)

                if min == 0 and sec == 0:
                    self.state = GAME_STATE_OVER
                    self.over_animation_time = pygame.time.get_ticks()

                min_str = "0%d"%min if min < 10 else "%d"%min
                sec_str = "0%d"%sec if sec < 10 else "%d"%sec
                timer_str = "%s : %s" % (min_str, sec_str)
                #print("남은 시간 %s" % timer_str)

                timer_text = self.sebang_font_30_bold.render(timer_str, True, self.COLOR_BLACK)
                timer_text_rect = timer_text.get_rect()
                timer_text_rect.centerx = SCREEN_WIDTH * 0.5
                self.SCREEN.blit(timer_text, (timer_text_rect.x, SCREEN_HEIGHT * 0.38))


            # ================================== OVER ==================================            
            if self.state == GAME_STATE_OVER and self.draw_result == True:
                # 게임 결과 애니메이션 출력
                now_over_animation_time = pygame.time.get_ticks()
                animation_time = int((now_over_animation_time - self.over_animation_time) / 1000)
                
                #s = pygame.Surface((300,300), pygame.SRCALPHA) 
                # game over screen background
                game_over_screen = pygame.Surface((SCREEN_WIDTH * 0.7, SCREEN_HEIGHT * ( 0.5 if self.is_draw else 0.8))) 
                #game_over_screen = pygame.Surface((SCREEN_WIDTH * 0.7, SCREEN_HEIGHT * 0.8)) 
                game_over_screen.set_alpha(200)   
                #s.fill((0,0,0))             
                game_over_screen_rect = game_over_screen.get_rect()
                game_over_screen_rect.center = self.SCREEN.get_rect().center

                #self.sound_map['stage_clear'].play()

                if self.is_draw:
                    text_draw = self.main_font_60.render("DRAW", True, self.COLOR_GREEN_LIGHT)    
                    text_draw_rect = text_draw.get_rect()
                    text_draw_rect.centerx = game_over_screen_rect.centerx + 50
                    game_over_screen.blit(text_draw, (game_over_screen_rect.size[0] * 0.25, game_over_screen_rect.size[1] * 0.3))                 
                else:
                    text_win = self.main_font_60.render("WIN", True, self.COLOR_BLUE_LIGHT)    
                    text_win_rect = text_win.get_rect()
                    text_win_rect.centerx = game_over_screen_rect.centerx                
                    game_over_screen.blit(text_win, (game_over_screen_rect.size[0] * 0.33, game_over_screen_rect.size[1] * 0.1))

                    text_winner = self.main_font_60.render(self.winner, True, self.COLOR_WHITE)    
                    text_winner_rect = text_winner.get_rect()
                    game_over_screen.blit(text_winner, (game_over_screen_rect.size[0] * 0.35, game_over_screen_rect.size[1] * 0.3))

                    text_lose = self.main_font_60.render("LOSE", True, self.COLOR_RED_LIGHT)    
                    text_lose_rect = text_lose.get_rect()                
                    text_lose_rect.center = game_over_screen_rect.center
                    game_over_screen.blit(text_lose, (game_over_screen_rect.size[0] * 0.3, game_over_screen_rect.size[1] * 0.6))


                    text_loser = self.main_font_60.render(self.loser, True, self.COLOR_WHITE)    
                    text_loser_rect = text_loser.get_rect()
                    game_over_screen.blit(text_loser, (game_over_screen_rect.size[0] * 0.35, game_over_screen_rect.size[1] * 0.8))

                self.SCREEN.blit(game_over_screen, game_over_screen_rect.topleft)
                #pygame.transform.smoothscale(game_over_screen, (SCREEN_WIDTH, SCREEN_HEIGHT))

                if animation_time == 10:
                    self.is_end_over_animation = True
                    self.over_animation_time = 0
                    self.draw_result = False
                    self.is_draw = False
                

            # 객체별로 필요한 백그라운드 그려주기
            for sprite in self.sprite_group:
                sprite.draw_back()   

            # 모든 sprite 화면에 그려주기
            self.sprite_group.draw(self.SCREEN)      

            
            # 객체별로 필요한 그림 그려주기
            for sprite in self.sprite_group:
                sprite.draw(mt)        
            
            #pygame.display.flip()
            pygame.display.update()



    async def game_event_loop(self, event_queue):        
        current_time = 0
        while True:
            #print('game_event_loop')
            last_time, current_time = current_time, time.time()
            await asyncio.sleep(1 / FPS - (current_time - last_time))
            event = pygame.event.poll()
            if event.type != pygame.NOEVENT:
                await event_queue.put(event)

    async def handle_events(self, event_queue):
        isLeft = True
        current_time = 0
        while True:
            last_time, current_time = current_time, time.time()
            await asyncio.sleep(10 / FPS - (current_time - last_time))
            event = await event_queue.get()
            #print("event", event)
            if event.type == pygame.QUIT:
                break            
            else:
                pass
                #print("event", event)
        asyncio.get_event_loop().stop()

    def ws_msg_process(self, message):
        msg_obj = None
        try:
            msg_obj = json.loads(message)
            #print("[[ Message Object ]]")                    
            #print(msg_obj)
        except Exception as e:
            print("[error]:%s" % e)
            raise
        
        # 도네이션의 경우 무조건 넘겨준다.
        # 다른 이벤트는 state가 playing이 아니라면 패스

        if msg_obj != None:
            if msg_obj['code'] == MSG_CODE_COMMENT and self.state == GAME_STATE_PLAYING:
                # 채팅에 팀 이름 포함 여부 확인
                # 이미 팀에 포함 되어 있는지 확인
                if msg_obj['user_id'] in self.join_map:
                    # 1.이미 팀에 포함되어 있다면 and 해당 사용자의 유닛이 살아 있다면 => 채팅 출력                    
                    user_info = self.join_map[msg_obj['user_id']]
                    if len(user_info['spawn_units']) > 0:
                        for idx, unit in enumerate(user_info['spawn_units']):                                        
                            if idx == 0:                    
                                unit.chat = msg_obj['comment']
                                break
                    
                    # 이미 참가했는데 계속해서 참가 채팅을 치는 경우 도움말 공지사항 띄우기
                    if msg_obj['comment'] == self.left_name or msg_obj['comment'] == self.right_name:
                        self.duplicate_join_cnt += 1
                        if self.duplicate_join_cnt >= self.duplicate_join_limit:
                            self.notice_queue.append("유닛 추가와 스킬은 좋아요 또는 후원으로 사용 가능합니다.")
                            self.duplicate_join_cnt = 0

                    
                else:
                    # 2. 포함되어 있지 않다면 
                    # => 팀에 포함 + 유닛 생성
                    print("[%s]: %s" % (msg_obj['nickname'], msg_obj['comment']))

                    # 현재 진행중이지 않은 지역을 계속해서 입력하는 경우
                    if msg_obj['comment'] != self.left_name and msg_obj['comment'] != self.right_name and msg_obj['comment'] in self.candidates:
                        self.invalid_join_cnt += 1
                        if self.invalid_join_cnt >= self.invalid_join_limit:
                            self.notice_queue.append("현재 전투중인 지역 이름을 입력하여 참가해주세요.")
                            self.invalid_join_limit = 0

                    #print(chardet.detect(msg_obj['nickname'].encode()))
                    #print(chardet.detect(msg_obj['comment'].encode()))                                
                    try:                        
                        nick = msg_obj['nickname']
                        com = msg_obj['comment']
                        
                        #nick_encoded = nick.encode('utf-8')
                        #print("nick[%s]/utf-encode[%s]"%(nick, nick_encoded))
                        #print("nick[%s]/unicode-escape[%s]"%(nick, nick_encoded.decode('unicode_escape')))

                        #print("UTF[%s]: %s" % (msg_obj['nickname'].encode(encoding='UTF-8'), msg_obj['comment']))                                                               
                        #print("Windows-1253[%s]: %s" % (msg_obj['nickname'].encode(encoding='Windows-1253'), msg_obj['comment']))
                    except Exception as e:
                        print(e)


                    if msg_obj['comment'].find(self.left_name) != -1:
                        msg_obj['group'] = 'left'
                        msg_obj['spawn_units'] = pygame.sprite.Group()
                        self.join_map[msg_obj['user_id']] = msg_obj      
                        self.join_queue.append(self.join_map[msg_obj['user_id']])                                                     
                                                      
                    elif msg_obj['comment'].find(self.right_name) != -1:
                        msg_obj['group'] = 'right'
                        msg_obj['spawn_units'] = pygame.sprite.Group()
                        self.join_map[msg_obj['user_id']] = msg_obj
                        self.join_queue.append(self.join_map[msg_obj['user_id']])
                                       

                    
            elif msg_obj['code'] == MSG_CODE_LIKE and self.state == GAME_STATE_PLAYING:
                print("[%s] likes count: %d" %(msg_obj['nickname'], msg_obj['like_count']))
                #unit_count = int(msg_obj['like_count'] / 5)
                #self.donation_queue.append(msg_obj)

                # # 참가 하지않고 좋아요만 누르는 경우 안내 메시지 노출
                if msg_obj['user_id'] in self.join_map:
                    pass
                else:
                    self.none_join_like_cnt += 1
                    if self.none_join_like_cnt >= self.none_join_like_limit:
                        self.notice_queue.append("채팅으로 참여 후 좋아요로 유닛 추가가 가능합니다.")
                        self.notice_queue.append("채팅으로 현재 대결중인 지역 이름을 입력하여 참가 가능합니다.")                        
                        self.none_join_like_cnt = 0

                if msg_obj['like_count'] >= 15 and msg_obj['user_id'] in self.join_map:
                    
                    is_knight = False
                    rand_int = random.randint(0, 99)
                    if rand_int == 1:
                        is_knight = True
                        # 나이트 소환
                        if msg_obj['user_id'] in self.join_map:
                            user_info = self.join_map[msg_obj['user_id']]
                            if user_info['group'] == 'left':                
                                self.spawn_knight('left', user_info)
                            else:
                                self.spawn_knight('right', user_info)
                            self.print_log_msg('%s님이 기사를 소환했습니다.'%(user_info['nickname']), user_info['profile'])
                    
                    rand_int = random.randint(0, 9)
                    if rand_int == 1 and is_knight == False:
                        user_info = self.join_map[msg_obj['user_id']]
                        if user_info['group'] == 'left':
                            self.spell_lightning('left')
                        else:
                            self.spell_lightning('right')
                        self.print_log_msg('%s님이 번개를 사용했습니다.'%(user_info['nickname']), user_info['profile'])

                    rand_int = random.randint(0, 2)
                    if rand_int == 1 and is_knight == False:
                        user_info = self.join_map[msg_obj['user_id']]
                        if user_info['group'] == 'left':
                            self.spawn_soldier('left', user_info)
                        else:
                            self.spawn_soldier('right', user_info)
                        self.print_log_msg('%s님이 일반 병사를 소환했습니다.'%(user_info['nickname']), user_info['profile'])

                elif msg_obj['like_count'] >= 5 and msg_obj['user_id'] in self.join_map:
                    user_info = self.join_map[msg_obj['user_id']]
                    if user_info['group'] == 'left':
                        self.spawn_soldier('left', user_info)
                    else:
                        self.spawn_soldier('right', user_info)
                    self.print_log_msg('%s님이 일반 병사를 소환했습니다.'%(user_info['nickname']), user_info['profile'])

            elif msg_obj['code'] == MSG_CODE_DONATION:
                print("[%s] dontaion: %d" %(msg_obj['nickname'], msg_obj['coin']))
                
                # 사용자의 팀 확인
                # 맵에서 가져올때 null 확인
                user_id = msg_obj['user_id']

                # must - 도네이션 애니메이션만 출력
                self.donation_queue.append(msg_obj)

                # 플레이 상태라면
                if self.state == GAME_STATE_PLAYING:
                    # 팀확인
                    # 도네이션 액수 확인
                    # 스킬 시전
                    diamondCnt = msg_obj['coin']
                    if diamondCnt >= 1 and diamondCnt < 5:                                
                        if msg_obj['user_id'] in self.join_map:                                    
                            user_info = self.join_map[msg_obj['user_id']]
                            if user_info['group'] == 'left':                
                                self.spell_lightning('left')
                            else:
                                self.spell_lightning('right')     
                            self.print_log_msg('%s님이 번개를 사용했습니다.'%(user_info['nickname']), user_info['profile'])                           
                    elif diamondCnt >= 5 and diamondCnt < 10:
                        # 솔져 소환 x5
                        # 시간 간격 두고 소환         
                        # TODO: 위치 치정                       
                        if msg_obj['user_id'] in self.join_map:                                    
                            #print("[SPAWN 5 Soldiers]")                                                                
                            user_info = self.join_map[msg_obj['user_id']]            
                            self.print_log_msg('%s님이 일반 병사 5 소환.'%(user_info['nickname']), user_info['profile'])

                            for i in range(1,6):
                                xy = None
                                if user_info['group'] == 'right':
                                    xy = (RIGHT_SPAWN_POSITION[0] + (i * 50), RIGHT_SPAWN_POSITION[1])
                                else:
                                    xy = (LEFT_SPAWN_POSITION[0] - (i * 50), LEFT_SPAWN_POSITION[1])

                                self.spawn_soldier_xy(user_info['group'], user_info, xy)

                    elif diamondCnt >= 10 and diamondCnt < 20:
                        # 나이트 소환
                        if msg_obj['user_id'] in self.join_map:
                            user_info = self.join_map[msg_obj['user_id']]
                            if user_info['group'] == 'left':                
                                self.spawn_knight('left', user_info)
                            else:
                                self.spawn_knight('right', user_info)
                            self.print_log_msg('%s님이 기사를 소환했습니다.'%(user_info['nickname']), user_info['profile'])

                    elif diamondCnt >= 20 and diamondCnt < 30:
                        # 참여 팀 확인
                        # 해당 팀의 castle 체력 증가
                        # TODO: 효과음 재생
                        if msg_obj['user_id'] in self.join_map:
                            user_info = self.join_map[msg_obj['user_id']]
                            if user_info['group'] == 'left':                
                                self.left_castle.hp = self.left_castle.hp_max
                            else:
                                self.right_castle.hp = self.right_castle.hp_max
                            self.print_log_msg('%s님이 회복을 사용했습니다.'%(user_info['nickname']), user_info['profile'])
                    elif diamondCnt >= 30:
                        if msg_obj['user_id'] in self.join_map:
                            user_info = self.join_map[msg_obj['user_id']]
                            if user_info['group'] == 'left':                
                                self.spell_devil('left')
                            else:
                                self.spell_devil('right')
                            self.print_log_msg('%s님이 악마를 사용했습니다.'%(user_info['nickname']), user_info['profile'])
            elif msg_obj['code'] == MSG_CODE_SHARE:
                pass 
            elif msg_obj['code'] == MSG_CODE_NOTICE:
                self.notice_queue.append(msg_obj['msg'])
                



    async def connect_to_server(self, event_queue): 
        print("[[ Cnnect to server ]]")
        target_ip = 'localhost'
        async with websockets.connect("ws://%s:30001" % target_ip) as websocket:
            await websocket.send("Hi server. I'm client" );          
            self.websocket = websocket
            
            current_time = 0            
            while True:
                #print("check")
                last_time, current_time = current_time, time.time()
                await asyncio.sleep(1 / FPS - (current_time - last_time))                
                now = datetime.datetime.now()
                
                # send message
                if len(self.message_queue) > 0: 
                    for message in self.message_queue:
                        print("[[ send to server ]]: %s" % message)
                        await self.websocket.send(message)
                        del self.message_queue[0]
                        break
                try:
                    msg_rcv = await websocket.recv();
                    #print('\n\n[%s] %s' % (now, msg_rcv))
                    #new_event = pygame.event.Event(EVENT_SOCKET_MSG, message=msg_rcv)    
                    #await event_queue.put(new_event) 
                    self.ws_msg_process(msg_rcv)
                except Exception as e:
                    print(e)
                


    def run(self):
        loop = asyncio.get_event_loop()
        event_queue = asyncio.Queue()

        pygame_task = asyncio.ensure_future(self.game_event_loop(event_queue))
        animation_task = asyncio.ensure_future(self.animation())
        event_task = asyncio.ensure_future(self.handle_events(event_queue))
        end_check_task = asyncio.ensure_future(self.check_castle_hp())
        socket_task = asyncio.ensure_future(self.connect_to_server(event_queue))
        img_task = asyncio.ensure_future(self.print_donation())
        join_task = asyncio.ensure_future(self.join_process())
        notice_task = asyncio.ensure_future(self.print_notice())        
        
        try:
            loop.run_forever()
        except KeyboardInterrupt:
            pass
        except Exception as e:
            print(e)
        finally:
            pygame_task.cancel()
            animation_task.cancel()
            event_task.cancel()
            socket_task.cancel()
            img_task.cancel()
            end_check_task.cancel()
            join_task.cancel()
            notice_task.cancel()

        pygame.quit()

    async def check_castle_hp(self):
        current_time = 0       
        while True:
            last_time, current_time = current_time, time.time()
            await asyncio.sleep(1 / FPS - (current_time - last_time))                      
            if self.destroyed_castle != None and len(self.destroyed_castle) > 0:
                self.destroyed_castle = None
                self.state = GAME_STATE_OVER
                self.over_animation_time = pygame.time.get_ticks()

    # 게임 참여 사용자들을 처리하는 로직
    async def join_process(self):
        print("[join_process]")
        # queue에서 join된 사용자 확인
        current_time = 0       
        while True:
            last_time, current_time = current_time, time.time()
            await asyncio.sleep(1 / FPS - (current_time - last_time))          
            
            if len(self.join_queue) > 0:
                user_info = self.join_queue[0]
                # 사용자 이미지 캐시 저장
                group = user_info['group']
                user_id = user_info['user_id']
                img_url = user_info['profile_img']
                image = self.get_cropped_image(user_id, img_url, self.profile_size)
                user_info['profile'] = image               
                self.join_map[user_id] = user_info

                if group == 'left':
                    self.print_log_msg('%s님이 %s에 참여했습니다.'%(user_info['nickname'], self.left_name), user_info['profile'])  
                else:
                    self.print_log_msg('%s님이 %s에 참여했습니다.'%(user_info['nickname'], self.right_name), user_info['profile'])  

                # 사용자 닉네임과 이미지와 함께 유닛(솔져) 생성
                spawn_soldier = self.spawn_soldier(group, user_info)
                
                del self.join_queue[0]       
       
    def update_rank(self):
        self.rank_list = []
        for key in self.rank:
            tmp_rank = self.rank[key]
            score = (tmp_rank['win'] * 2) + (tmp_rank['draw'] * 1) - (tmp_rank['lose'] * 1)
            tmp_rank['score'] = score
            self.rank[key] = tmp_rank
            self.rank_list.append(tmp_rank)
            #print(tmp_rank)

        self.sort_rank()
        
    def sort_rank(self):        
        self.rank_list.sort(key = lambda object : (object['score'], object['update_time']), reverse=True)

        for idx, r in enumerate(self.rank_list):
            self.rank[r['name']]['rank'] = idx + 1
            self.rank_list[idx]['rank'] = idx + 1

        self.print_rank()

    def print_rank(self):
        print("[[ RANK ]] ====================")
        for idx, rank in enumerate(self.rank_list):
            print("[Top %d] %s => %s" % (idx+1, rank['name'], rank['score']))
        print("===============================")

    # 원 모양으로 크롭된 이미지 가져오기
    # user_id에 대한 캐시된 이미지 있으면 바로 가져온다.
    # 없으면 img_url을 통해 이미지를 다운 받고 crop 후 이미지 저장
    # return: pygame에서 사용할 수 있는 Image를 반환
    def get_cropped_image(self, user_id, img_url, size):
        print("[get_cropped_image]")

        cache_path = "game/res/cache/profile/%s.png" % user_id

        # 캐시 파일 존재 확인
        is_file = os.path.isfile(cache_path)
        
        image = None
        if is_file:
            image = pygame.transform.scale(pygame.image.load(cache_path), size)
        else:
            try:
                image_str = urlopen(img_url).read()

                # use PIL
                pil_img = Image.open(io.BytesIO(image_str))

                height,width = pil_img.size
                lum_img = Image.new('L', [height, width] , 0)
                
                draw = ImageDraw.Draw(lum_img)
                draw.pieslice([(0,0), (height - 3,width - 3)], 0, 360, 
                            fill = 255, outline = "white")
                img_arr =np.array(pil_img)
                lum_img_arr =np.array(lum_img)                    
                final_img_arr = np.dstack((img_arr,lum_img_arr))                        

                final_pil_img = Image.fromarray(final_img_arr)

                # 캐시 파일 저장
                final_pil_img.save(cache_path, 'png')
                image = pygame.transform.scale(pygame.image.load(cache_path), size)
            except Exception as e:
                print(e)
                image = pygame.transform.scale(pygame.image.load('game/res/default.png'), size)

        return image

    async def print_donation(self):        
        current_time = 0       
        while True:
            last_time, current_time = current_time, time.time()
            await asyncio.sleep(1 / FPS - (current_time - last_time))          
            
            if len(self.donation_queue) > 0 and self.donation_state == True:

                self.donation_state = False

                try:                
                    # # get image from url and set stream file
                    # image_str = urlopen(donation_obj['profile_img']).read()
                    # image_file = io.BytesIO(image_str) 
                    # image = pygame.image.load(image_file)
                    # image = pygame.image.load(image_file)                    

                    #print("[print_web_image]")
                    donation_obj = self.donation_queue[0]
                    #print(donation_obj)
                    user_id = donation_obj['user_id']
                    
                    #print("[user_id]:%s" % user_id)

                    cache_path = "game/res/cache/profile/%s.png" % user_id

                    # 캐시 파일 존재 확인
                    is_file = os.path.isfile(cache_path)
                    
                    image = None
                    if is_file:
                        image = pygame.transform.scale(pygame.image.load(cache_path), self.donation_size)
                    else:
                        try:
                            image_str = urlopen(donation_obj['profile_img']).read()

                            # use PIL
                            pil_img = Image.open(io.BytesIO(image_str))
                            
                            height,width = pil_img.size
                            lum_img = Image.new('L', [height,width] , 0)
                            
                            draw = ImageDraw.Draw(lum_img)
                            draw.pieslice([(0,0), (height - 3, width - 3)], 0, 360, 
                                        fill = 255, outline = "white")
                            img_arr =np.array(pil_img)
                            lum_img_arr =np.array(lum_img)                    
                            final_img_arr = np.dstack((img_arr,lum_img_arr))                        

                            final_pil_img = Image.fromarray(final_img_arr)

                            # 캐시 파일 저장
                            final_pil_img.save(cache_path, 'png')
                            image = pygame.transform.scale(pygame.image.load(cache_path), self.donation_size)
                        except:
                            image = pygame.transform.scale(pygame.image.load('game/res/default.png'), self.donation_size)

                    tmps = []
                    tmps.append(image)                    
                    new_donation = ui.DonationSprite(size=self.donation_size, position=((SCREEN_WIDTH * 0.28) - (self.donation_size[0] * 0.5), SCREEN_HEIGHT * 0.22), group='donation', 
                                                    name=donation_obj['nickname'], coin=donation_obj['coin'], images=tmps, sound=self.sound_map['donation'], game=self)
                    self.ui_group.add(new_donation)
                    self.sprite_group.add(new_donation)
                    del self.donation_queue[0]
                except Exception as e:
                    print("[print_donation error]:%s" % e)
                    del self.donation_queue[0]


    async def print_notice(self):        
        prev_tick = 0        
        current_time = 0
        while True:
            last_time, current_time = current_time, time.time()
            await asyncio.sleep(1 / FPS - (current_time - last_time))          
            
            now_tick = pygame.time.get_ticks()
            tick_term = now_tick - prev_tick
            if self.now_notice != None:  
                self.notice_time += tick_term / 1000
                prev_tick = now_tick
                if self.notice_time >= self.notice_term:
                    self.notice_time = 0
                    self.now_notice = None
                    self.notice_state = True

            if len(self.notice_queue) > 0 and self.notice_state == True:
                self.notice_state = False
                self.now_notice = self.notice_queue[0]
                self.notice_queue = self.notice_queue[1:]
                prev_tick = pygame.time.get_ticks()




    ####### SPAWN LOGIC #######       
    def spawn_soldier(self, group, user_info):
        #print("[spawn_soldier]:%s, %s"%(group, user_info))

        ch_name = "%s_soldier"%group
        profile_img = None

        if user_info != None:
            ch_name = user_info['nickname']
            if 'profile' in user_info:
                profile_img = user_info['profile']                

        new_soldier = None
        if group == 'right':
            new_soldier = characters.SoldierSprite(size=self.soldier_size, position=RIGHT_SPAWN_POSITION, movement=(-1,0), state=1, group='right', 
                                                hp=150, power=1, name=ch_name, profile=profile_img, images=soldier_images_right, game=self)
            self.right_group.add(new_soldier)
            self.sprite_group.add(new_soldier)

        elif group == 'left':
            new_soldier = characters.SoldierSprite(size=self.soldier_size, position=LEFT_SPAWN_POSITION, movement=(1,0), state=1, group='left', 
                                            hp=150, power=1, name=ch_name, profile=profile_img, images=soldier_images_left, game=self)
            self.left_group.add(new_soldier)
            self.sprite_group.add(new_soldier)
            

        if user_info != None and new_soldier != None:
            user_info = self.join_map[user_info['user_id']]
            user_info['spawn_units'].add(new_soldier)
            self.join_map[user_info['user_id']] = user_info


    def spawn_soldier_xy(self, group, user_info, xy):
        #print("[spawn_soldier]:%s, %s"%(group, user_info))

        ch_name = "%s_soldier"%group
        profile_img = None

        if user_info != None:
            ch_name = user_info['nickname']
            if 'profile' in user_info:
                profile_img = user_info['profile']
                

        new_soldier = None
        if group == 'right':
            new_soldier = characters.SoldierSprite(size=self.soldier_size, position=xy, movement=(-1,0), state=1, group='right', 
                                                hp=150, power=1, name=ch_name, profile=profile_img, images=soldier_images_right, game=self)
            self.right_group.add(new_soldier)
            self.sprite_group.add(new_soldier)
        elif group == 'left':
            new_soldier = characters.SoldierSprite(size=self.soldier_size, position=xy, movement=(1,0), state=1, group='left', 
                                            hp=150, power=1, name=ch_name, profile=profile_img, images=soldier_images_left, game=self)
            self.left_group.add(new_soldier)
            self.sprite_group.add(new_soldier)

        if user_info != None and new_soldier != None:
            user_info = self.join_map[user_info['user_id']]
            user_info['spawn_units'].add(new_soldier)
            self.join_map[user_info['user_id']] = user_info
        
    def spawn_knight(self, group, user_info):

        ch_name = "%s_soldier"%group
        profile_img = None

        if user_info != None:
            ch_name = user_info['nickname']
            if 'profile' in user_info:
                profile_img = user_info['profile']


        new_knight = None
        if group == 'right':
            speed = -1
            sp_y = RIGHT_SPAWN_POSITION[1]
            new_y = sp_y - (self.knight_size[0] - self.soldier_size[0])
            sp_xy = (RIGHT_SPAWN_POSITION[0], new_y)

            new_knight = characters.KnightSprite(size=self.knight_size, position=sp_xy, movement=(speed,0), group='right', 
                                                        hp=1000, power=10, name=ch_name, profile=profile_img, images=knight_images_right, game=self)
            self.right_group.add(new_knight)
            self.sprite_group.add(new_knight)
        else:
            speed = 1
            sp_y = LEFT_SPAWN_POSITION[1]
            new_y = sp_y - (self.knight_size[0] - self.soldier_size[0])
            sp_xy = (LEFT_SPAWN_POSITION[0], new_y)
            new_knight = characters.KnightSprite(size=self.knight_size, position=sp_xy, movement=(speed,0), group='left', 
                                                        hp=1000, power=10, name=ch_name, profile=profile_img, images=knight_images_left, game=self)
        
            self.left_group.add(new_knight)
            self.sprite_group.add(new_knight)

        if user_info != None and new_knight != None:
            user_info = self.join_map[user_info['user_id']]
            user_info['spawn_units'].add(new_knight)
            self.join_map[user_info['user_id']] = user_info
        
            
    ####### SKILL LOGIC #######
    def spell_lightning(self, group_name): 
        print("%s group spell lightning!" % group_name)     
        target_group = None
        if group_name == 'left':
            target_group = self.right_group
        else:
            target_group = self.left_group
        
        if len(target_group) > 1:
            sp_x = 0
            rand_idx = random.randint(1, len(target_group) - 1)
            for idx, sprite in enumerate(target_group):               
                if rand_idx == idx:
                    sp_x = sprite.rect.x
                
            sp_y = RIGHT_SPAWN_POSITION[1]
            new_y = sp_y - (self.lightning_size[1] - self.soldier_size[0])
            sp_xy = (sp_x, new_y)
            new_lightning = skills.LightningSprite(size=self.lightning_size, position=sp_xy, movement=(0,0), group=group_name, 
                                                    hp=100, power=250, name='%s_thunder'%group_name, skill_type=1, images=lightning_images, animation_count=2, sound=self.sound_map['thunder'], game=self)
            self.skill_group.add(new_lightning)
            self.sprite_group.add(new_lightning)


    def spell_devil(self, group_name):
        tmp_rect = pygame.Rect(0, 0, self.devil_size[0], self.devil_size[1])
        tmp_rect.centerx = SCREEN_WIDTH / 2
        sp_xy = (tmp_rect.x, SCREEN_HEIGHT * 0.2)
        new_lightning = skills.DevilSprite(size=self.devil_size, position=sp_xy, movement=(0,0), group=group_name, 
                                                hp=100, power=100000, name='%s_devil'%group_name, skill_type=2, images=devil_images, animation_count=6, sound=self.sound_map['devil'], game=self)
        self.skill_group.add(new_lightning)
        self.sprite_group.add(new_lightning)


    def print_log_msg(self, msg, profile):
        new_log = ui.LogSprite(size=self.profile_size, position=LOG_POSITION, msg=msg, profile=profile, game=self)
        self.sprite_group.add(new_log)


    def set_tiles(self):        
        # ground 타일 생성
        col_size = int(SCREEN_WIDTH / self.tile_size[0])
        if SCREEN_WIDTH % self.tile_size[0] > 0:
            col_size += 1

        row_size = int((SCREEN_HEIGHT - LAND_BOTTOM_HEIGHT) / self.tile_size[0])
        if (SCREEN_HEIGHT - LAND_BOTTOM_HEIGHT) / self.tile_size[0] > 0:
            row_size += 1

        ground_x = 0
        ground_y = LAND_BOTTOM_HEIGHT - self.castle_size[1] * 0.36
        for row in range(0, row_size):
            ground_x = 0
            for col in range(0, col_size):
                new_ground_tile = tiles.TileSprite(size=self.tile_size, position=(ground_x, ground_y), movement=(0,0), group='tile',
                                                hp=10000, power=0, name='ground tile', images=ground_tile_images, game=self)
    
                self.tile_group.add(new_ground_tile)
                self.sprite_group.add(new_ground_tile) 
                ground_x += self.tile_size[0]
            ground_y += self.tile_size[0]

        # stone 타일 생성 
        col_size = int(SCREEN_WIDTH / self.tile_size[0])
        if SCREEN_WIDTH % self.tile_size[0] > 0:
            col_size += 1

        row_size = int((SCREEN_HEIGHT - LAND_BOTTOM_HEIGHT) / self.tile_size[0])
        if (SCREEN_HEIGHT - LAND_BOTTOM_HEIGHT) / self.tile_size[0] > 0:
            row_size += 1

        stone_x = 0
        stone_y = LAND_BOTTOM_HEIGHT
        for row in range(0, row_size):
            stone_x = 0
            for col in range(0, col_size):
                new_stone_tile = tiles.TileSprite(size=self.tile_size, position=(stone_x, stone_y), movement=(0,0), group='tile',
                                                hp=10000, power=0, name='stone tile', images=stone_tile_images, game=self)
    
                self.tile_group.add(new_stone_tile)
                self.sprite_group.add(new_stone_tile) 
                stone_x += self.tile_size[0]
            stone_y += self.tile_size[0]
        
        menu_x = ((SCREEN_WIDTH / MAX_SKILL_COUNT) * 0.15) # TODO + profile_img_size
        menu_y = LAND_BOTTOM_HEIGHT + ((SCREEN_WIDTH / 4) * 0.15)
        for idx, skill in enumerate(self.skills):
            tmp_image_list = []
            tmp_image_list.append(menu_images[idx])
            new_skill_menu = ui.SkillMenuSprite(size=self.menu_size, position=(menu_x, menu_y), group='menu', 
                                                name=skill['name'], coin=skill['coin'], images=tmp_image_list, game=self)
            self.ui_group.add(new_skill_menu)
            self.sprite_group.add(new_skill_menu)
            menu_x += self.menu_size[0] + ((SCREEN_WIDTH / MAX_SKILL_COUNT) * 0.15 * 2)
            
            # TODO: 현재 menu_x가 SCREEN WIDTH를 넘어서는 경우
            #menu_y += self.menu_size[0] + ((SCREEN_WIDTH / MAX_SKILL_COUNT) * 0.15)
        


if __name__ == '__main__':
    game = Game()
    game.run()