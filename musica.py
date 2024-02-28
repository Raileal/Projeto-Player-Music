from pygame import mixer
import pygame
import os
from tkinter.filedialog import askdirectory

class Player():
    def __init__(self):
        mixer.init()
        self.pasta_origem = None
        self.lista_arquivos = []
        self.indice = 0
        self.parou = True
        self.musica_atual = None
        self.pausado = False  # Novo atributo para controlar a pausa
        
    def selecionar_pasta(self):
        self.pasta_origem = askdirectory(title="Selecione a Pasta Origem")
        if self.pasta_origem:
            self.lista_arquivos = [os.path.join(self.pasta_origem, arquivo) for arquivo in os.listdir(self.pasta_origem) if arquivo.endswith(('.mp3', '.wav'))]
            self.iniciar_musica()
        else:
            print("Nenhuma pasta selecionada.")
            
        return self.lista_arquivos
            

    def iniciar_musica(self):
        if len(self.lista_arquivos) > 0:
            mixer.music.load(self.lista_arquivos[self.indice])
            mixer.music.play()
            
            self.musica_atual = os.path.basename(self.lista_arquivos[self.indice])
            # self.get_indice_musica_atual()
            self.parou = False

            
    def toggle_reproducao(self):
        if mixer.music.get_busy():  
            print('parou')
            self.pausar_musica() 
        else:
            print('retomou')
            self.retomar_reproducao()
            if self.parou == True:
                self.iniciar_musica()

    def proxima_musica(self):
        if self.indice < len(self.lista_arquivos) - 1:
            self.indice += 1
            self.iniciar_musica()
        else:
            print('Não há próxima música.')
            self.indice = 0  # Volta para a primeira música
            self.iniciar_musica()
            

    def musica_anterior(self):
        if self.indice > 0:
            self.indice -= 1
            self.iniciar_musica()
        else:
            print('Não há música anterior.')
            self.indice = len(self.lista_arquivos) - 1  # Vai para a última música
            self.iniciar_musica()
            
    def pausar_musica(self):  # Verifica se a música está em reprodução
        mixer.music.pause()
        self.pausado = True 


    def retomar_reproducao(self):
        if not mixer.music.get_busy():
            mixer.music.unpause()
            self.pausado = False
        else:
            print("Nao ha musica em pause")
            
    def parar_musica(self):
        mixer.music.stop()
        self.parou = True
        
    
    def tocar_musica(self, musica):
        if self.pasta_origem and os.path.exists(self.pasta_origem):
            self.lista_arquivos = [os.path.join(self.pasta_origem, arquivo) for arquivo in os.listdir(self.pasta_origem) if arquivo.endswith(('.mp3', '.wav'))]
            print("Música clicada:", musica)
            for index, arquivo in enumerate(self.lista_arquivos):
                if musica in arquivo:
                    print(f"Música {musica} está na lista de reprodução.")
                    
                    if self.musica_atual == musica:
                        if mixer.music.get_busy():
                            print('Música em reprodução, pausando...')
                            self.pausar_musica()
                        else:
                            print('Música pausada, retomando...')
                            self.retomar_reproducao()
                    else:
                        print('Nova música selecionada, iniciando...')
                        mixer.music.load(self.lista_arquivos[index])
                        mixer.music.play()
                        self.parou = False
                        self.musica_atual = musica
                    break
            else:
                print(f"Música {musica} não está na lista de reprodução.")
        else:
            print("Nenhuma pasta de origem selecionada ou pasta não existe.")
            
        return index

    def get_indice_musica_atual(self):
        print('id atual ->',self.indice)
        return self.indice

    # def check_music_end(self):
    #     for event in pygame.event.get():
    #         if event.type == pygame.USEREVENT + 1:
    #             self.proxima_musica()

            

# # Criar uma instância da classe Player
# player = Player()
# player.selecionar_pasta()

# while True:
#     op = int(input('Digite'))
#     if op == 0:
#         player.parar_musica()
#     if op == 1:
#         player.proxima_musica()
#     if op == 2:
#         player.musica_anterior()
#     if op == 3:
#         player.pausar_musica()
#     if op == 4:
#         player.retomar_reproducao()
#     if op == 5:
#         player.iniciar_musica()
#     if op == 6:
#         break