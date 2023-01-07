from pytesseract import pytesseract
import csv
import cv2
import re
import PySimpleGUI as sg
import os 

diretorio = os.getcwd()

class Janela():
    def __init__(self):
        #sg.Theme('Reddit')
        layout = [
            [sg.Text('Selecione uma imagem:'), sg.InputText(key='file_path'),
            sg.FileBrowse(target = 'file_path', initial_folder = diretorio, file_types =[('Arquivos de imagem', '.png .jpeg')]),
            sg.Button('Importar')],
            [sg.Text('Nomeie seu arquivo:'), sg.InputText(key='nome_arquivo')],
            [sg.Button('Confirmar e exportar', key = 'confirmar')],
            #sg.Output(size = (50,10))
        ]
        self.criarJanela = sg.Window('Leitor de Cupons Fiscais').layout(layout)

    def leitorImagem(self, endereco_imagem):
        dict_itens = dict.fromkeys(['Descricao', 'Quantidade', 'Valor'])
        vetor_nomes = []
        regex = re.compile(r'^[0-9]+\s+[0-9]+\s+((\S+(?:\s*\S*)*?)\s+([0-9]+(?:,[0-9]+)?)\s+\w\w)\s+.*\s+([0-9]+(?:,[0-9]+)?)$', flags=re.M)
        texto_imagem = pytesseract.image_to_string(cv2.imread(endereco_imagem))

        for match in regex.finditer(texto_imagem):
            dict_itens['Descricao'] = match.group(2)
            dict_itens['Quantidade'] = match.group(3)
            dict_itens['Valor'] = match.group(4)
            
            vetor_nomes.append(dict_itens.copy())

        return vetor_nomes

    def criar_csv(self, nome_arquivo, vetor_nomes):
        if(nome_arquivo == None):
            nome_arquivo = 'meuarquivo'
        arquivo_csv = open('${nome_arquivo}.csv', 'w')
        with open('${nome_arquivo}.csv','w', newline = '') as arquivo:
            escreve = csv.DictWriter(arquivo, fieldnames = vetor_nomes[0].keys())
            escreve.writeheader()
            escreve.writerows(vetor_nomes)

        return True

    def Iniciar(self):
        self.dados_itens = []
        while True:
            self.evento, self.values = self.criarJanela.Read()
            if self.evento == sg.WIN_CLOSED:
                break

            if self.evento == 'Importar':
                print(self.values['file_path'])
                endereco_imagem = self.values['file_path']
                self.dados_itens_temp = self.leitorImagem(endereco_imagem)
                self.dados_itens = self.dados_itens + self.dados_itens_temp
                print(self.dados_itens)

            if self.evento == 'confirmar':
                self.criar_csv(self.values['nome_arquivo'], self.dados_itens)
                if(self.leitorImagem(endereco_imagem) == True):
                    print('Operação realizada com sucesso!')

tela = Janela()
tela.Iniciar()
