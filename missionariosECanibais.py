import os
import copy

def cria_copia(alvo):
    return copy.deepcopy(alvo)

global_margem_esquerda = {
    'missionarios': 3,
    'canibais': 3,
}

global_margem_direita = {
    'missionarios': 0,
    'canibais': 0,
}

global_estado_jogo = {
    'margem_esquerda': global_margem_esquerda,
    'margem_direita': global_margem_direita,
    'barco': 'margem_esquerda',
}

def canibais_comem_missionarios(estado_jogo):
    margem_esquerda = estado_jogo['margem_esquerda']
    margem_direita = estado_jogo['margem_direita']
    if margem_esquerda['missionarios'] > 0 and margem_esquerda['missionarios'] < margem_esquerda['canibais']:
        return True
    if margem_direita['missionarios'] > 0 and margem_direita['missionarios'] < margem_direita['canibais']:
        return True
    return False

def jogo_ganho(estado_jogo):
    margem_esquerda = estado_jogo['margem_esquerda']
    margem_direita = estado_jogo['margem_direita']
    if margem_direita['missionarios'] == 3 and margem_direita['canibais'] == 3:
        return True
    return False

def transporta_pessoas_de_para(origem, destino, quantidade_missionarios=0, quantidade_canibais=0):
    origem_copia = cria_copia(origem)
    destino_copia = cria_copia(destino)
    transportou = False
    if origem['missionarios'] >= quantidade_missionarios and origem['canibais'] >= quantidade_canibais:
        origem_copia['missionarios'] -= quantidade_missionarios
        origem_copia['canibais'] -= quantidade_canibais
        destino_copia['missionarios'] += quantidade_missionarios
        destino_copia['canibais'] += quantidade_canibais
        transportou = True
    
    return transportou, origem_copia, destino_copia

def realiza_comando(estado_jogo, comando):
    novo_estado_jogo = cria_copia(estado_jogo)
    contrario = {
        'margem_direita': 'margem_esquerda',
        'margem_esquerda': 'margem_direita'
    }
    com_barco = novo_estado_jogo['barco']
    sem_barco = contrario[com_barco]
    margem_com_barco = novo_estado_jogo[com_barco]
    margem_sem_barco = novo_estado_jogo[sem_barco]

    quantidade_missionarios = 0
    quantidade_canibais = 0

    if comando == 'M M':
        quantidade_missionarios=2
    elif comando == 'C C':
        quantidade_canibais=2
    elif comando == 'M C' or comando == 'C M':
        quantidade_missionarios=1
        quantidade_canibais=1
    elif comando == 'M':
        quantidade_missionarios=1
    elif comando == 'C':
        quantidade_canibais=1
    
    transportou, margem_com_barco, margem_sem_barco = transporta_pessoas_de_para(margem_com_barco, margem_sem_barco, quantidade_missionarios, quantidade_canibais)
    
    if transportou:
        novo_estado_jogo['barco'] = sem_barco
        novo_estado_jogo[com_barco] = margem_com_barco
        novo_estado_jogo[sem_barco] = margem_sem_barco

    return novo_estado_jogo

def imprime_lugar(lugar):
    quantidade_missionarios = lugar['missionarios']
    quantidade_canibais = lugar['canibais']

    for _ in range(quantidade_missionarios):
        print('M ', end='')
    for _ in range(quantidade_canibais):
        print('C ', end='')
    for _ in range(6 - (quantidade_missionarios + quantidade_canibais)):
        print('_ ', end='')
    
    print('   ', end='')

def imprime_chao(barco_na_magem):
    barco_espaco_esquerda = ' '*3
    barco_espaco_direita = ' '*3

    if barco_na_magem == 'margem_esquerda':
        barco_espaco_esquerda = '<- '
    else:
        barco_espaco_direita = ' ->'

    print('margem esquerda ', end='')
    print(barco_espaco_esquerda+'barco'+barco_espaco_direita, end='')
    print(' margem direita ')

def imprime_estado_jogo(estado_jogo):
    imprime_lugar(estado_jogo['margem_esquerda'])
    print(' '*13, end='')
    imprime_lugar(estado_jogo['margem_direita'])
    print()
    imprime_chao(estado_jogo['barco'])

def limpa_tela():
    os.system('cls' if os.name=='nt' else 'clear')

def pega_comandos_usuario():
    print('\nPara atrevessar o rio utilize M (missionário) e C (canibal) ou X para sair ou se estiver cansado tente CONCLUIR')
    print('Comandos: "M C", "C M", "M M", "C C", "M", "C", "X", "CONCLUIR"')
    while True:
        comando = input('> ').upper().strip()
        comandos_possiveis = ["M C", "C M", "M M", "C C", "M", "C", "X", "CONCLUIR"]
        if comando in comandos_possiveis:
            return comando
        print('Vish! Comando errado, tenta de novo aí')


def inicia_jogo():
    estado_jogo = cria_copia(global_estado_jogo)
    terminou = False
    estados = []
    while(not terminou):
        limpa_tela()
        imprime_estado_jogo(estado_jogo)

        if estado_jogo in estados:
            print('\nVocê já esteve por aqui')
        else:
            estados.append(estado_jogo)

        comando = pega_comandos_usuario()

        if comando == 'X':
            terminou = True
            break
        elif comando == 'CONCLUIR':
            print('Modo Automático ligado!--------------------------------------------------\n')
            caminho = joga_automatico(estado_jogo, [estado_jogo])[2]
            imprime_jogo_automatico(caminho)
            print('Jogo Concluido XD')
            terminou = True
            break

        estado_jogo = realiza_comando(estado_jogo, comando)

        if canibais_comem_missionarios(estado_jogo):
            limpa_tela()
            imprime_estado_jogo(estado_jogo)
            print('\nOs canibais comeram um missionário')
            print('T.T')
            terminou = True
            break
        elif jogo_ganho(estado_jogo):
            print('Parabéns você ganhou! êeeeeee')
            terminou = True
            break

def joga_automatico(estado_inicial, estados_ja_visitados=[], caminho_realizado=[]):
    comandos = ["M", "C", "M C", "M M", "C C"]

    estados_visitados = estados_ja_visitados.copy()
    caminho_atual = caminho_realizado.copy()

    for comando in comandos:
        estado_candidato = estado_inicial
        estado_candidato = realiza_comando(estado_candidato, comando)

        perdeu = canibais_comem_missionarios(estado_candidato)
        if perdeu or estado_candidato == estado_inicial:
            continue

        if estado_candidato not in estados_visitados:
            estados_visitados.append(estado_candidato)
            caminho_atual.append((comando, estado_candidato))

            ganho = jogo_ganho(estado_candidato)
            if ganho:
                return False, estados_visitados, caminho_atual

            erro, estados, caminho = joga_automatico(estado_candidato, estados_visitados, caminho_atual)
            if not erro:
                return False, estados, caminho
            
            caminho_atual.pop()
    
    return True, None, None


def imprime_jogo_automatico(caminho):
    for comando, estado in caminho:
        print(f'\n> {comando}\n')
        imprime_estado_jogo(estado)

inicia_jogo()
