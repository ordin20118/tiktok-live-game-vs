import pygame
import pygame.mixer
import websockets
import websocket
import asyncio
import threading
import time
import datetime
from websocket_client import client
from game.sprite import characters
from game.dataload import *

FPS = 60

# 스크린 전체 크기 지정
SCREEN_WIDTH = 475
SCREEN_HEIGHT = 844

LEFT_CASTLE_POSITION = (-18, 407.5)
RIGHT_CASTLE_POSITION = (390, 407.5)

LEFT_SPAWN_POSITION = (50, 527.5)
RIGHT_SPAWN_POSITION = (400, 527.5)

# 커스텀 이벤트 생성
EVENT_NEW_USER_LEFT = pygame.USEREVENT+1
EVENT_NEW_USER_RIGHT = pygame.USEREVENT+1
new_user_left_event = pygame.event.Event(EVENT_NEW_USER_LEFT, message="New left user.")
new_user_right_event = pygame.event.Event(EVENT_NEW_USER_RIGHT, message="New right user.")

class Game:
    def __init__(self):
        # 게임 초기화
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption("WAR GAME")
        

        # 게임 변수 설정
        # - 게임 시간, 게임 점수 등..

        self.SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) #화면 크기 설정
        self.SCREEN_SURFACE = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock() 
        self.FPS = 60
        self.BLUE = (0, 0, 255)

        # sprite group 설정
        self.sprite_group = pygame.sprite.Group()
        self.left_group = pygame.sprite.Group()
        self.right_group = pygame.sprite.Group()
        self.stone_group = pygame.sprite.Group()

        self.soldier_size = (60, 60)
        self.castle_size = (100, 180)


        # 리소스 불러오기
        import_soldier_left(self.soldier_size)
        import_soldier_right(self.soldier_size)
        
        import_castle_left(self.castle_size)
        import_castle_right(self.castle_size)

        # 효과음 로드

        # 소켓 연결        
        #asyncio.run(self.connect_to_server())
        #asyncio.get_event_loop().run_in_executor(None, self.connect_to_server())
        #asyncio.get_event_loop().run_until_complete(self.connect_to_server);
        
        # thr=threading.Thread(target=self.connect_to_server, args=())
        # thr.Daemon=True
        # thr.start()

        #self.start_websocket()

        
    
    def start_websocket(self):
        wsapp = websocket.WebSocketApp("ws://192.168.219.106:30001", on_open=self.on_open, on_message=self.on_message, on_close=self.on_close)
        wsapp.run_forever()

    def on_open(ws):
        ws.send("hi")
    
    def on_message(ws, message):
        def run(*args):
            print(message)
            #ws.close()
            print("Message received...")

        threading.Thread(target=run).start()

    def on_close(ws, close_status_code, close_msg):
        print(">>>>>>CLOSED")

    def run(self):

        # 생성된 player를 그룹에 넣기
        auto_player_spawn_term = 100 # 160
        auto_player_spawn_time = 0

        self.is_running = True


        # castle 생성
        new_left_castle = characters.CastleSprite(size=self.castle_size, position=LEFT_CASTLE_POSITION, movement=(0,0), group='left',
                                                 hp=5000, power=0, name='left castle', images=castle_images_left, game=self)
        self.left_group.add(new_left_castle)
        self.sprite_group.add(new_left_castle)

        new_right_castle = characters.CastleSprite(size=self.castle_size, position=RIGHT_CASTLE_POSITION, movement=(0,0), group='right',
                                                 hp=5000, power=0, name='right castle', images=castle_images_right, game=self)
        self.right_group.add(new_right_castle)
        self.sprite_group.add(new_right_castle)



        auto_player_num = 1
        while self.is_running: #게임 루프
            

            # 변수 업데이트
            #30 FPS (초당 프레임 수) 를 위한 딜레이 추가, 딜레이 시간이 아닌 목표로 하는 FPS 값
            mt = self.clock.tick(self.FPS) / 1000 # 1000dmf 나누어줘서 초단위로 변경하여 반환

            if auto_player_spawn_time == auto_player_spawn_term:
                new_left_player = characters.SoldierSprite(size=self.soldier_size, position=LEFT_SPAWN_POSITION, movement=(1,0), group='left', hp=100, power=3, name='left_%d'%auto_player_num, images=solider_images_left, game=self)
                self.left_group.add(new_left_player)
                self.sprite_group.add(new_left_player)
                
                new_right_player = characters.SoldierSprite(size=self.soldier_size, position=RIGHT_SPAWN_POSITION, movement=(-1,0), group='right', hp=100, power=1, name='right_%d'%auto_player_num, images=soldier_images_right, game=self)
                self.right_group.add(new_right_player)
                self.sprite_group.add(new_right_player)
                auto_player_spawn_time = 0
                auto_player_num += 1
                
            else:
                auto_player_spawn_time = auto_player_spawn_time + 1
                

            # 이벤트 처리
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == EVENT_NEW_USER_LEFT:
                    print("[이벤트 정상 수신됨]")

            # 화면 그리기
            
            # all_sprites 그룹안에 든 모든 Sprite update
            self.sprite_group.update(mt, self)
            
            # 배경색
            self.SCREEN.fill(self.BLUE) 

            # 객체별로 필요한 그림 그려주기
            for sprite in self.sprite_group:
                sprite.draw()
            
            # 모든 sprite 화면에 그려주기
            self.sprite_group.draw(self.SCREEN)
            pygame.display.update() #모든 화면 그리기 업데이트

    def send_event(self, event):
        print("[recevie event]:%s" % event)
        pygame.event.post(EVENT_NEW_USER_LEFT)

    async def connect_to_server(self): 
        print("connect_to_server")
        async with websockets.connect("ws://192.168.219.106:30001") as websocket:
            await websocket.send("Hi server. I'm client" );          
            current_time = 0
            while True:
                last_time, current_time = current_time, time.time()
                await asyncio.sleep(1 / FPS - (current_time - last_time))  # tick
                now = datetime.datetime.now()
                msg_rcv = await websocket.recv(); 
                print('[%s] %s' % (now, msg_rcv)) 
        


if __name__ == '__main__':
    game = Game()
    game.run()