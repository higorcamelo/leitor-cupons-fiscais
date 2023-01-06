from pytesseract import pytesseract
import cv2
import xml
import PySimpleGUI as sg
import os 

diretorio = os.getcwd()

class Janela():
    def __init__(self):
        #sg.Theme('Reddit')
        layout = [
            [sg.Text('Selecione uma imagem:')],
            [sg.InputText(key='file_path'),
            sg.FileBrowse(target = 'file_path', initial_folder = diretorio, file_types =[('Arquivos de imagem', '.png .jpeg')]),
            sg.Button('Importar'),
            sg.Output(size = (100,40))
            ]
        ]
        self.criarJanela = sg.Window('Leitor de Cupons Fiscais').layout(layout)

    def leitorImagem(self, endereco_imagem):
        arquivo = cv2.imread(endereco_imagem)
        texto = pytesseract.image_to_string(arquivo)
        return texto


    def Iniciar(self):
        while True:
            self.evento, self.values = self.criarJanela.Read()
            if self.evento == sg.WIN_CLOSED:
                break

            if self.evento == 'Importar':
                print(self.values['file_path'])
                endereco_imagem = self.values['file_path']
                print(self.leitorImagem(endereco_imagem))

tela = Janela()
tela.Iniciar()
