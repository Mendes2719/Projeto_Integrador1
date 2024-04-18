from tabulate import tabulate

try:
    cod = int(input('Digite o código do produto: '))
    np = input('Digite o nome do produto: ')
    des = input('Faça uma descrição do produto: ')
    cp = float(input('Digite o custo do produto (R$): '))
    cf = float(input('Digite o percentual do custo fixo/administrativo do produto (%): '))
    cv = float(input('Digite o percentual da comissão de vendas (%): '))
    imp = float(input('Digite o percentual dos impostos (%): '))
    rent = float(input('Digite o percentual da rentabilidade (%): '))

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

        print(tabulate(tabela))

except ValueError:
    print('Entrada inválida. Precisa ser um número.')
