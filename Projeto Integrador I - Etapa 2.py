import mysql.connector
from mysql.connector import Error
from tabulate import tabulate

try:
    # Conecta ao banco de dados MySQL
    con = mysql.connector.connect(host='localhost',  
                                   database='cadastro',
                                   user='root',
                                   password='')

    if con.is_connected():
        print("Conectado ao banco de dados MySQL")

        # Consulta SQL para selecionar todos os registros da tabela 
        consulta_sql = "select * from produtos"

        cursor = con.cursor()
        cursor.execute(consulta_sql)
        linhas = cursor.fetchall()

        if cursor.rowcount > 0:
            print("Número total de registros retornados:", cursor.rowcount)
            print("\nMostrando os autores cadastrados:")
            for linha in linhas:
                cod=linha[0]
                np=linha[1]
                des=linha[2]
                cp=linha[3]
                cf=linha[4]
                cv=linha[5]
                imp=linha[6]
                rent=linha[7]               
                
                try:

                    if cf + cv + imp + rent >= 100:
                        print("Erro: A soma dos custos e despesas é igual ou maior que 100%. Não é possível calcular o preço de venda.")
                    else:
                        pv = cp / (1 - ((cf + cv + imp + rent) / 100))

                        cpp = (cp / pv) * 100
                        cfd = (cf / 100) * pv
                        cvd = (cv / 100) * pv
                        impd = (imp / 100) * pv
                        rentd = (rent / 100) * pv

                        if rent > 20:
                            lucro = '\033[4;34mAlta\033[m'
                        elif rent > 10 and rent <= 20:
                            lucro = '\033[4;32mMédia\033[m'
                        elif rent > 0 and rent <= 10:
                            lucro = '\033[4;33mBaixa\033[m'
                        elif rent == 0:
                            lucro = '\033[4;97mEquilibrada\033[m'
                        elif rent < 0:
                            lucro = '\033[4;31mPrejuízo\033[m'

                        tabela = [['\033[1mDescrição\033[m', '\033[1mValor\033[m', '\033[1m(%)\033[m'],
                                    ['Preço de Venda', f'R$ {pv:.2f}', '100.0%'],
                                    ['Custo do Produto', f'R$ {cp:.2f}', f'{cpp:.2f}%'],
                                    ['Custo Fixo/Administrativo', f'R$ {cfd:.2f}', f'{cf:.2f}%'],
                                    ['Comissão de Vendas', f'R$ {cvd:.2f}', f'{cv:.2f}%'],
                                    ['Impostos', f'R$ {impd:.2f}', f'{imp:.2f}%'],
                                    [f'Rentabilidade → {lucro}', f'R$ {rentd:.2f}', f'{rent:.2f}%']]
                        
                        print(cod,'-',np,des)
                        print(tabulate(tabela))

                except ValueError:
                    print('Entrada inválida. Precisa ser um número.')
        else:
            print("Nenhum registro encontrado.")

except Error as e:
    print("Erro ao acessar tabela MySQL:", e)

finally:
    # Fecha o cursor e a conexão com o banco de dados, se estiverem abertos
    if 'con' in locals() and con.is_connected():
        cursor.close()
        con.close()
        print("Conexão ao MySQL encerrada.")