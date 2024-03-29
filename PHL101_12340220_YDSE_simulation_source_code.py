import pygame, tkinter as tk , time
from sys import exit
from math import pi, sin, asin

def gradientRect(window, left_colour, right_colour, target_rect):
    colour_rect = pygame.Surface((2, 2))
    pygame.draw.line(colour_rect, left_colour, (0,0), (1,0))
    pygame.draw.line(colour_rect, right_colour, (0,1), (1,1))
    colour_rect = pygame.transform.smoothscale(colour_rect, (target_rect.width, target_rect.height))
    window.blit(colour_rect, target_rect)
    
def wavelength_to_rgb(wavelength):
    gamma = 0.8
    intensity_max = 255

    if 380 <= wavelength < 440:
        R = -(wavelength - 440) / (440 - 380)
        G = 0.0
        B = 1.0
    elif 440 <= wavelength < 490:
        R = 0.0
        G = (wavelength - 440) / (490 - 440)
        B = 1.0
    elif 490 <= wavelength < 510:
        R = 0.0
        G = 1.0
        B = -(wavelength - 510) / (510 - 490)
    elif 510 <= wavelength < 580:
        R = (wavelength - 510) / (580 - 510)
        G = 1.0
        B = 0.0
    elif 580 <= wavelength < 645:
        R = 1.0
        G = -(wavelength - 645) / (645 - 580)
        B = 0.0
    elif 645 <= wavelength <= 750:
        R = 1.0
        G = 0.0
        B = 0.0
    else:
        R = 255
        G = 255
        B = 255

    # Adjust intensity
    if 380 <= wavelength < 645:
        factor = 1.0
    else:
        factor = 0.3 + 0.7 * (750 - wavelength) / (750 - 645)
    if 380 <= wavelength <= 750:
        R = int(intensity_max * (R ** gamma) * factor)
        G = int(intensity_max * (G ** gamma) * factor)
        B = int(intensity_max * (B ** gamma) * factor)

    return (R, G, B)

class Wavefronts:
    def __init__(self, startx, starty):
        self.startx, self.starty = startx, starty
        self.boxes = [0]
        self.rect = pygame.Rect(startx, starty, 40, 40)
        self.prev_D = 800
        
        self.wavefront_seperation = 5
        self.wavefront_seperation_input = str(self.wavefront_seperation)
        
        self.propogate = True
    
    def production(self, color = 'white'):
        pygame.draw.arc(screen, color, self.rect, -1.5, 1.5, width = 1)
    
    def propogation(self, color = 'white'):
        self.wavefront_seperation_input = str(self.wavefront_seperation)
        for i in self.boxes[::-1]:
            self.rect = pygame.Rect(self.startx, self.starty-i, 2*i, 2*i)
            self.production(color)
            if self.boxes.index(i) <= 10:
                time.sleep(0.001)
        if self.propogate:
            self.boxes.insert(0,self.boxes[0] + self.wavefront_seperation)
    
    def animate(self, scr_pos):
        for i in range(self.startx + 2*self.boxes[-1], scr_pos ,self.wavefront_seperation):
            pass
        
        
