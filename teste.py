from tkinter import Tk, Button, Listbox, PhotoImage, Frame
from musica import *
import pygame

musica = Player()
player = Tk()
player.title("Music Player")
player.geometry("400x300")

playlist = []
# Variável global para controlar se a próxima música deve ser iniciada
proxima_musica_automatica = True

def select_dir():
    rai = musica.selecionar_pasta()
    for files in rai:
        print(files)
        nomes_musicas = os.path.basename(files)
        playlist.append(nomes_musicas)
        
    for t in playlist:
        listbox.insert("end", t)
        
    update_playlist_highlight()
        
def click_listbox(index):
    # Obtém o índice do item clicado
    index = listbox.curselection()
    
    if index:
        # Obtém o índice como um número inteiro
        index = int(index[0])
        # Obtém o nome do arquivo de música correspondente ao índice
        nome_musica = playlist[index]
        # Inicia a reprodução da música selecionada
        
        index = musica.tocar_musica(nome_musica)
        print('indice clique ->',index)

        
def play_stop_music():
    global proxima_musica_automatica
    proxima_musica_automatica = True
    musica.toggle_reproducao()

def stop_music():
    musica.parar_musica()
    # Define a variável global como False para não iniciar a próxima música automaticamente
    global proxima_musica_automatica
    proxima_musica_automatica = False

def pause_music():
    pausou = musica.pausar_musica()
    print(pausou)

def proxima():
    musica.proxima_musica()
    update_playlist_highlight()
    
def anterior():
    musica.musica_anterior()
    update_playlist_highlight()

def update_playlist_highlight():
    index = musica.get_indice_musica_atual()
    # Limpa qualquer destaque existente
    listbox.selection_clear(0, "end")
    # Marca o item atualmente em reprodução
    listbox.selection_set(index)
    listbox.activate(index)
    
def check_music_end():
    for event in pygame.event.get():
        if event.type == pygame.USEREVENT + 1 and proxima_musica_automatica:
            print('Música chegou ao fim, iniciando próxima...')
            proxima()

    player.after(100, check_music_end)  # Verifica a cada 100 milissegundos se a música terminou

# Inicialização do mixer do pygame
pygame.init()
mixer.init()

# Define um novo tipo de evento para sinalizar o fim da música
MUSIC_END_EVENT = pygame.USEREVENT + 1
# Registra o evento com o Pygame
pygame.mixer.music.set_endevent(MUSIC_END_EVENT)

# Verifica se a música terminou
player.after(100, check_music_end)

listbox = Listbox(player, relief='sunken', width=70, height=13)
listbox.pack(pady=10)

playImage = PhotoImage(file="./icons/play.png").subsample(2, 2)
stop_image = PhotoImage(file="./icons/stop.png").subsample(2,2)
seleciona_dir = PhotoImage(file="./icons/list.png").subsample(2, 2)
nextImage = PhotoImage(file="./icons/next.png").subsample(2, 2)
prevImage = PhotoImage(file="./icons/priv.png").subsample(2, 2)

button_frame = Frame(player)
button_frame.pack(pady=10)

bt3 = Button(button_frame, text="prev", image=prevImage, command=anterior)
bt3.config(height=40, width=40)
bt3.pack(side="left", padx=5)

bt1 = Button(button_frame, text="play", command=play_stop_music, image=playImage)
bt1.config(height=40, width=40)
bt1.pack(side="left", padx=5)

bt5 = Button(button_frame, text="stop", command=stop_music, image=stop_image)
bt5.config(height=40, width=40)
bt5.pack(side="left", padx=5)

bt4 = Button(button_frame, text="next", image=nextImage, command=proxima)
bt4.config(height=40, width=40)
bt4.pack(side="left", padx=5)

bt5 = Button(button_frame, text="list", image=seleciona_dir, command=select_dir)
bt5.config(height=40, width=40)
bt5.pack(side="left", padx=5)

listbox.bind("<Double-Button-1>", click_listbox)

player.mainloop()
