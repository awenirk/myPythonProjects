from panda3d.core import WindowProperties

key_switch_camera = "r"
key_switch_mode = "f"
key_toggle_mouse = 'c'

key_forward = "w"
key_left = "a"
key_back = "s"
key_right = "d"
key_up = "space"
key_down = "shift"

key_turn_left = "arrow_left"
key_turn_right = "arrow_right"
key_turn_up = "arrow_up"
key_turn_down = "arrow_down"

save_map = 'k'
load_map = 'l'

key_add_block = 'mouse1'
key_del_block = 'mouse3'

class Hero():
    def __init__(self, pos, land):
        self.land = land
        self.mode = True  # режим спостерігача
        self.hero = loader.loadModel('smiley')
        self.hero.setColor(1, 0.5, 0)
        self.hero.setScale(0.4)
        self.hero.setPos(pos)
        self.hero.reparentTo(render)
        self.saved_hpr = None
        self.cameraOn = False  # Початковий режим — від першої особи
        self._mouse_look_active = False  # Поворот мишкою вимкнений
        self.cameraUp()  # Початковий вид — від першої особи
        self.accept_events()

    def cameraBind(self):
        """Прив'язує камеру до героя в режимі від третьої особи."""
        base.disableMouse()
        base.camera.reparentTo(self.hero)  # Прив'язуємо камеру до героя
        base.camera.setPos(0, 9, 3)  # Камера позаду і трохи вище героя
        base.camera.setHpr(180, 0, 0)  # Камера дивиться вперед (з урахуванням повороту героя)
        self.stop_mouse_look()
        self.cameraOn = True

    def cameraUp(self):
        """Прив'язує камеру до героя в режимі від першої особи."""
        base.disableMouse()
        base.camera.reparentTo(self.hero)  # Прив'язуємо камеру до героя
        base.camera.setPos(0, 0, 1)  # Камера на рівні очей героя
        base.camera.setHpr(180, 0, 0)  # Камера дивиться вперед (з урахуванням повороту героя)
        self.stop_mouse_look()
        self.cameraOn = False

    def look_at(self, angle):
        x_from = round(self.hero.getX())
        y_from = round(self.hero.getY())
        z_from = round(self.hero.getZ())

        dx, dy = self.check_dir(angle)
        x_to = x_from + dx
        y_to = y_from + dy
        return x_to, y_to, z_from
    def just_move(self, angle):
        '''перемещается в нужные координаты в любом случае'''
        pos = self.look_at(angle)
        self.hero.setPos(pos)
    def move_to(self, angle):
        if self.mode:
            self.just_move(angle)
        else:
            self.try_move(angle)
    def check_dir(self,angle):
        ''' возвращает округленные изменения координат X, Y, 
        соответствующие перемещению в сторону угла angle.
        Координата Y уменьшается, если персонаж смотрит на угол 0,
        и увеличивается, если смотрит на угол 180.    
        Координата X увеличивается, если персонаж смотрит на угол 90,
        и уменьшается, если смотрит на угол 270.    
            угол 0 (от 0 до 20)      ->        Y - 1
            угол 45 (от 25 до 65)    -> X + 1, Y - 1
            угол 90 (от 70 до 110)   -> X + 1
            от 115 до 155            -> X + 1, Y + 1
            от 160 до 200            ->        Y + 1
            от 205 до 245            -> X - 1, Y + 1
            от 250 до 290            -> X - 1
            от 290 до 335            -> X - 1, Y - 1
            от 340                   ->        Y - 1  '''
        if angle >= 0 and angle <= 20:
            return (0, -1)
        elif angle <= 65:
            return (1, -1)
        elif angle <= 110:
            return (1, 0)
        elif angle <= 155:
            return (1, 1)
        elif angle <= 200:
            return (0, 1)
        elif angle <= 245:
            return (-1, 1)
        elif angle <= 290:
            return (-1, 0)
        elif angle <= 335:
            return (-1, -1)
        else:
            return (0, -1)
    def try_move(self, angle):
        pos = self.look_at(angle)
        if self.land.isEmpty(pos):
            pos = self.land.findHighestEmpty(pos)
            self.hero.setPos(pos)
        else:
            pos = pos[0], pos[1], pos[2] + 1
            if self.land.isEmpty(pos):
                self.hero.setPos(pos)

    def changeView(self):
        """Перемикає між видом від першої та третьої особи."""
        if self.cameraOn:
            self.cameraUp()
        else:
            self.cameraBind()
    def switch_mode(self):
        self.mode = not self.mode

    def forward(self):
        angle =(self.hero.getH()) % 360
        self.move_to(angle)
    def back(self):
        angle = (self.hero.getH()+180) % 360
        self.move_to(angle)
    def left(self):
        angle = (self.hero.getH() + 90) % 360
        self.move_to(angle)
    def right(self):
        angle = (self.hero.getH() + 270) % 360
        self.move_to(angle)
    def up(self):
        pos = self.hero.getPos()
        self.hero.setPos(pos[0], pos[1], pos[2] + 1)
    def down(self):
        pos = self.hero.getPos()
        self.hero.setPos(pos[0], pos[1], pos[2] - 1)

    def turn_left(self):
        self.hero.setH((self.hero.getH() + 5) % 360)
    def turn_right(self):
        self.hero.setH((self.hero.getH() - 5) % 360)
    def turn_up(self):
        current_p = base.camera.getP()
        new_p = max(-90, min(90, current_p + 5))
        base.camera.setP(new_p)
    def turn_down(self):
        current_p = base.camera.getP()
        new_p = max(-90, min(90, current_p - 5))
        base.camera.setP(new_p)

    def build(self):
        angle = self.hero.getH() % 360
        pos = self.look_at(angle)
        if self.mode:
            self.land.addBlock(pos)
        else:
            self.land.buildBlock(pos)
        self.land.updateColumnTexture(pos)
    def destroy(self):
        angle = self.hero.getH() % 360
        pos = self.look_at(angle)
        if self.mode:
            self.land.delBlock(pos)
        else:
            self.land.delBlock(pos)
        self.land.updateColumnTexture(pos)

    def mouse_look_task(self, task):
        """Таск для обробки руху миші."""
        if not base.win:
            return task.cont
        p = base.win.getPointer(0)
        x = p.getX()
        y = p.getY()

        cx = getattr(self, '_center_x', base.win.getXSize() // 2)
        cy = getattr(self, '_center_y', base.win.getYSize() // 2)

        dx = x - cx
        dy = y - cy

        if dx != 0 or dy != 0:
            sens = 0.2  # Чутливість миші
            if self.cameraOn:  # Режим від третьої особи
                # Обертання героя і камери разом
                new_h = self.hero.getH() - dx * sens
                self.hero.setH(new_h)
                new_p = base.camera.getP() - dy * sens
                new_p = max(-45, min(45, new_p))  # Обмеження кута огляду
                base.camera.setP(new_p)
            else:  # Режим від першої особи
                # Обертання героя разом із камерою
                new_h = self.hero.getH() - dx * sens
                self.hero.setH(new_h)
                new_p = base.camera.getP() - dy * sens
                new_p = max(-90, min(90, new_p))  # Обмеження кута огляду
                base.camera.setP(new_p)
            base.win.movePointer(0, cx, cy)

        return task.cont

    def toggle_mouse_look(self):
        """Вмикає/вимикає поворот мишкою."""
        if getattr(self, '_mouse_look_active', False):
            self.stop_mouse_look()
        else:
            self.start_mouse_look()

    def start_mouse_look(self):
        """Запускає таск для обробки руху миші."""
        name = 'hero-mouse-look'
        try:
            taskMgr.remove(name)
        except Exception:
            pass

        # Зберегти поточний кут огляду камери та героя
        if not hasattr(self, 'saved_hpr') or self.saved_hpr is None:
            self.saved_hpr = base.camera.getHpr()
        if not hasattr(self, 'saved_hero_h') or self.saved_hero_h is None:
            self.saved_hero_h = self.hero.getH()

        props = WindowProperties()
        props.setCursorHidden(True)
        base.win.requestProperties(props)

        self._center_x = base.win.getXSize() // 2
        self._center_y = base.win.getYSize() // 2
        base.win.movePointer(0, self._center_x, self._center_y)

        taskMgr.add(self.mouse_look_task, name)
        self._mouse_task_name = name
        self._mouse_look_active = True

    def stop_mouse_look(self):
        """Зупиняє таск для обробки руху миші."""
        name = getattr(self, '_mouse_task_name', None)
        if name:
            try:
                taskMgr.remove(name)
            except Exception:
                pass
            self._mouse_task_name = None

        # Відновити збережений кут огляду камери та героя
        if hasattr(self, 'saved_hpr') and self.saved_hpr is not None:
            base.camera.setHpr(self.saved_hpr)
            self.saved_hpr = None
        if hasattr(self, 'saved_hero_h') and self.saved_hero_h is not None:
            self.hero.setH(self.saved_hero_h)
            self.saved_hero_h = None

        props = WindowProperties()
        props.setCursorHidden(False)
        base.win.requestProperties(props)
        self._mouse_look_active = False

    def accept_events(self):
        base.accept(key_forward, self.forward)
        base.accept(key_forward + '-repeat', self.forward)
        base.accept(key_back, self.back)
        base.accept(key_back + '-repeat', self.back)
        base.accept(key_left, self.left)
        base.accept(key_left + '-repeat', self.left)
        base.accept(key_right, self.right)
        base.accept(key_right + '-repeat', self.right)
        base.accept(key_up, self.up)
        base.accept(key_up + '-repeat', self.up)
        base.accept(key_down, self.down)
        base.accept(key_down + '-repeat', self.down)
        
        
        base.accept(key_turn_left, self.turn_left)
        base.accept(key_turn_left + '-repeat', self.turn_left)
        base.accept(key_turn_right, self.turn_right)
        base.accept(key_turn_right + '-repeat', self.turn_right)
        base.accept(key_turn_up, self.turn_up)
        base.accept(key_turn_up + '-repeat', self.turn_up)
        base.accept(key_turn_down, self.turn_down)
        base.accept(key_turn_down + '-repeat', self.turn_down)
        

        base.accept(key_switch_camera, self.changeView)
        base.accept(key_switch_mode, self.switch_mode)
        base.accept(key_toggle_mouse, self.toggle_mouse_look)

        
        base.accept(key_add_block, self.build)
        base.accept(key_add_block + '-repeat', self.build)
        base.accept(key_del_block, self.destroy)
        base.accept(key_del_block + '-repeat', self.destroy)
    
        base.accept(save_map, self.land.saveMap)
        base.accept(load_map, self.land.loadMap)
