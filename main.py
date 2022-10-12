import pygame
import pygame.mixer
import asyncio
import time
import datetime
import websockets
from game.sprite import characters
from game.sprite import tiles
from game.dataload import *
from game.transitions import *


# 0:초기화 / 1:다음 게임 준비 / 2: 게임 시작 / 3: 플레이 / 4: 게임 종료
GAME_STATE_INIT = 0
GAME_STATE_READY = 1
GAME_STATE_START = 2
GAME_STATE_PLAYING = 3
GAME_STATE_OVER = 4


FPS = 60

# 스크린 전체 크기 지정
SCREEN_WIDTH = 475
SCREEN_HEIGHT = 844

LAND_TOP_HEIGHT = SCREEN_HEIGHT * 0.5
LAND_BOTTOM_HEIGHT = LAND_TOP_HEIGHT + 179

print("[LAND_HEIGHT]:%d" % LAND_TOP_HEIGHT)

LEFT_CASTLE_POSITION = (-18, LAND_TOP_HEIGHT)
RIGHT_CASTLE_POSITION = (SCREEN_WIDTH - 85, LAND_TOP_HEIGHT)

LEFT_SPAWN_POSITION = (50, LAND_TOP_HEIGHT + 100)
RIGHT_SPAWN_POSITION = (400, LAND_TOP_HEIGHT + 100)


# 커스텀 이벤트 생성
EVENT_NEW_USER_LEFT = pygame.USEREVENT+1
EVENT_NEW_USER_RIGHT = pygame.USEREVENT+1
new_user_left_event = pygame.event.Event(EVENT_NEW_USER_LEFT, message="New left user.")
new_user_right_event = pygame.event.Event(EVENT_NEW_USER_RIGHT, message="New right user.")

# 게임 플레이 설정


