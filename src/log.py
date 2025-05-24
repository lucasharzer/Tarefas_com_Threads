from datetime import datetime
import os


class LogTerminal:
    def __init__(self, arquivo):
        self.arquivo = arquivo

        if not os.path.exists(self.arquivo):
            with open(self.arquivo, "w"):
                pass
    
    def gerar_log(self, log):
        horario = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        with open(self.arquivo, "a", encoding="utf-8") as file:
            print(log)
            if hasattr(log, "replace"):
                log = log.replace('\n', ' ')
            file.write(f"[{horario}] {log}\n")