from arkanoid.escenas import Partida, GameOver
from pygame import init, display

init()

class Game:
    def __init__(self, ancho=600, alto=800):
        pantalla = display.set_mode((ancho, alto))
        partida = Partida(pantalla)
        game_over = GameOver(pantalla)

        self.escenas = [partida, game_over]

    def lanzar(self):
        escena_activa = 0
        game_active = True
        while game_active:
            game_active = self.escenas[escena_activa].bucle_ppal()
            escena_activa += 1
            if escena_activa == len(self.escenas):
                escena_activa = 0
                