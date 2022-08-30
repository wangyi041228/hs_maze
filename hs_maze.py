import asyncio
import os
import threading
from ctypes import windll
from tkinter import *
from tkinter.ttk import *
from PIL import Image, ImageTk
import sys
import winreg

error_lines = ''
try:
    _win_v = sys.getwindowsversion()
    if _win_v.major == 6 and _win_v.minor == 1:
        windll.user32.SetProcessDPIAware()
    else:
        windll.shcore.SetProcessDpiAwareness(2)
except Exception as e:
    error_lines += str(e) + '\n'

hs_dir = ''
try:
    reg_pos = r'SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\Hearthstone'
    handle = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_pos)
    hs_dir, _type = winreg.QueryValueEx(handle, 'InstallLocation')
    winreg.CloseKey(handle)
except Exception as e:
    error_lines += str(e) + '\n'
hs_dir += '\\Logs\\'
if not os.path.exists(hs_dir):
    error_lines += '找不到Log文件夹。关闭工具，把所有文件移动到\nHearthstone.exe所在文件夹后再试。'
HS_LOG_PATH = hs_dir + 'Power.log'

APPDATA_DIR = os.getenv('LOCALAPPDATA')
log_config_p0 = APPDATA_DIR + '\\Blizzard\\Hearthstone\\'
log_config_path = APPDATA_DIR + r'\Blizzard\Hearthstone\log.config'
if not os.path.exists(log_config_path):
    try:
        with open(log_config_path, 'w', encoding='utf-8') as ff:
            print("""[Achievements]
LogLevel=1
FilePrinting=True
ConsolePrinting=False
ScreenPrinting=False
Verbose=False
[Arena]
LogLevel=1
FilePrinting=True
ConsolePrinting=False
ScreenPrinting=False
Verbose=False
[FullScreenFX]
LogLevel=1
FilePrinting=True
ConsolePrinting=False
ScreenPrinting=False
Verbose=False
[LoadingScreen]
LogLevel=1
FilePrinting=True
ConsolePrinting=False
ScreenPrinting=False
Verbose=False
[Power]
LogLevel=1
FilePrinting=True
ConsolePrinting=False
ScreenPrinting=False
Verbose=True""", file=ff)
            error_lines += '已创建log.config，需重启游戏。\n'
    except Exception as e:
        error_lines += str(e) + '\n'
offsets = ((23, 25), (89, 25), (155, 25), (155, 91), (155, 157), (89, 157), (23, 157), (23, 91))
id2d = {
    'id=8': 0,  # 上
    'id=9': 1,  # 右
    'id=10': 2,  # 左
    'id=11': 3,  # 下
}
ca2d = {
    'AV_760t0': 0,
    'AV_760t1': 1,
    'AV_760t2': 2,
    'AV_760t3': 3,
    'AV_760t4': 4,
    'AV_760t5': 5,
    'AV_760t6': 6,
    'AV_760t7': 7,
}
if not error_lines:
    error_lines = '（检测正常）\n'
