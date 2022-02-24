from curses import BUTTON1_RELEASED
import pygame as pg
import random 
pg.init()

FPS = 60


niveles = [
           [(0,0), (1,1), (2,2), (3, 3)],
           [(0, 0), (1, 0),(2, 0),(3, 0),(4, 0),(5, 0),(6, 0),(7, 0),(8, 0),(9, 0), 
            (0, 1), (9, 1),
            (0, 2), (9, 2),
            (0, 3), (1, 3),(2, 3),(3, 3),(4, 3),(5, 3),(6, 3),(7, 3),(8, 3),(9, 3)],
           ] 

class Vigneta:
    def __init__(self, padre, x, y, ancho, alto, color = (255, 255, 255)):
        self.padre = padre
        self.x = x
        self.y = y
        self.color = color
        self.ancho = ancho
        self.alto = alto
        self.vx = 0
        self.vy = 0

    @property
    def xcentro(self):
        return self.x + self.ancho // 2

    @property
    def ycentro(self):
        return self.y + self.alto // 2

    def intersecta(self, otro) -> bool:

        if self.ancho > otro.ancho:
            menor_ancho = otro
            mayor_ancho = self
        else:
            menor_ancho = self
            mayor_ancho = otro

        if self.alto > otro.alto:
            menor_alto = otro
            mayor_alto = self
        else:
            menor_alto = self
            mayor_alto = otro
        return (menor_ancho.x in range(mayor_ancho.x, mayor_ancho.x + mayor_ancho.ancho) or \
                menor_ancho.x + menor_ancho.ancho in range(mayor_ancho.x, mayor_ancho.x + mayor_ancho.ancho)) and \
               (menor_alto.y in range(mayor_alto.y, mayor_alto.y + mayor_alto.alto) or \
                menor_alto.y + menor_alto.alto in range(mayor_alto.y, mayor_alto.y + mayor_alto.alto))
        """
        return (self.x in range(otro.x, otro.x + otro.ancho) or \
                self.x + self.ancho in range(otro.x, otro.x + otro.ancho)) and \
               (self.y in range(otro.y, otro.y + otro.alto) or \
                self.y + self.alto in range(otro.y, otro.y + otro.alto))
        """                 


    def dibujar(self):
        pass

    def mover(self):
        pass

class Ladrillo(Vigneta):
    """
    def __init__(self, padre, x, y, ancho, alto, color = (255, 255, 255)):
        super().__init__(padre, x, y, ancho, alto, color)
        self.vivo = True
    """

    def dibujar(self):
        pg.draw.rect(self.padre, self.color, (self.x, self.y, self.ancho, self.alto))

    def comprobarToque(self, bola):
        if self.intersecta(bola):
            bola.vy *= -1
            return True

        return False

class Raqueta(Vigneta):
    def __init__(self, padre, x, y, ancho, alto, color = (255, 255, 0)):
        super().__init__(padre, x, y, ancho, alto, color)
        self.vx = 5

    def dibujar(self):
        pg.draw.rect(self.padre, self.color, (self.x, self.y, self.ancho, self.alto))

    def mover(self):
        teclas = pg.key.get_pressed()
        if teclas[pg.K_LEFT]:
            self.x -= self.vx
        if teclas[pg.K_RIGHT]:
            self.x += self.vx

        if self.x <= 0:
            self.x = 0
        if self.x + self.ancho >= self.padre.get_width():
            self.x = self.padre.get_width() - self.ancho

