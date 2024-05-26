import pygame
import math
import asyncio
pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (100, 149, 237)
RED = (188, 39, 50)
DARK_GREY = (80, 78, 81)

FONT_planet = pygame.font.SysFont("comicsans", 16)
FONT_menu = pygame.font.SysFont("arial", 48)

class Button:
    def __init__(self, text, position):
        self.text = text
        self.font = pygame.font.SysFont("arial", 36)
        self.text_surface = self.font.render(self.text, True, DARK_GREY)
        self.rect = self.text_surface.get_rect()
        self.rect.topleft = position
        self.state = False

    #draw button on the screen
    def draw_btn(self, screen):
        screen.blit(self.text_surface, self.rect) #(背景變數, 繪製位置)

class Planet:
    AU = 149.6e6 * 1000
    G = 6.67428e-11
    SCALE = 250 / AU # 1AU = 100 pixels
    TIMESTEP = 3600 * 24 # 1 day

    def __init__(self, name, x, y, radius, image, mass, scale):
        self.width = image.get_width()
        self.height = image.get_height()
        self.name = name
        self.x = x 
        self.y = y 
        self.radius = radius
        self.image = pygame.transform.scale(image, (int(self.width * scale), int(self.height * scale)))
        self.mass = mass
        self.scale = scale
        self.rect = self.image.get_rect()

        self.orbit = []
        self.sun = False
        self.distance_to_sun = 0

        self.x_vel = 0
        self.y_vel = 0

    def draw(self):
        x = self.x * self.SCALE + WIDTH / 2
        y = self.y * self.SCALE + HEIGHT / 2
        
        if len(self.orbit) >= 2:
            updated_points = []
            for point in self.orbit:
                x, y = point
                x = x * self.SCALE + WIDTH / 2 - int(self.width * self.scale)/2
                y = y * self.SCALE + HEIGHT / 2 - int(self.height * self.scale)/2
                updated_points.append((x, y))

            planet_name = FONT_planet.render(f"{self.name}", 3, WHITE)
            if self.name == "Sun":
                screen.blit(planet_name, (x, y))
            else:
                screen.blit(planet_name, (x+50, y))
        
        #pygame.draw.circle(screen, self.color, (x, y), self.radius)
        screen.blit(self.image, (x, y))
    
    def attraction(self, other):
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)
        if other.sun:
            self.distance_to_sun = distance
        force = self.G * self.mass * other.mass / distance**2
        theta = math.atan2(distance_y, distance_x)
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force
        return force_x, force_y
    
    def update_position(self, planets):
        total_fx = total_fy = 0
        for planet in planets:
            if self == planet:
                continue
            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy

        self.x_vel += total_fx / self.mass * self.TIMESTEP
        self.y_vel += total_fy / self.mass * self.TIMESTEP

        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP
        self.orbit.append((self.x, self.y))

async def main():
    run = True
    clock = pygame.time.Clock()
    planets = []

    sun_img = pygame.image.load(r"C:\myProject\Web\app\static\game_image\sun.png")
    sun_img = pygame.transform.scale(sun_img, (100, 100))
    #sun = Planet("Sun", 0, 0, 30, YELLOW, 1.98892 * 10**30)
    sun = Planet("Sun", 0, 0, 30, sun_img, 1.98892 * 10**30, 1) #(self, name, x, y, radius, image, mass, scale)
    sun.sun = True
    planets.append(sun)

    mercury_img = pygame.image.load(r"C:\myProject\Web\app\static\game_image\mercury.png")
    mercury_img = pygame.transform.scale(mercury_img, (100, 100))
    #mercury = Planet("Mercury", 0.3878*Planet.AU, 0, 8, DARK_GREY, 3.30 * 10**24)
    mercury = Planet("Mercury", 0.3878*Planet.AU, 0, 8, mercury_img, 3.30 * 10**24, 8/30)
    planets.append(mercury)
    mercury.y_vel = -47.4 * 1000

    venus_img = pygame.image.load(r"C:\myProject\Web\app\static\game_image\venus.png")
    venus_img = pygame.transform.scale(venus_img, (100, 100))
    #venus = Planet("Venus", 0.723*Planet.AU, 0, 14, WHITE, 4.8685 * 10**24)
    venus = Planet("Venus", 0.723*Planet.AU, 0, 14, venus_img, 4.8685 * 10**24, 14/30)
    planets.append(venus)
    venus.y_vel = -35.02 * 1000

    earth_img = pygame.image.load(r"C:\myProject\Web\app\static\game_image\earth.png")
    earth_img = pygame.transform.scale(earth_img, (100, 100))
    #earth = Planet("Earth", -1*Planet.AU, 0, 16, BLUE, 5.9742 * 10**24)
    earth = Planet("Earth", -1*Planet.AU, 0, 16, earth_img, 5.9742 * 10**24, 16/30)
    planets.append(earth)
    earth.y_vel = 29.783 * 1000

    mars_img = pygame.image.load(r"C:\myProject\Web\app\static\game_image\mars.png")
    mars_img = pygame.transform.scale(mars_img, (100, 100))
    #mars = Planet("Mars", -1.524*Planet.AU, 0, 12, RED, 6.39 * 10**23)
    mars = Planet("Mars", -1.524*Planet.AU, 0, 12, mars_img, 6.39 * 10**23, 12/30)
    planets.append(mars)
    mars.y_vel = 24.077 * 1000

    #jupiter_img = pygame.image.load(r"C:\Users\shuo\Desktop\game_image\jupiter.png")
    #jupiter_img = pygame.transform.scale(jupiter_img, (100, 100))
    #jupiter = Planet("Jupiter", 5.20*Planet.AU, 0, 24, jupiter_img, 1.898 * 10**27, 24/30)
    #planets.append(jupiter)
    #jupiter.y_vel = 37.26 * 1000

    menu_btn = []
    pause_start_btn = Button("PAUSE/START", (5, 50))
    restart_btn = Button("RESTART", (5, 85))
    introduction_btn = Button("INTRODUCTION", (5, 120))
    menu_btn.append(pause_start_btn)
    menu_btn.append(restart_btn)
    menu_btn.append(introduction_btn)

    while run:
        clock.tick(60)
        screen.fill(BLACK)

        #Menu
        pygame.draw.rect(screen, WHITE, [0, 0, 280, 170], 3)
        menu_text = FONT_menu.render("MENU", 3, WHITE)
        screen.blit(menu_text, (5, 0))

        pause_start_btn.draw_btn(screen)
        restart_btn.draw_btn(screen)
        introduction_btn.draw_btn(screen)

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if(pause_start_btn.rect.collidepoint(event.pos)):
                    if(pause_start_btn.state == False):
                        pause_start_btn.state = True
                    else:
                        pause_start_btn.state = False
                
                if(restart_btn.rect.collidepoint(event.pos)):
                    await main()
                

            for btn in menu_btn:
                if event.type == pygame.MOUSEMOTION:
                    if(btn.rect.collidepoint(event.pos)):
                        btn.text_surface = btn.font.render(btn.text, True, WHITE)
                    else:
                        btn.text_surface = btn.font.render(btn.text, True, DARK_GREY)
            if event.type == pygame.QUIT:
                run = False

        
        for planet in planets:
            planet.draw()
            if(pause_start_btn.state == False):
                planet.update_position(planets)
        
        pygame.display.update()
    pygame.quit()


WIDTH, HEIGHT = 1000, 1000
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Planet Simulation")
asyncio.run( main() )