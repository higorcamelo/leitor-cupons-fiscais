import PySimpleGUI as sg
import os 

working_directory = os.getcwd()

class Janela():
    def __init__(self):
        #sg.Theme('Reddit')
        layout = [
            [sg.Text('Selecione uma imagem:')],
            [sg.InputText(key='-FILE_PATH-'),
            sg.FileBrowse(initial_folder = working_directory, file_types =[('Arquivos de imagem', '.png .jpeg')]),
            sg.Button('Importar'), sg.Exit()]
        ]
        criarJanela = sg.Window('Leitor de Notas Fiscais').layout(layout)
        self.buttons = criarJanela.Read()

    def Iniciar(self):
        print(self.values)

tela = Janela()
tela.Iniciar()