class Game:
    def __init__(self):
        # 게임 초기화
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption("TIKTOK GAME")        

        #print(pygame.font.get_fonts())  # 사용 가능한 시스템 폰트 목록 출력 - 한글 지원x

        # 게임 변수 설정
        # - 게임 시간, 게임 점수 등..
        
        self.state = GAME_STATE_INIT  

        self.SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) #화면 크기 설정
        #self.SCREEN_SURFACE = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock() 
        self.FPS = FPS
        self.COLOR_BLUE = (24, 154, 211)
        self.COLOR_BLACK = (0, 0, 0)
        self.COLOR_WHITE = (255, 255, 255)        
        self.main_font_30 = pygame.font.Font("game/res/font/NanumBarunGothic.ttf", 30)   
        self.main_font_20 = pygame.font.Font("game/res/font/NanumBarunGothic.ttf", 20) 
        self.main_font_15 = pygame.font.Font("game/res/font/NanumBarunGothic.ttf", 15) 
        self.main_font_11 = pygame.font.Font("game/res/font/NanumBarunGothic.ttf", 11) 
        #text = main_font.render("Test Text", True, COLOR_BLACK)     # 문자열, antialias, 글자색

        self.auto_player_spawn_term = 500 # 160      자동 플레이어 생성 주기
        self.auto_player_spawn_time = 0   #          자동 플레이어 생성 딜레이 시간

        # sprite group 설정
        self.sprite_group = pygame.sprite.Group()
        self.left_group = pygame.sprite.Group()
        self.right_group = pygame.sprite.Group()
        self.tile_group = pygame.sprite.Group()
        self.ui_group = pygame.sprite.Group()

        self.tile_size = (50, 50)
        self.soldier_size = (60, 60)
        self.castle_size = (100, 180)


        # 리소스 불러오기
        import_soldier_left(self.soldier_size)
        import_soldier_right(self.soldier_size)
        
        import_castle_left(self.castle_size)
        import_castle_right(self.castle_size)

        import_ground_images(self.tile_size)

        # 효과음 로드


      
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

        # castle 생성
        new_left_castle = characters.CastleSprite(size=self.castle_size, position=LEFT_CASTLE_POSITION, movement=(0,0), group='left',
                                                 hp=3000, power=0, name='left castle', images=castle_images_left, game=self)
        self.left_group.add(new_left_castle)
        self.sprite_group.add(new_left_castle)

        new_right_castle = characters.CastleSprite(size=self.castle_size, position=RIGHT_CASTLE_POSITION, movement=(0,0), group='right',
                                                 hp=3000, power=0, name='right castle', images=castle_images_right, game=self)
        self.right_group.add(new_right_castle)
        self.sprite_group.add(new_right_castle)

   


    async def game_event_loop(self, event_queue):
        current_time = 0
        while True:
            #print('game_event_loop')
            last_time, current_time = current_time, time.time()
            await asyncio.sleep(1 / FPS - (current_time - last_time))  # tick
            event = pygame.event.poll()
            if event.type != pygame.NOEVENT:
                await event_queue.put(event)



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
                pass



            # ================================== START ==================================
            if self.state == GAME_STATE_START:
                pass


            
            # ================================== PLAYING ==================================
            if self.state == GAME_STATE_PLAYING:

                # 승,패 확인
                


                # 유닛 자동 생성 
                if self.auto_player_spawn_time == self.auto_player_spawn_term:
                    #print("[SPAWN PLAYER AUTO]")
                    new_left_player = characters.SoldierSprite(size=self.soldier_size, position=LEFT_SPAWN_POSITION, movement=(1,0), group='left', 
                                                            hp=100, power=5, name='left_%d'%auto_player_num, images=solider_images_left, game=self)
                    self.left_group.add(new_left_player)
                    self.sprite_group.add(new_left_player)
                    
                    # new_right_player = characters.SoldierSprite(size=self.soldier_size, position=RIGHT_SPAWN_POSITION, movement=(-1,0), group='right', 
                    #                                             hp=100, power=5, name='right_%d'%auto_player_num, images=soldier_images_right, game=self)
                    # self.right_group.add(new_right_player)
                    # self.sprite_group.add(new_right_player)
                    
                    self.auto_player_spawn_time = 0
                    auto_player_num += 1                
                else:
                    self.auto_player_spawn_time += + 1
            # ==========================================================================


            # ================================== OVER ==================================
            if self.state == GAME_STATE_OVER:
                pass



            # <화면 그리기>
            # 모든 Sprite update
            self.sprite_group.update(mt, self)
            
            # 배경색
            self.SCREEN.fill(self.COLOR_BLUE) 

            # 설명 UI
            desc_rect_x = SCREEN_WIDTH * 0.04
            desc_rect_y = desc_rect_x
            desc_rect_width = SCREEN_WIDTH * 0.43
            desc_rect_fill = pygame.draw.rect(self.SCREEN, (255, 255, 228), [desc_rect_x+3, desc_rect_y+3, desc_rect_width-6, desc_rect_width-6], 
                                        border_radius=0, border_top_left_radius=5, border_top_right_radius=5, border_bottom_left_radius=5, border_bottom_right_radius=5)
            desc_rect_border = pygame.draw.rect(self.SCREEN, (153, 56, 0), [desc_rect_x, desc_rect_y, desc_rect_width, desc_rect_width], 
                                        width=3, border_radius=0, border_top_left_radius=10, border_top_right_radius=10, border_bottom_left_radius=10, border_bottom_right_radius=10)

            # 참가 설명 텍스트
            text_join_title = self.main_font_11.render("[ 참가 ]", True, self.COLOR_BLACK)
            text_join_title_rect = text_join_title.get_rect()
            text_join_title_rect.centerx = desc_rect_fill.centerx
            text_join_desc = self.main_font_11.render("원하는 진영 이름 채팅으로 입력", True, self.COLOR_BLACK)
            text_join_desc_rect = text_join_desc.get_rect()
            text_join_desc_rect.centerx = desc_rect_fill.centerx            
            self.SCREEN.blit(text_join_title, (text_join_title_rect.x, desc_rect_y + 15))
            self.SCREEN.blit(text_join_desc, (text_join_desc_rect.x, desc_rect_y + 35))
            
            # 유닛 추가 설명 텍스트
            text_join_title = self.main_font_11.render("[ 유닛 추가 ]", True, self.COLOR_BLACK)
            text_join_title_rect = text_join_title.get_rect()
            text_join_title_rect.centerx = desc_rect_fill.centerx
            text_join_desc = self.main_font_11.render("하트 5개당 1유닛", True, self.COLOR_BLACK)
            text_join_desc_rect = text_join_desc.get_rect()
            text_join_desc_rect.centerx = desc_rect_fill.centerx            
            self.SCREEN.blit(text_join_title, (text_join_title_rect.x, desc_rect_y + 65))
            self.SCREEN.blit(text_join_desc, (text_join_desc_rect.x, desc_rect_y + 85))



            # ================================== READY ==================================
            if self.state == GAME_STATE_READY:
                pass



            # ================================== START ==================================
            if self.state == GAME_STATE_START:
                pass




            # ================================== OVER ==================================
            if self.state == GAME_STATE_OVER:
                pass




            # 객체별로 필요한 그림 그려주기
            for sprite in self.sprite_group:
                sprite.draw()
            
            # 모든 sprite 화면에 그려주기
            self.sprite_group.draw(self.SCREEN)            
            
            #pygame.display.flip()
            pygame.display.update()


    
    async def handle_events(self, event_queue):
        isLeft = True
        current_time = 0
        while True:
            last_time, current_time = current_time, time.time()
            await asyncio.sleep(10 / FPS - (current_time - last_time))  # tick
            event = await event_queue.get()
            #print("event", event)
            if event.type == pygame.QUIT:
                break
            elif event.type == EVENT_NEW_USER_LEFT:                
                if isLeft == True:
                    new_left_player = characters.SoldierSprite(size=self.soldier_size, position=LEFT_SPAWN_POSITION, movement=(1,0), group='left', 
                                                            hp=100, power=1, name='left_soldier', images=solider_images_left, game=self)
                    self.left_group.add(new_left_player)
                    self.sprite_group.add(new_left_player)
                    isLeft = False
                else:
                    new_right_player = characters.SoldierSprite(size=self.soldier_size, position=RIGHT_SPAWN_POSITION, movement=(-1,0), group='right', 
                                                            hp=100, power=1, name='right_soldier', images=soldier_images_right, game=self)
                    self.right_group.add(new_right_player)
                    self.sprite_group.add(new_right_player)
                    isLeft = True
            else:
                pass
                #print("event", event)
        asyncio.get_event_loop().stop()



    async def connect_to_server(self, event_queue): 
        print("connect_to_server")
        async with websockets.connect("ws://192.168.219.106:30001") as websocket:
            #await websocket.send("Hi server. I'm client" );          
            current_time = 0
            while True:
                last_time, current_time = current_time, time.time()
                await asyncio.sleep(1 / FPS - (current_time - last_time))  # tick
                
                if self.state != GAME_STATE_PLAYING:
                    continue
                
                now = datetime.datetime.now()
                msg_rcv = await websocket.recv(); 
                print('[%s] %s' % (now, msg_rcv))                
                new_event = pygame.event.Event(EVENT_NEW_USER_LEFT, message=msg_rcv)    
                await event_queue.put(new_event)  
               

    def run(self):
        loop = asyncio.get_event_loop()
        event_queue = asyncio.Queue()

        pygame_task = asyncio.ensure_future(self.game_event_loop(event_queue))
        animation_task = asyncio.ensure_future(self.animation())
        event_task = asyncio.ensure_future(self.handle_events(event_queue))
        socket_task = asyncio.ensure_future(self.connect_to_server(event_queue))

        try:
            loop.run_forever()
        except KeyboardInterrupt:
            pass
        finally:
            pygame_task.cancel()
            animation_task.cancel()
            event_task.cancel()
            socket_task.cancel()

        pygame.quit()


    def send_event(self, event):
        print("[recevie event]:%s" % event)
        pygame.event.post(EVENT_NEW_USER_LEFT)


if __name__ == '__main__':
    game = Game()
    game.run()