sample_map = [
    [[1, 1, 0, 1, 1, 1, 1, 1, 0, 1, ],
     [1, 1, 0, 1, 0, 0, 0, 1, 0, 1, ],
     [1, 0, 0, 1, 0, 1, 0, 0, 0, 1, ],
     [0, 0, 0, 1, 0, 1, 1, 1, 1, 1, ],
     [1, 0, 0, 1, 0, 0, 0, 0, 0, 1, ],
     [1, 1, 1, 1, 0, 0, 1, 0, 0, 1, ],
     [1, 1, 1, 0, 0, 0, 0, 0, 0, 1, ],
     [1, 1, 1, 1, 0, 0, 0, 1, 1, 1, ]],

    [[1, 4, 4, 4, 1, 1, 2, 1, 0, 1, ],
     [1, 4, 4, 4, 4, 1, 2, 1, 0, 1, ],
     [1, 0, 0, 4, 4, 1, 2, 1, 0, 1, ],
     [0, 0, 0, 4, 4, 0, 0, 1, 0, 1, ],
     [1, 0, 0, 4, 4, 1, 1, 1, 0, 1, ],
     [1, 4, 4, 4, 4, 0, 1, 1, 0, 1, ],
     [1, 4, 4, 4, 1, 0, 0, 0, 0, 1, ],
     [1, 1, 1, 1, 1, 1, 1, 1, 0, 1, ]],

    [[1, 1, 0, 0, 0, 0, 1, 1, 1, 1, ],
     [1, 0, 0, 0, 0, 1, 1, 1, 1, 1, ],
     [1, 0, 0, 0, 1, 1, 1, 1, 1, 1, ],
     [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, ],
     [1, 0, 0, 0, 0, 1, 1, 1, 1, 1, ],
     [1, 0, 0, 0, 0, 0, 0, 1, 1, 1, ],
     [1, 1, 1, 1, 0, 0, 0, 1, 1, 1, ],
     [1, 1, 1, 1, 1, 0, 0, 1, 1, 1, ]],

    [[1, 0, 1, 2, 0, 1, 0, 0, 1, 1, ],
     [1, 0, 1, 2, 1, 1, 1, 0, 0, 1, ],
     [1, 0, 1, 2, 1, 2, 1, 1, 0, 1, ],
     [0, 0, 2, 2, 1, 2, 1, 1, 0, 1, ],
     [1, 0, 1, 2, 2, 2, 2, 1, 0, 1, ],
     [1, 0, 1, 1, 1, 1, 2, 0, 0, 1, ],
     [1, 0, 0, 0, 0, 1, 1, 1, 1, 1, ],
     [1, 1, 1, 1, 0, 1, 0, 0, 0, 1, ]],

    [[4, 4, 0, 1, 1, 0, 0, 1, 1, 1, ],
     [1, 0, 0, 1, 1, 0, 0, 1, 1, 1, ],
     [1, 0, 0, 1, 0, 0, 0, 1, 1, 1, ],
     [0, 0, 0, 1, 0, 0, 1, 1, 1, 1, ],
     [1, 0, 0, 1, 1, 0, 0, 1, 1, 1, ],
     [1, 1, 1, 1, 1, 0, 0, 1, 1, 1, ],
     [1, 1, 1, 0, 0, 0, 0, 0, 0, 1, ],
     [1, 1, 1, 1, 0, 0, 0, 0, 0, 1, ]],

    [[1, 1, 0, 0, 0, 0, 1, 1, 1, 1, ],
     [1, 0, 0, 0, 0, 1, 1, 1, 1, 1, ],
     [1, 0, 0, 0, 1, 1, 1, 1, 1, 1, ],
     [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, ],
     [1, 0, 0, 0, 0, 1, 1, 1, 1, 1, ],
     [1, 0, 0, 0, 0, 0, 0, 1, 1, 1, ],
     [1, 1, 1, 1, 0, 0, 0, 0, 1, 1, ],
     [1, 1, 1, 1, 1, 0, 0, 0, 1, 1, ]],

    [[0, 0, 0, 0, 0, 0, 0, 0, 0, 1, ],
     [1, 1, 1, 0, 1, 1, 1, 1, 1, 1, ],
     [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, ],
     [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, ],
     [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, ],
     [1, 1, 1, 1, 1, 1, 1, 0, 1, 1, ],
     [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, ],
     [1, 1, 1, 1, 0, 1, 1, 1, 1, 1, ]],

    [[0, 0, 0, 0, 0, 0, 0, 0, 0, 1, ],
     [1, 1, 1, 1, 1, 1, 0, 1, 1, 1, ],
     [1, 0, 0, 1, 1, 1, 0, 1, 1, 1, ],
     [0, 0, 0, 1, 1, 1, 0, 1, 1, 1, ],
     [1, 0, 0, 1, 1, 1, 0, 1, 1, 1, ],
     [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, ],
     [1, 1, 1, 1, 1, 1, 0, 1, 1, 1, ],
     [1, 1, 1, 1, 1, 1, 0, 1, 0, 1, ]]
]