class Main:
    def __init__(self):
        self.default()
        
    def draw(self):
        self.s.propogation(wavelength_to_rgb(self.L))
        
        pygame.draw.line(screen, 'white', (10,0), (10,800))
        pygame.draw.rect(screen ,'black', pygame.Rect(self.D,0,800,800))
        pygame.draw.line(screen, 'white', (self.D, 0), (self.D, 395 - self.d/2), width = 5)
        pygame.draw.line(screen, 'white', (self.D, 405 - self.d/2), (self.D, 395 + self.d/2), width = 5)
        pygame.draw.line(screen, 'white', (self.D, 405 + self.d/2), (self.D, 800), width = 5)
        
        if (self.D - self.s.startx)/2 <= self.s.boxes[0]:
            self.s1.propogation(wavelength_to_rgb(self.L))
            self.s2.propogation(wavelength_to_rgb(self.L))
            
        pygame.draw.rect(screen, 'white', pygame.Rect(800,0,200,800))
        pygame.draw.rect(screen, 'white', pygame.Rect(0, 770, 1000, 30))
        
        if self.s1.rect.midright[0] > 800:
            self.scr()

            
        self.text_surface = text_font.render('D = ' + str(self.actual_D) + ' cm', False, 'black')
        self.text_rect = self.text_surface.get_rect(center = (self.D + (800-self.D)/2, 780))
        
        
    def change_D(self):
        if self.s.prev_D != self.D:
            self.s.prev_D = self.D

            self.s1.startx = self.D
            self.s2.startx = self.D
            
            self.restart(1)
        self.actual_D = 2*(800 - self.D)/10
            
            
    def change_d(self):
        self.s1.starty = 400 - self.d/2
        self.s2.starty = 400 + self.d/2
        
    def change_L(self):
        self.s1.wavefront_seperation = self.L/115
        self.s2.wavefront_seperation = self.L/115
        self.s.wavefront_seperation = self.L/115
        self.restart(lm[1]%2)

    def restart(self, cond):
        if cond: 
            self.s1.boxes.clear()
            self.s2.boxes.clear()
            self.s.boxes.clear()
            
            self.s.boxes.append(0)
            self.s1.boxes.append(0)
            self.s2.boxes.append(0)
    
    def default(self):
        self.d = 50
        self.actual_d = self.d/10
        self.d_input_text = str(self.actual_d)
        
        self.D = 300
        self.actual_D = 2*(800 - self.D)/10
        
        self.source = (10,400)
        
        self.L = 600
        self.L_input_text = str(self.L)
        
        self.B = (self.L)*(self.actual_D/self.d)*(10**-4)
        self.actual_B = self.L * (self.D/100)/self.actual_d
        self.B_input_text = str(self.B)
        
        self.s = Wavefronts(*self.source)
        self.s.prev_D = self.D

        self.slit1 = (self.D, 400 - self.d/2)
        self.slit2 = (self.D, 400 + self.d/2)

        self.s1 = Wavefronts(*self.slit1)
        self.s2 = Wavefronts(*self.slit2)
        
    def update(self):
        self.change_D()
        self.change_d()
        self.change_L()
        self.draw()
        self.ui()
        
        self.actual_D = 800 - self.D
        self.actual_d = self.d/10
        self.actual_B = self.L * (self.actual_D/100)/self.actual_d
        
        self.B_input_text = str(self.B)
        screen.blit(self.text_surface, self.text_rect)
        
    def scr(self):
        if self.d and self.D > 4:
            self.B = ((800-self.D) * sin(asin(73/700)) * 50 * self.L / self.d)/600
        i = 0
        while (i*self.B < 500):
            gradientRect(screen, wavelength_to_rgb(self.L), (0,0,0), pygame.Rect(800, 400 - i*self.B, 200, self.B/2))
            gradientRect(screen, (0,0,0), wavelength_to_rgb(self.L), pygame.Rect(800, 400 - i*self.B - self.B/2, 200, self.B/2))
            gradientRect(screen, wavelength_to_rgb(self.L), (0,0,0), pygame.Rect(800, 400 + i*self.B, 200, self.B/2))
            gradientRect(screen, (0,0,0), wavelength_to_rgb(self.L), pygame.Rect(800, 400 + i*self.B + self.B/2, 200, self.B/2))
            i+=1
        
        
    def ui(self):
        pygame.draw.rect(screen, 'white', pygame.Rect(0, 800, 1000, 200))
        pygame.draw.rect(screen, 'white', pygame.Rect(800, 770, 200, 230))
        
        B_text = text_font.render(f"β = {(self.actual_B)/5} µm", False, 'black')
        B_text_rect = B_text.get_rect(topleft = (850, 800))
        screen.blit(B_text, B_text_rect)
        
        
        d_text = text_font.render(f"d = {self.actual_d} mm", False, 'black')
        d_text_rect = d_text.get_rect(topleft = (10, 800))
        screen.blit(d_text, d_text_rect)
        pygame.draw.rect(screen, 'black', pygame.Rect(10, 819, 80, 16), width = 1)
        d_input = text_font.render(self.d_input_text, False, 'black')
        d_input_rect = d_input.get_rect(center = (45, 828))
        screen.blit(d_input, d_input_rect)
        
        L_text = text_font.render(f"λ = {self.L} nm", False, 'black')
        L_text_rect = L_text.get_rect(topleft = (100, 800))
        screen.blit(L_text, L_text_rect)
        pygame.draw.rect(screen, 'black', pygame.Rect(100, 819, 80, 16), width = 1)
        L_input = text_font.render(self.L_input_text, False, 'black')
        L_input_rect = L_input.get_rect(center = (135, 828))
        screen.blit(L_input, L_input_rect)
        
        default_text = text_font.render('Back to Default', False, 'red')
        default_text_rect = default_text.get_rect(topleft = (300, 815))
        screen.blit(default_text, default_text_rect)
        pygame.draw.rect(screen, 'black', pygame.Rect(295, 810, 120, 20), width = 1)
        
        instructions_text = text_font.render('Read Instructions', False, 'red')
        instructions_text_rect = instructions_text.get_rect(topleft = (450, 815))
        screen.blit(instructions_text, instructions_text_rect)
        pygame.draw.rect(screen, 'black', pygame.Rect(445, 810, 150, 20), width = 1)
        

    def pop_up(self):
        greet = tk.Label(text = '''Welcome to the simulation for YDSE!!!
This simulation is made by AMAY DIXIT
Following is the basic guide on how to operate the program\n\n
1. Click on the text boxes below the variables (eg. d, λ) to change them
 2. Once you click on them, the option to enter values is active, press backspace to erase the current value completely and only then enter the new value 
3. Do not forget to click anywhere else on the screen after you're done entering the values, not doing so can cause bugs\n
4. Click on the black screen to change the values of D, you need not drag the slit surface, 
   just click on the black screen once and the slit surface will follow the cursor, click again to stop it, you can see the values of D changing
''')
        greet.pack()
        window.mainloop()
    
