from flask import Flask, jsonify, request
import requests
from bs4 import BeautifulSoup
import json

app = Flask(__name__)

def paginaRequest():
    page = requests.get('https://pncp.gov.br/api/search/?tipos_documento=edital&ordenacao=-data&pagina=1&tam_pagina=20&status=recebendo_proposta')
    pageHTML = BeautifulSoup(page.text,'html.parser')
    vetor = str(pageHTML)
    novoDado = json.loads(vetor)

    listaId = []
    for i in novoDado["items"]:
        cnpj = i["orgao_cnpj"]
        sequencial = i["numero_sequencial"]
        ano = i["ano"]
        estruturaJson = {"orgao_cnpj": cnpj, "numero_sequencial": sequencial, "ano": ano}
        listaId.append(estruturaJson)

    listaRequisicoesItem = []
    i = 0
    while i < len(listaId):
        requisicaoItem = 'https://pncp.gov.br/api/pncp/v1/orgaos/' + listaId[i]["orgao_cnpj"] + '/compras/' + listaId[i]["ano"] + '/' + listaId[i]["numero_sequencial"] + '/itens'
        listaRequisicoesItem.append(requisicaoItem)
        i += 1

    listaRequisicoesCompra = []
    j = 0
    while j < len(listaId):
        requisicaoCompra = 'https://pncp.gov.br/api/pncp/v1/orgaos/' + listaId[j]["orgao_cnpj"] + '/compras/' + listaId[j]["ano"] + '/' + listaId[j]["numero_sequencial"]
        listaRequisicoesCompra.append(requisicaoCompra)
        j += 1

    requisicoesUnificadas = []
    k = 0
    while k < len(listaId):
        itemUnificado = {"detalhesCompra": listaRequisicoesCompra[k], "detalhesItens": listaRequisicoesItem[k]}
        requisicoesUnificadas.append(itemUnificado)
        k += 1

    return requisicoesUnificadas

@app.route('/microtecnica/pncp/licitacoes')
def getLicitacoes():
    return paginaRequest()

app.run(port=5000,host='127.0.0.1',debug=True)