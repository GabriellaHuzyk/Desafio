import gspread
import math
from oauth2client.service_account import ServiceAccountCredentials

from pprint import pprint

scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]

creds=ServiceAccountCredentials.from_json_keyfile_name("desafio.json", scope)

client = gspread.authorize(creds)

sheet = client.open("Engenharia de Software – Desafio Gabriella Huzyk").sheet1

data = sheet.get_all_records()



for linha in range(4,28):
    pprint(sheet.row_values(linha)) #Aqui o python faz a leitura da planilha como string.

    if float(sheet.cell(linha,3).value)<0.25*60: #Condição que verifica o número de faltas.
        sheet.update_cell(linha,7, "Reprovado por falta") #Anota na planilha a situação do aluno, caso ele esteja reprovado por falta.
        sheet.update_cell(linha,8, "0") #Insere o número 0 em  nota para aprovação final.
        continue #O if passa por todas as linhas da planilha nestas colunas.

    #Cálculo da média. O Float foi necessário para que o programa converta a string que ele leu na planilha em números flutuantes.
    p1 = float(sheet.cell(linha,4).value) #Indica o local de cada nota na planilha.
    p2 = float(sheet.cell(linha,5).value)
    p3 = float(sheet.cell(linha,6).value)
    media = math.ceil((p1+p2+p3)/3) #O math.ceil arredonda o número para o próximo número inteiro, caso seja necessário.
    print("A média é: ", media)


    if media < 50 : #Segunda condição: Se a media for menor que 50 então o aluno estará reprovado.
        sheet.update_cell(linha,7, "Reprovado por nota") #Indica o local e o que o programa deve escrever na situação do aluno.
        sheet.update_cell(linha,8, "0") #Indica o campo Nota para aprovação. Caso o aluno esteja reprovado, o resultado será zero.



    elif media >= 70 : #Terceira condição: Se a média for maior ou igual a 70 o aluno estará aprovado.
        sheet.update_cell(linha,7, "Aprovado") #Situação.
        sheet.update_cell(linha,8, "0") #Nota para aprovação final.


    else: #Quarta e última condição. Caso o aluno não se encontre em nenhuma das outras duas condições, esta será aplicada.
        sheet.update_cell(linha,7, "Exame final") #Situação do aluno.
        naf = 100 - media #A nota para aprovação final.
        sheet.update_cell(linha,8,naf) #Escreve o valor na coluna indicada.



