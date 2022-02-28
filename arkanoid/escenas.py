import pygame as pg

from arkanoid.entities import Bola, Raqueta, Ladrillo
from arkanoid import niveles, FPS

class Escena:
    def __init__(self, pantalla):
        self.pantalla = pantalla
        self.reloj = pg.time.Clock()

    def bucle_ppal(self) -> bool:
        pass


class Partida(Escena):
    def __init__(self, pantalla):
        super().__init__(pantalla)
        self.bola = Bola(self.pantalla, self.pantalla.get_width() // 2, 
                         self.pantalla.get_height() // 2)
        self.raqueta = Raqueta(self.pantalla, self.pantalla.get_width()//2, 
                         self.pantalla.get_height() - 30)

        self.fondo = pg.image.load("./resources/images/background.jpg")
        self.ladrillos = []
        self.todos = []
        self.reset()

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

    def reset(self):
        self.ladrillos = []
        self.todos = []
        self.todos.append(self.bola)
        self.todos.append(self.raqueta)
        self.contador_vidas = 3


    def crea_ladrillos(self, nivel):
        for col, fil in niveles[nivel]:
            l = Ladrillo(self.pantalla, 5 + 60 * col, 25 + 30 * fil, 50, 20)
            self.ladrillos.append(l)
        
        self.todos = self.todos + self.ladrillos

    def bucle_ppal(self) -> bool:
        nivel = 0
        self.reset()
        # Inicializaciones 

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
                        return False
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
                

                self.pantalla.blit(self.fondo, (0, 0))

                for objeto in self.todos:
                    objeto.mover()

                self.bola.compruebaChoque(self.raqueta)

                if not self.bola.esta_viva:
                    self.contador_vidas -= 1
                    self.bola.reset()
        
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
                        self.todos.remove(ladrillo)


                for objeto in self.todos:
                    objeto.dibujar()

                pg.display.flip()

            nivel += 1
            self.bola.reset()

        return True

class GameOver(Escena):
    def __init__(self, pantalla):
        pg.Rect
        super().__init__(pantalla)
        self.fuente = pg.font.Font("resources/fonts/FredokaOne-Regular.ttf", 25)

    def bucle_ppal(self):
        while True:
            for evento in pg.event.get():
                if evento.type == pg.QUIT:
                    return False
                
                if evento.type == pg.KEYDOWN:
                    if evento.key == pg.K_SPACE:
                        return True

            self.pantalla.fill((30, 30, 255))
            texto = self.fuente.render("GAME OVER", True, (255, 255, 0))
            rectexto = texto.get_rect() 

            rectpantalla = self.pantalla.get_rect()

            self.pantalla.blit(texto, (rectpantalla.centerx - rectexto.centerx, 
                                       rectpantalla.centery - rectexto.centery))

            self.pantalla.blit(texto, ((self.pantalla.get_width() - rectexto.w) // 2,
                                      (self.pantalla.get_height() - rectexto.h) // 2))

            pg.display.flip()
            