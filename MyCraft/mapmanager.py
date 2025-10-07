from panda3d.core import SamplerState
import pickle

class Mapmanager():
    
    def __init__(self):
        self.model = 'Models/block'
        self.texture = 'Textures/stone1.png'
        self.top_texture = 'Textures/diamond_ore.png'
        self.bedrock_texture = 'Textures/bedrock.png'
        self.colors = [
            (0.7, 0.2, 0.2, 1),   # темно-червоний
            (0.75, 0.35, 0.2, 1), # червоно-оранжевий
            (0.8, 0.5, 0.2, 1),   # оранжевий
            (0.85, 0.65, 0.25, 1),# золотисто-жовтий
            (0.85, 0.75, 0.3, 1), # жовтий
            (0.75, 0.8, 0.3, 1),  # жовто-зелений
            (0.6, 0.8, 0.35, 1),  # світло-зелений
            (0.4, 0.75, 0.4, 1),  # зелений
            (0.3, 0.7, 0.5, 1),   # зелено-бірюзовий
            (0.25, 0.65, 0.65, 1),# бірюзовий
            (0.25, 0.55, 0.75, 1),# блакитний
            (0.3, 0.45, 0.75, 1), # синій
            (0.4, 0.35, 0.75, 1), # синьо-фіолетовий
            (0.5, 0.3, 0.75, 1),  # фіолетовий
            (0.6, 0.25, 0.7, 1),  # пурпурний
            (0.65, 0.25, 0.6, 1), # темно-пурпурний
            (0.65, 0.25, 0.5, 1), # рожево-фіолетовий
            (0.65, 0.3, 0.4, 1),  # винний
            (0.6, 0.3, 0.3, 1),   # червоно-коричневий
            (0.55, 0.25, 0.25, 1) # темний бордо
        ]
        self.startNew()

    def addBlock(self, pos, is_top=False):
        existing_blocks = self.findBlocks(pos)
        if not existing_blocks.isEmpty():
            return None
        self.block = loader.loadModel(self.model)
        x, y, z = pos
        if z == 0:
            self.block.setTexture(loader.loadTexture(self.bedrock_texture))
        elif is_top:
            self.block.setTexture(loader.loadTexture(self.top_texture))
        else:
            self.block.setTexture(loader.loadTexture(self.texture))
        self.block.setPos(pos)
        self.color = self.getColor(int(pos[2]))
        self.block.setColor(self.color)
        self.block.reparentTo(self.land)
        self.block.setTag('at', str(pos))
        self.block.setTag('is_top', '1' if is_top else '0')
    def getColor(self, z):
        if z < len(self.colors):
            return self.colors[z]
        else:
            return self.colors[len(self.colors) - 1]

    def startNew(self):
        self.land = render.attachNewNode("Land") # узел, к которому привязаны все блоки карты
    def check_block(self, pos):
        block = self.find_block(pos)
        if block is not None:
            return False
        else:
            return True
    def clear(self):
        self.land.removeNode()
        self.startNew()
    def isEmpty(self, pos):
        block = self.findBlocks(pos)
        if block.isEmpty():
            return True
        else:
            return False
    def findBlocks(self, pos):
        return self.land.findAllMatches('=at=' + str(pos))
    def findHighestEmpty(self, pos):
        x, y, z = pos
        z = 1
        while not self.isEmpty((x, y, z)):
            z += 1
        return (x, y, z)

    def buildBlock(self, pos):
        x, y, z = pos
        new = self.findHighestEmpty(pos)
        if new[2] <= z + 1:
            self.addBlock(new)
    def delBlock(self, pos):
        block = self.findBlocks(pos)
        for b in block:
            b.removeNode()
    def delBlockFrom(self, tag):
        x, y, z = tag
        pos = x, y, z -1
        blocks = self.findBlocks(pos)
        for b in blocks:
            b.removeNode()

    def saveMap(self):
        blocks = self.land.getChildren()
        with open('my_map.dat', 'wb') as fout:
            pickle.dump(len(blocks), fout)
            for block in blocks:
                x, y, z = block.getPos()
                pos = (int(x), int(y), int(z))
                is_top = block.getTag('is_top') == '1'
                pickle.dump((pos, is_top), fout)
    def loadMap(self):
        self.clear()
        with open('my_map.dat', 'rb') as fin:
            length = pickle.load(fin)
            for i in range(length):
                pos, is_top = pickle.load(fin)
                self.addBlock(pos, is_top=is_top)

    def updateBlockTexture(self, pos):
        x, y, z = pos
        for dz in (-1, 0, 1):
            current_pos = (x, y, z + dz)
            block = self.find_block(current_pos)
            if block:
                if dz == 1:  # Верхній блок
                    block.setTexture(loader.loadTexture(self.top_texture))
                elif dz == -1 and z + dz == 0:  # Найнижчий блок
                    block.setTexture(loader.loadTexture(self.bedrock_texture))
                else:  # Звичайний блок
                    block.setTexture(loader.loadTexture(self.texture))
    def updateColumnTexture(self, pos):
        x, y, _ = pos

        # Знайти всі блоки в колонці (x, y)
        blocks = []
        for z in range(0, 256):  # Припустимо, що висота світу — 256 блоків
            block_collection = self.findBlocks((x, y, z))
            for block in block_collection:  # Обробляємо кожен блок у колекції
                blocks.append((block, z))

        # Оновити текстури
        for i, (block, z) in enumerate(blocks):
            if i == len(blocks) - 1:  # Найвищий блок
                block.setTexture(loader.loadTexture(self.top_texture))
                block.setTag('is_top', '1')
            elif z == 0:  # Найнижчий блок
                block.setTexture(loader.loadTexture(self.bedrock_texture))
                block.setTag('is_top', '0')
            else:  # Звичайний блок
                block.setTexture(loader.loadTexture(self.texture))
                block.setTag('is_top', '0')
    def findBlocksInColumn(self, pos):
        x, y = pos
        blocks = []
        
        for z in range(0, 256):
            block = self.findBlocks((x,y,z))
            if not block.isEmpty():
                blocks.append(block)

        return blocks

    def loadLand(self, filename):
        self.clear()
        with open(filename) as file:
            y = 0
            for line in file:
                x = 0
                line = line.split(' ')
                for z in line:
                    height = int(z)
                    for z0 in range(height+1):
                        is_top = (z0 == height)
                        block = self.addBlock((x, y, z0), is_top=is_top)
                    x += 1
                y += 1
        return x,y
