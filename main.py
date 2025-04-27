from spreadsheet import Spreadsheet
import requests
import os


# Buscar ceps para consultar
pasta_input = os.path.join(os.getcwd(), "input")
pasta_output = os.path.join(os.getcwd(), "output")
if not os.path.exists(pasta_output):
    os.mkdir(pasta_output)

planilha = Spreadsheet(os.path.join(pasta_input, "ceps.xlsx"))
lista = list()

# Iniciando consultas dos ceps
for cep in planilha.get_data()["CEP"]:
    infos = dict()
    # Formata o CEP para 8 dígitos
    cep = str(cep).replace("-", "").zfill(8)
    url = f"https://viacep.com.br/ws/{cep}/json/"
    print("\n")

    res = requests.get(url, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
    })
    if res.status_code == 200:
        dados = res.json()
        print(dados)
    else:
        print("Erro ao consultar o CEP")

    # Adiciona os dados à planilha
    infos["CEP"] = cep
    infos["Logradouro"] = "Não encontrado" if not "logradouro" in dados or dados["logradouro"] == "" else dados["logradouro"]
    infos["Complemento"] = "Não encontrado" if not "complemento" in dados or dados["complemento"] == "" else dados["complemento"]
    infos["Bairro"] = "Não encontrado" if not "bairro" in dados or dados["bairro"] == "" else dados["bairro"]
    infos["Localidade"] = "Não encontrado" if not "localidade" in dados or dados["localidade"] == "" else dados["localidade"]
    infos["UF"] = "Não encontrado" if not "uf" in dados or dados["uf"] == "" else dados["uf"]
    infos["Estado"] = "Não encontrado" if not "estado" in dados or dados["estado"] == "" else dados["estado"]
    infos["Região"] = "Não encontrado" if not "regiao" in dados or dados["regiao"] == "" else dados["regiao"]
    infos["IBGE"] = "Não encontrado" if not "ibge" in dados or dados["ibge"] == "" else dados["ibge"]
    infos["DDD"] = "Não encontrado" if not "ddd" in dados or dados["ddd"] == "" else dados["ddd"]
    infos["SIAF"] = "Não encontrado" if not "siafi" in dados or dados["siafi"] == "" else dados["siafi"]
    lista.append(infos)

# Salvar resultados
print(lista)
planilha.save(lista, os.path.join(pasta_output, "dados.xlsx"))