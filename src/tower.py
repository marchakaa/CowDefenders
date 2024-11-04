from pygame import sprite, image, transform, draw

class Tower(sprite.Sprite):
    def __init__(self, name, dmg, image_url):
        super().__init__()
        self.name = name
        self.dmg = dmg
        self.size = 32
        self.center_pos = [0,0]
        
        if image_url:
            self.image = image.load(image_url)
            self.image = transform.scale(self.image, (self.size, self.size))
        else:
            self.image = None

    def update(self):
        pass
    def render(self, screen):
        if self.image:
            rect = self.image.get_rect(center=self.center_pos)
            screen.blit(self.image, rect)
        else:
            draw.rect(screen, (0,255,0), (self.center_pos[0] - self.size / 2, self.center_pos[1] - self.size / 2, self.size, self.size))
        
    def __str__(self):
        return super().__str__()
    def __repr__(self):
        return super().__repr__()
