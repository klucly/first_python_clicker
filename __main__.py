import os
from libs import *

reset_word_list = True

if reset_word_list:
    import word_list_getter
    word_list = word_list_getter.WORDS
else:
    try:
        with open("resources/word_list.json", "r") as file:
            word_list = eval(file.read())
    except:
        import word_list_getter
        word_list = word_list_getter.WORDS

class Main:
    def __init__(self, reset = False) -> None:
        self.window = engine.Window(win_size, win_caption, 60)
        self.objlist = []
        self.dirt_block_list = []
        self.event_list = []
        self.money = 0.
        self.tick = 0
        self.money_per_click = .1
        self.money_multiplier = 1.
        self.upgrades = []
        self.money_to_next_upgrade = 1
        self.upgrade_count = 0
        self.previous_money_multiplier = 0.
        self.loaded = False
        self.money_to_next_reset = 1000000
        self.reset_afford = False

        self.stats = Stats(self.window, [0, 500], [1280, 220], "(stats)")
        self.objlist.append(self.stats)
        self.money_counter = Text(self.window, 1., [1070, 10])
        self.objlist.append(self.money_counter)
        self.upgrade_list = Upgrade_list(self, [0, 0], [400, 720])
        self.objlist.append(self.upgrade_list)
        self.reset_button = Reset_button(self, [1020, 470], [260, 30], self.reset)

        if not reset:
            self.load()

            while 1: self.mainloop()

    def reset(self):
        old_money_multiplier = self.money_multiplier
        old_money_to_next_reset = self.money_to_next_reset
        self.__init__(True)
        self.loaded = True
        self.money_to_next_reset = old_money_to_next_reset*1000000
        self.money_multiplier = old_money_multiplier + 1.

    def dirt_block_init(self, dirt_block_count = 1):
        for dirt_block in self.dirt_block_list:
            self.objlist.remove(dirt_block)
        self.dirt_block_list = []

        dirt_block_size = [int(numpy.sqrt(dirt_block_count))+1]*2

        dirt_block_i = 0

        for i in range(dirt_block_size[0], 0, -1):
            for j in range(dirt_block_size[1], 0, -1):
                if dirt_block_i < dirt_block_count:
                    block = DirtBlock(self, [100-i*100+(j*100), -50-j*25-i*50])
                    self.objlist.append(block)
                    self.dirt_block_list.append(block)
                dirt_block_i += 1

    def mainloop(self) -> None:
        self.tick += 1

        if self.tick % 1000 == 0:
            self.save()

        if self.money_multiplier != self.previous_money_multiplier:
            self.dirt_block_init(self.money_multiplier)
            self.previous_money_multiplier = self.money_multiplier

        self.window.camera.position.x = numpy.sin(self.tick/40)*10
        self.window.camera.position.y = numpy.cos(self.tick/40)*10
        if self.money < 1000:
            self.money = float(float_to_string_short(self.money))
        else: self.money = round(self.money)

        self.money_counter.text = str(self.money)+"$"
        money_per_click = float(float_to_string_short(self.money_per_click))
        money_multiplier = float(float_to_string_short(self.money_multiplier))
        self.stats.text = f"Money per click: {money_per_click}, money multiplier: {money_multiplier}, tick: {self.tick}"
        self.dirt_block_list[0].calculate_press()

        if self.loaded:
            if self.money >= self.money_to_next_upgrade:
                self.upgrade_count += 1
                upgrade = Upgrade_list.Upgrade(random.choice(word_list), float(self.money_to_next_upgrade), upgrade_buy, self.money_to_next_upgrade/100)
                upgrade.init(self.upgrade_list)
                self.money_to_next_upgrade *= 10

        self.window.display.fill([40, 40, 50])

        if self.money_to_next_reset <= self.money and not self.reset_afford and self.reset_button not in self.objlist:
            self.objlist.append(self.reset_button)

        for obj in self.objlist:
            obj.draw()
        self.window.update()


    def save(self):
        base = {
            "money": self.money,
            "money_per_click": self.money_per_click,
            "money_mul": self.money_multiplier,
            "tick": self.tick,
            "upgrades": [],
            "money_to_next_upgrade": self.money_to_next_upgrade
        }

        for upgrade in self.upgrade_list.upgrades:
            base["upgrades"].append({"name": upgrade.title, "cost": upgrade.cost, "money_per_upgrade": upgrade.money})
        
        with open("save.save", "w") as file:
            file.write(str(base))

    def load(self):
        if "save.save" in os.listdir("."):
            self.upgrade_list.upgrades = []
            self.upgrades = []
            with open("save.save", "r") as file:
                save = eval(file.read())
            self.money = save["money"]
            self.money_per_click = save["money_per_click"]
            self.money_multiplier = save["money_mul"]
            self.tick = save["tick"]
            for upgrade in save["upgrades"]:
                upgrade_ = Upgrade_list.Upgrade(upgrade["name"], upgrade["cost"], upgrade_buy, upgrade["money_per_upgrade"])
                upgrade_.init(self.upgrade_list)
            self.money_to_next_upgrade = save["money_to_next_upgrade"]
        else:
            print("Can't find save file. Loading from the start")
        self.loaded = True


def upgrade_buy(self, main, add_money):
    main.money_per_click += add_money
    self.cost *= 1.2

if __name__ == "__main__":
    Main()