class Bola(Vigneta):
    def __init__(self, padre, x, y, color = (255, 255, 255), radio = 10):
        super().__init__(padre, x - radio, y - radio, 2 * radio, 2 * radio, color)
        self.radio = radio
        self.vx = 5
        self.vy = 5
        self.x_ini = x
        self.y_ini = y
        self.esta_viva = True

    def reset(self):
        self.x = self.x_ini
        self.y = self.y_ini
        self.vx = 5
        self.vy = 5
        self.esta_viva = True

    def mover(self):
        self.x += self.vx 
        self.y += self.vy

        if self.x <= 0 or self.x >= self.padre.get_width() - self.ancho:
            self.vx *= -1

        if self.y <= 0:
            self.vy *= -1

        if self.y >= self.padre.get_height() - self.alto:
            self.esta_viva = False

    def dibujar(self):
        pg.draw.circle(self.padre, self.color, (self.xcentro, self.ycentro), self.radio)

    def compruebaChoque(self, otro):
        if self.intersecta(otro):
           self.vy *= -1

class Game:
    def __init__(self, ancho=600, alto=800):
        self.pantalla = pg.display.set_mode((ancho, alto))
        self.bola = Bola(self.pantalla, ancho // 2, alto // 2)
        self.raqueta = Raqueta(self.pantalla, ancho//2, alto - 30, 100, 20)
        self.ladrillos = []
        self.contador_vidas = 3

        self.reloj = pg.time.Clock()
        """
        for i in range(random.randint(2, 10)):
            radio = random.randint(5, 50)
            self.bolas.append(Bola(random.randint(radio, ancho - radio),
                                   random.randint(radio, alto - radio),
                                   self.pantalla,
                                   (random.randint(0, 255),
                                    random.randint(0, 255),
                                    random.randint(0, 255)),
                                   radio))
            self.bolas[i].vx = random.randint(5,15) * random.choice[(-1, 1)]
            self.bolas[i].vy = random.randint(5,15) * random.choice[(-1, 1)]
        """

    def crea_ladrillos(self, nivel):
        for col, fil in niveles[nivel]:
            l = Ladrillo(self.pantalla, 5 + 60 * col, 25 + 30 * fil, 50, 20)
            self.ladrillos.append(l)

    def bucle_ppal(self):
        game_over = False
        nivel = 0

        while self.contador_vidas > 0 and nivel < len(niveles):
            self.crea_ladrillos(nivel)

            while self.contador_vidas > 0 and len(self.ladrillos) > 0: 
                # Este if equivale a
                # and  len(self.ladrillos) > 0
                # puesto en la línea del while
                
                self.reloj.tick(FPS)

                eventos = pg.event.get()
                for evento in eventos:
                    if evento.type == pg.QUIT:
                        self.contador_vidas = 0
                    """
                    if evento.type == pg.KEYDOWN:
                        if evento.key == pg.K_LEFT:
                            self.raqueta.vx = -5
                        if evento.key == pg.K_RIGHT:
                            self.raqueta.vx = 5
                    if evento.type == pg.KEYUP:
                        if evento.key in (pg.K_LEFT, pg.K_RIGHT):
                            self.raqueta.vx = 0
                    """
                

                self.pantalla.fill((255, 0, 0))    

                self.bola.mover()
                self.raqueta.mover()
                self.bola.compruebaChoque(self.raqueta)

                if not self.bola.esta_viva:
                    self.contador_vidas -= 1
                    self.bola.reset()
        
                self.bola.dibujar()
                self.raqueta.dibujar()
                """
                for ladrillo in self.ladrillos:
                    if ladrillo.vivo:
                        ladrillo.comprobarToque(self.bola)
                        ladrillo.dibujar()
                for indice, ladrillo in enumerate(self.ladrillos):
                    ha_chocado = ladrillo.comprobarToque(self.bola)
                    if ha_chocado:
                        self.ladrillos.pop(indice)
                """
                for ladrillo in self.ladrillos:
                    if ladrillo.comprobarToque(self.bola):
                        self.ladrillos.remove(ladrillo)
                    ladrillo.dibujar()

                print(len(self.ladrillos))
                pg.display.flip()

            nivel += 1
    
if __name__ == '__main__':
    pg.init()

    game = Game()
    game.bucle_ppal()

    pg.quit()
    