class MainWindow(Tk):
    def __init__(self):
        global error_lines
        super().__init__()
        self.title('迷宫辅助 右击窗口有说明')
        self.geometry('310x310+1200+400')
        self.wm_attributes('-topmost', True)
        self.loop = None
        self.x = 0
        self.y = 0
        self.offset = (0, 0)
        self.around = [0] * 4
        self.birth_tf = [True] * 8
        self.birth_t = 8
        with Image.open('me.png') as im:
            self.me = im.convert('RGBA')
        with Image.open('map1.png') as im:
            self.map1 = im.convert('RGBA')
        with Image.open('map2.png') as im:
            self.map2 = im.convert('RGBA')
        with Image.open('map3.png') as im:
            self.map3 = im.convert('RGBA')
        with Image.open('map4.png') as im:
            self.map4 = im.convert('RGBA')
        with Image.open('map5.png') as im:
            self.map5 = im.convert('RGBA')
        with Image.open('map6.png') as im:
            self.map6 = im.convert('RGBA')
        self.maps = [self.map1, self.map2, self.map3, self.map4, self.map5, self.map6]
        self.map = self.map1
        self.vision = None
        self.vision_ps = None
        self.Label = Label(self, image=None)
        self.Label.pack()
        self.Label.place(x=-1, y=-1)
        button_lines = error_lines + '\n单击按钮开始检测\n出村后切换出生点'
        self.Button1 = Button(self, text=button_lines, command=self.main_start)
        self.Button1.pack()
        self.Button1.place()

        self.Menu = Menu(self, tearoff=False)
        self.Menu.add_cascade(label='进入佣兵之书：凯瑞尔界面，点击毛笔右侧的扇形花纹进入谜题。')
        self.Menu.add_cascade(label='沿着蓝线朝对应的空位使用英雄技能移动。')
        self.Menu.add_cascade(label='树木拦路时，技能点脸停下脚步，用斧子砍树。')
        self.Menu.add_cascade(label='炸药附近的红✖是以后抄近路用的，别浪费炸药。')
        self.Menu.add_cascade(label='走到上方红✖前对特殊墙壁使用炸药，通关新手村。')
        self.Menu.add_cascade(label='观察前方地形，特别是墙壁，在下方菜单中切换并确认出生点。')
        self.Menu.add_cascade(label='沿着蓝线找到炸药，炸开第二道门。')
        self.Menu.add_cascade(label='根据窗口标题栏的坐标，找到在(0,0)的鲍勃，给他5金币。')
        self.Menu.add_cascade(label='获得下方树林中的金币和炸药，把金币给鲍勃。')
        self.Menu.add_cascade(label='直接打开map6.png查看，推荐地图正南、正北、东南和东北的迷宫。')
        self.Menu.add_cascade(label='沿着蓝线找到其他迷宫，对准两个红✖使用炸药，找到炸药进入内层。')
        self.Menu.add_cascade(label='迷宫外壁是看不出区别的，瞄准了一炸就开。')
        self.Menu.add_cascade(label='每个后续迷宫提供5个金币和5个炸药，其中3个炸药是冗余的。')
        self.Menu.add_cascade(label='自信的话，每次带回5个金币和1个炸药找鲍勃，交金币找下个迷宫。')
        self.Menu.add_cascade(label='不然带着炸药先开其他迷宫的门。累计给鲍勃20金币通关。')
        self.Menu.add_separator()
        self.Menu.add_cascade(label='提醒：手牌上限是10。不要对鲍勃用炸药。前期不能浪费炸药。')
        self.Menu.add_cascade(label='以地图正东（游戏内东北）为x轴正方向。')
        self.Menu.add_cascade(label='以地图正南（游戏内西北）为y轴正方向。')
        self.Menu.add_cascade(label='移动后刷新视野，适应窗口大小')
        self.Menu.add_separator()
        self.seed_menu = Menu(self.Menu, tearoff=0)
        self.seed_var = IntVar(value=0)
        for i, lb in enumerate(['1 地图西北 游戏正西 入口(-40, 50)',
                                '2 地图正北 游戏西北 入口(-24, 88) 推荐',
                                '3 地图东北 游戏正北 入口(63, 40) 推荐',
                                '4 地图正东 游戏东北 入口(40, -13) 推荐',
                                '5 地图东南 游戏正东 入口(40, -50) 推荐',
                                '6 地图正南 游戏东南 入口(18, -40) 推荐',
                                '7 地图西南 游戏正南 入口(-92, -54)',
                                '8 地图正西 游戏西南 入口(-69, -26)']):
            self.seed_menu.add_radiobutton(label=lb, command=self.set_seed, variable=self.seed_var, value=i)
        self.Menu.add_cascade(label='出新手村后试出生点', menu=self.seed_menu)
        self.Menu.add_separator()
        self.Menu.add_cascade(label='打开日志配置路径，手动删除log.config', command=self.pop_dir)
        self.Menu.add_separator()
        self.Menu.add_cascade(label='第3版')
        self.bind('<Button-3>', self.popupmenu)
        self.update_vision()
        self.mainloop()

    def popupmenu(self, event):
        try:
            self.Menu.post(event.x_root, event.y_root)
        finally:
            self.Menu.grab_release()

    def pop_dir(event):
        os.startfile(log_config_p0)

    def set_seed(self):
        seed = self.seed_var.get()
        self.map = self.maps[5]
        self.offset = offsets[seed]
        self.update_vision()

    def get_loop(self, loop):
        self.loop = loop
        asyncio.set_event_loop(self.loop)
        self.loop.run_forever()

    def main_start(self):
        self.Button1.destroy()
        coroutine1 = self.handler()
        new_loop = asyncio.new_event_loop()
        t = threading.Thread(target=self.get_loop, args=(new_loop,))
        t.daemon = True
        t.start()
        asyncio.run_coroutine_threadsafe(coroutine1, new_loop)

    def update_vision(self):
        if self.offset != (0, 0):
            px = self.offset[0] + self.x - 92
            py = 100 - self.offset[1] - self.y
            self.title(f'迷宫辅助 ({px}, {py})')
        _x = (self.offset[0] + self.x) * 25
        _y = (self.offset[1] + self.y) * 25
        _box = (425 + _x, 225 + _y, 850 + _x, 650 + _y)
        _im = self.map.crop(_box).rotate(45).crop((57, 57, 367, 367))
        _im.paste(self.me, (141, 141), self.me)
        if self.loop:
            _h = min(self.winfo_height(), self.winfo_width())
            _im = _im.resize((_h, _h), Image.LANCZOS)
        self.vision = _im
        self.vision_ps = ImageTk.PhotoImage(self.vision)
        self.Label.configure(image=self.vision_ps)
        self.Label.image = self.vision_ps

    async def handler(self):
        last_pos = 0
        # state = 0
        creating = False
        changing = False
        while True:
            try:
                with open(HS_LOG_PATH, 'r', encoding='utf-8') as f:
                    f.seek(last_pos)
                    while True:
                        txt = f.read()
                        last_pos = f.tell()
                        last_size = last_pos
                        if txt:
                            for line in txt.split('\n'):
                                if '() - ' not in line:
                                    continue
                                head_body_other = line.split('() - ', 1)
                                head = head_body_other[0].split(' ')[-1]
                                body = head_body_other[1]
                                body_strip = body.lstrip()
                                space = len(body) - len(body_strip)
                                body_list = body_strip.split(' ')
                                # print(head, space, body_list)
                                if head == 'PowerTaskList.DebugPrintPower':
                                    if space == 4:
                                        if body_list[0] == 'CREATE_GAME':
                                            creating = True
                                        else:
                                            creating = False
                                    if space == 12 and len(body_list) == 2:
                                        if body_list[0] == 'tag=STATE':
                                            if body_list[1] == 'value=RUNNING':
                                                creating = False
                                        elif body_list[0] == 'tag=937' and creating:
                                            if body_list[1] == 'value=4827':
                                                self.title('迷宫辅助 右击窗口有说明')
                                                self.x = 0
                                                self.y = 0
                                                self.offset = (0, 0)
                                                self.around = [0] * 4
                                                self.map = self.maps[0]
                                                self.birth_tf = [True] * 8
                                                self.birth_t = 8
                                                self.update_vision()
                                # elif head == 'GameState.DebugPrintPower':
                                #     if body[0] == 'BLOCK_START' and body[1] == 'BlockType=PLAY':
                                #         if body[6] == 'cardId=AV_760':
                                #             state = 1
                                #         elif body[6] == 'cardId=AV_761t2':
                                #             state = 2
                                #         elif body[6] == 'cardId=AV_761t3':
                                #             state = 3
                                #             if body[-3] == 'cardId=AV_760t3':
                                #                 action = '砍树'
                                #                 pos = body[-6]
                                #                 direction = id2d.get(pos)
                                # elif body[0] == 'BLOCK_END':
                                #     state = 0
                                elif head == 'GameState.SendChoices':
                                    if 'm_chosenEntities[0]=[entityName=' in body_list[0]:
                                        if body_list[1] == 'id=8':
                                            self.y -= 1
                                        elif body_list[1] == 'id=9':
                                            self.x += 1
                                        elif body_list[1] == 'id=10':
                                            self.x -= 1
                                        elif body_list[1] == 'id=11':
                                            self.y += 1
                                        # print('坐标', self.x, self.y)
                                        if self.x == 20:
                                            if self.y == 12:
                                                self.map = self.maps[1]
                                                self.offset = (0, 0)
                                        elif self.x == -3:
                                            if self.y == 16:
                                                self.map = self.maps[2]
                                                self.offset = (0, 0)
                                        elif self.x == 10:
                                            if self.y == -6:
                                                self.map = self.maps[3]
                                                self.offset = (0, 0)
                                        elif self.x == 1:
                                            if self.y == 23:
                                                self.map = self.maps[4]
                                                self.offset = (0, 0)
                                        # elif self.x == 18:
                                        #     if self.y == 2:
                                        #         self.map = self.maps[5]
                                        #         self.offset = offsets[self.seed_var.get()]
                                        self.update_vision()
                                elif head == 'GameState.DebugPrintPower':
                                    if 'CHANGE_ENTITY' in body_list[0]:
                                        changing = True
                                        new_card = ca2d[body_list[-1][7:]]
                                        pos = id2d[body_list[-6]]
                                        self.around[pos] = new_card
                                else:
                                    if changing:
                                        changing = False
                                        if self.birth_t > 1 and 20 <= self.x <= 27 and 0 <= self.y <= 5:
                                            _x = self.x - 19
                                            _y = self.y + 1
                                            for birth_n in range(8):
                                                if self.birth_tf[birth_n]:
                                                    for pos_i in range(4):
                                                        if pos_i == 0:
                                                            __x, __y = _x, _y - 1
                                                        elif pos_i == 1:
                                                            __x, __y = _x + 1, _y
                                                        elif pos_i == 2:
                                                            __x, __y = _x - 1, _y
                                                        elif pos_i == 3:
                                                            __x, __y = _x, _y + 1
                                                        if self.around[pos_i] != sample_map[birth_n][__y][__x]:
                                                            self.birth_tf[birth_n] = False
                                                            self.birth_t -= 1
                                                            if self.birth_t == 1:
                                                                _c = self.birth_tf.index(True)
                                                                self.map = self.maps[5]
                                                                self.seed_var.set(_c)
                                                                self.offset = offsets[_c]
                                                                self.update_vision()
                                                            break
                        else:
                            try:
                                now_size = os.path.getsize(HS_LOG_PATH)
                                if now_size < last_size:
                                    f.seek(0)
                            except Exception as ee:
                                print(ee)
                        await asyncio.sleep(0.005)
                await asyncio.sleep(0.005)
            except Exception as ee:
                print(ee)


if __name__ == "__main__":
    MainWindow()
