from pytesseract import pytesseract
import csv, os, cv2, re
import PySimpleGUI as sg
import pandas as pd

diretorio = os.getcwd()

class Janela():
    def __init__(self):
        layout = [
            [sg.Push(), sg.Text('Selecione uma imagem:'), sg.InputText(key='file_path'),
            sg.FileBrowse(target = 'file_path', initial_folder = diretorio, file_types =[('Arquivos de imagem', '.png .jpeg')]),
            sg.Button('Importar')],
            [sg.Output(size = (80,10))],
            [sg.Text('Nomeie seu arquivo (opcional):'), sg.InputText(key='nome_arquivo')],
            [sg.Button('Confirmar e exportar', key = 'confirmar')],
        ]
        self.criarJanela = sg.Window('Leitor de Cupons Fiscais').layout(layout)

    def leitorImagem(self, endereco_imagem):
        dict_itens = dict.fromkeys(['Descricao', 'Quantidade', 'Valor'])
        vetor_nomes = []
        regex = re.compile(r'^[0-9]+\s+[0-9]+\s+((\S+(?:\s*\S*)*?)\s+([0-9]+(?:,[0-9]+)?)\s+\w\w)\s+.*\s+([0-9]+(?:,[0-9]+)?)$', flags=re.M)
        texto_imagem = pytesseract.image_to_string(cv2.imread(endereco_imagem))

        if(texto_imagem == ''):
            sg.popup('Nenhuma informação foi encontrada')

        for match in regex.finditer(texto_imagem):
            dict_itens['Descricao'] = match.group(2)
            dict_itens['Quantidade'] = match.group(3)
            dict_itens['Valor'] = match.group(4)
            
            vetor_nomes.append(dict_itens.copy())

        return vetor_nomes

    def criar_csv(self, nome_temp, vetor_nomes):
        if(nome_temp == ''):
            nome_temp = 'meuarquivo'
        
        nome_arquivo = nome_temp + '.csv'
        arquivo_csv = open(nome_arquivo, 'w')
        with open(nome_arquivo,'w', newline = '') as arquivo:
            escreve = csv.DictWriter(arquivo, fieldnames = vetor_nomes[0].keys())
            escreve.writeheader()
            escreve.writerows(vetor_nomes)

        df = pd.read_csv(nome_arquivo, decimal = ',')
        soma_itens = df['Quantidade'].sum()
        soma_valores = df['Valor'].sum()
        df.loc[len(df)] = ['TOTAL', soma_itens, soma_valores]
        df.to_csv(nome_arquivo, mode='w', index = False, header = True)
        print(df)

        return True

    def Iniciar(self):
        self.dados_itens = []
        while True:
            self.evento, self.values = self.criarJanela.Read()
            if self.evento == sg.WIN_CLOSED:
                break

            if self.evento == 'Importar':
                if( self.values['file_path'] == ''):
                    sg.popup('Selecione um arquivo')
                else:
                    print(self.values['file_path']+'\n')
                    endereco_imagem = self.values['file_path']
                    self.dados_itens_temp = self.leitorImagem(endereco_imagem)
                    self.dados_itens = self.dados_itens + self.dados_itens_temp
                    print(self.dados_itens)

            if self.evento == 'confirmar':
                self.criar_csv(self.values['nome_arquivo'], self.dados_itens)
                sg.popup('Operação realizada com sucesso!')

tela = Janela()
tela.Iniciar()
