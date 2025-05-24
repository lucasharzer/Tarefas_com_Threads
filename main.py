from src import Spreadsheet, LogTerminal
from datetime import datetime
import requests
import os


class Execution:
    def __init__(self):
        # Definição de pastas
        self.pasta_input = os.path.join(os.getcwd(), "input")
        self.pasta_output = os.path.join(os.getcwd(), "output")

        # Buscar ceps para consultar
        self.planilha = Spreadsheet(os.path.join(self.pasta_input, "ceps.xlsx"))
        self.lista = list()

        # geração e gerenciamento de logs de execução
        self.pasta_logs = os.path.join(os.getcwd(), "logs")
        if not os.path.exists(self.pasta_logs):
            os.makedirs(self.pasta_logs)

        # Gerenciamento dos logs
        data = datetime.now()
        arquivo = os.path.join(self.pasta_logs, f"CEPs_{data.strftime('%Y-%m-%d')}.txt")

        for arq in os.listdir(self.pasta_logs):
            caminho = os.path.join(self.pasta_logs, arq)
            dia = datetime.fromtimestamp(os.path.getctime(caminho))
            if (data - dia).days >= 3:
                os.remove(caminho)

        self.log = LogTerminal(arquivo)
    
    def create_folder(self):
        if not os.path.exists(self.pasta_output):
            os.mkdir(self.pasta_output)

    def start_consult(self, cep):
        infos = dict()
        # Formata o CEP para 8 dígitos
        cep = str(cep).replace("-", "").zfill(8)
        url = f"https://viacep.com.br/ws/{cep}/json/"
        self.log.gerar_log("\n")

        res = requests.get(url, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
        })
        if res.status_code == 200:
            dados = res.json()
            self.log.gerar_log(dados)
        else:
            self.log.gerar_log("Erro ao consultar o CEP")

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

        return infos
    
    def tradicional_run(self):
        self.create_folder()

        for cep in self.planilha.get_data()["CEP"]:
            resuldato = self.start_consult(cep)
            self.lista.append(resuldato)

        # Salvar resultados
        self.log.gerar_log(self.lista)
        self.planilha.save(self.lista, os.path.join(self.pasta_output, "dados.xlsx"))


if __name__ == "__main__":
    execute = Execution()
    # Executando consultas de maneira convencional: sequencialmente
    execute.tradicional_run()