# pygame setup 
pygame.init()
screen = pygame.display.set_mode((1000,850))
pygame.display.set_caption("Amay's Double Slit Experiment")
SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)
clock = pygame.time.Clock()
text_font = pygame.font.Font(None, 22)
main = Main()


# tkinter setup
window = tk.Tk()
main.pop_up()

k = -1
lm = [0, 0, 0]
while 1:
    key = pygame.key.get_pressed()
    mouse = pygame.mouse.get_pos()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if mouse[0] < 750 and mouse[1] < 800:
            if event.type == pygame.MOUSEMOTION:
                if k%2 == 0:
                    main.D = mouse[0]
                
            elif event.type == pygame.MOUSEBUTTONDOWN:
                k += 1
                
        if event.type == pygame.MOUSEBUTTONDOWN:
            lm = [0 for x in lm]
            if mouse[0] in range(10,90) and mouse[1] in range(820,835):
                lm[0] += 1      
            if mouse[0] in range(100,180) and mouse[1] in range(820,835):
                lm[1] += 1
            if mouse[0] in range(295,295+120) and mouse[1] in range(810,830):
                main.default()
            if mouse[0] in range(445, 445+150) and mouse[1] in range(810, 830):
                main.pop_up()
                
                
                
        if lm[0]%2:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    main.d_input_text = main.d_input_text[:-1]
                else:
                    main.d_input_text += event.unicode
                    main.d = float(main.d_input_text)*10
        if lm[1]%2:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    main.L_input_text = main.L_input_text[:-1]
                else:
                    main.L_input_text += event.unicode
                    main.L = float(main.L_input_text)
        if lm[2]%2:
            pass
    
    screen.fill('#000000')
    main.update()
    pygame.display.update()
    clock.tick(90)