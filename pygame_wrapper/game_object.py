class GameObject:
    def __init__(self, game):
        self.children = []
        self.game = game

    def add_child(self, child):
        self.children.append(child)

    def on_init(self):
        for child in self.children:
            child.on_init()

    def on_event(self, event):
        for child in self.children:
            child.on_event(event)

    def on_update(self, dt):
        for child in self.children:
            child.on_update(dt)

    def on_render(self, screen):
        for child in self.children:
            child.on_render(screen)

    def on_cleanup(self):
        for child in self.children:
            child.on_cleanup()
