import mysql.connector
from mysql.connector import Error
from tabulate import tabulate

def conectar(host, database, user, password):
    try:
        con = mysql.connector.connect(host = host,  
                                      database = database,
                                      user = user,
                                      password = password)
        if con.is_connected():
            print("Conectado ao banco de dados MySQL\n")
        return con
    except Error as e:
        print("Erro ao conectar ao banco de dados MySQL:", e)
        return None

def desconectar(con):
    if con.is_connected():
        con.close()
        print("Conexão ao MySQL encerrada.")

def listar(con):
    try:
        consulta_sql = "SELECT * FROM produtos"
        cursor = con.cursor()
        cursor.execute(consulta_sql)
        linhas = cursor.fetchall()

        if cursor.rowcount > 0:
            print("Número total de registros retornados:", cursor.rowcount)
            for linha in linhas:
                cod = linha[0]
                np = linha[1]
                des = linha[2]
                cp = linha[3]
                cf = linha[4]
                cv = linha[5]
                imp = linha[6]
                rent = linha[7]

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
                        
                        print(cod, '-', np, des)
                        print(tabulate(tabela))

                except ValueError:
                    print('Entrada inválida. Precisa ser um número.')
                    return
        else:
            print("Nenhum registro encontrado.")
    except Error as e:
        print("Erro ao acessar tabela MySQL:", e)

def inserir(con):
    try:
        cursor = con.cursor()
        cod = int(input('Digite o código do produto: '))

        # Verificar se o produto existe
        check_sql = "SELECT COUNT(*) FROM produtos WHERE cod = %s"
        cursor.execute(check_sql, (cod,))
        result = cursor.fetchone()

        if result[0] != 0:
            print("Produto com o código fornecido já existe.")
            return
        
        np = input('Digite o nome do produto: ')
        if np=='':
            print('O produto precida ter um nome')
            return
        des = input('Faça uma descrição do produto: ')
        cp = float(input('Digite o custo do produto (R$): '))
        cf = float(input('Digite o percentual do custo fixo/administrativo do produto (%): '))
        cv = float(input('Digite o percentual da comissão de vendas (%): '))
        imp = float(input('Digite o percentual dos impostos (%): '))
        rent = float(input('Digite o percentual da rentabilidade (%): '))
        
        insert_sql = 'INSERT INTO produtos (cod, np, des, cp, cf, cv, imp, rent) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'
        cursor.execute(insert_sql, (cod, np, des, cp, cf, cv, imp, rent))
        con.commit()
        print("Registro inserido com sucesso.")
    except Error as e:
        print("Erro ao inserir registro no MySQL: Valores acima do limite")
        return
    except ValueError:
        print('O valor deve ser numérico')
        return

def atualizar(con):
    try:
        cursor = con.cursor()
        cod = int(input("Código do Produto a ser atualizado: "))

        # Verificar se o produto existe
        check_sql = "SELECT COUNT(*) FROM produtos WHERE cod = %s"
        cursor.execute(check_sql, (cod,))
        result = cursor.fetchone()

        if result[0] == 0:
            print("Produto com o código fornecido não encontrado.")
            return
        
        print()

        print('~'*30)
        print('''1. Nome do produto
2. Descrição do produto
3. Custo do produto
4. Custo Fixo/Administrativo
5. Comissão de Vendas
6. Impostos
7. Rentabilidade''')
        print('~'*30)
        n = int(input('O que você gostaria de atualizar ?: '))

        # Definir a coluna a ser atualizada com base na escolha do usuário
        if n == 1:
            coluna = 'np'
            novo_valor = input("Digite o novo nome: ")
            if novo_valor=='':
                print('O produto precida ter um nome')
                return
        elif n == 2:
            coluna = 'des'
            novo_valor = input("Digite a nova descrição: ")
        elif n == 3:
            coluna = 'cp'
            novo_valor = float(input("Digite o novo custo: "))
        elif n == 4:
            coluna = 'cf'
            novo_valor = float(input("Digite o novo Custo Fixo/Administrativo: "))
        elif n == 5:
            coluna = 'cv'
            novo_valor = float(input("Digite a nova Comissão de Vendas: "))
        elif n == 6:
            coluna = 'imp'
            novo_valor = float(input("Digite os novos impostos: "))
        elif n == 7:
            coluna = 'rent'
            novo_valor = float(input("Digite a nova rentabilidade: "))
        else:
            print('Número inválido')
            return

        # Obter o valor atual do campo selecionado
        select_sql = f"SELECT {coluna} FROM produtos WHERE cod = %s"
        cursor.execute(select_sql, (cod,))
        valor_atual = cursor.fetchone()[0]

        # Atualizar o campo com o novo valor
        update_sql = f'UPDATE produtos SET {coluna} = %s WHERE cod = %s'
        cursor.execute(update_sql, (novo_valor, cod))
        con.commit()

        print(f"Registro atualizado com sucesso.\nAntes: {valor_atual}\nDepois: {novo_valor}")
    except Error as e:
        print("Erro ao atualizar registro no MySQL: Valores acima do limite")
        return
    except ValueError:
        print('O valor deve ser numérico')
        return


def deletar(con):
    try:
        cursor = con.cursor()
        cod = int(input("Código do Produto a ser deletado: "))

        # Verificar se o produto existe
        check_sql = "SELECT COUNT(*) FROM produtos WHERE cod = %s"
        cursor.execute(check_sql, (cod,))
        result = cursor.fetchone()

        if result[0] == 0:
            print("Produto com o código fornecido não encontrado.")
            return

        delete_sql = "DELETE FROM produtos WHERE cod = %s"
        cursor.execute(delete_sql, (cod,))
        con.commit()
        print("Registro deletado com sucesso.")
    except Error as e:
        print("Erro ao deletar registro no MySQL:", e)
        return
    except ValueError:
        print('O valor deve ser numérico')
        return

#Programa Principal
con = conectar(host='localhost', database='cadastro', user='root', password='')
if con:
    while True:
        print('=-'*30)
        print("Menu CRUD")
        print("1. Mostrar todos os registros")
        print("2. Inserir novo registro")
        print("3. Atualizar registro")
        print("4. Deletar registro")
        print("5. Sair")
        print('=-'*30)
        opcao = input("Escolha uma opção: ")
        

        if opcao == '1':
            listar(con)
        elif opcao == '2':
            inserir(con)
        elif opcao == '3':
            atualizar(con)
        elif opcao == '4':
            deletar(con)
        elif opcao == '5':
            break
        else:
            print("Opção inválida. Tente novamente.")

    desconectar(con)

