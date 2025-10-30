from fila import Fila
from paciente import Paciente
from nodo_arvore import NodoArvore
import datetime

class SistemaTriagem:
    def __init__(self):
        self.arvores_triagem = self._montar_todos_fluxogramas()
        self.lista_queixas = list(self.arvores_triagem.keys())

        self.filas = {
            "Vermelho": Fila(), "Laranja": Fila(), "Amarelo": Fila(),
            "Verde": Fila(), "Azul": Fila()
        }
        self.ordem_prioridade = ["Vermelho", "Laranja", "Amarelo", "Verde", "Azul"]
        self.log_file = "log_atendimentos.txt"

    def _montar_todos_fluxogramas(self):
        f_verm = NodoArvore("Vermelho - Emergência")
        f_laran = NodoArvore("Laranja - Muito Urgente")
        f_amar = NodoArvore("Amarelo - Urgente")
        f_verd = NodoArvore("Verde - Pouco Urgente")
        f_azul = NodoArvore("Azul - Não Urgente")

        q_queixa_recente = NodoArvore("O paciente tem uma queixa/sintoma recente?")
        q_dor = NodoArvore("Está com dor intensa?")
        q_consciente = NodoArvore("Está consciente?")
        raiz_geral = NodoArvore("O paciente está respirando?")
        q_queixa_recente.sim, q_queixa_recente.nao = f_verd, f_azul
        q_dor.sim, q_dor.nao = f_amar, q_queixa_recente
        q_consciente.sim, q_consciente.nao = q_dor, f_laran
        raiz_geral.sim, raiz_geral.nao = q_consciente, f_verm
        
        q_dor_subita = NodoArvore("A dor de cabeça foi súbita e severa (pior da vida)?")
        q_sintomas_neuro = NodoArvore("Há sintomas neurológicos (fraqueza, confusão, problema de fala)?")
        raiz_cefaleia = NodoArvore("A dor de cabeça começou há menos de 24h?")
        q_dor_subita.sim, q_dor_subita.nao = f_laran, f_amar
        q_sintomas_neuro.sim, q_sintomas_neuro.nao = f_laran, q_dor_subita
        raiz_cefaleia.sim, raiz_cefaleia.nao = q_sintomas_neuro, f_verd

        return {
            "Geral / Outros": raiz_geral,
            "Dor de Cabeça": raiz_cefaleia
        }

    def adicionar_paciente_fila(self, paciente, cor):
        cor_base = cor.split(' ')[0]
        if cor_base in self.filas:
            self.filas[cor_base].enqueue(paciente)
            return True
        return False
    
    def chamar_proximo_paciente(self):
        for cor in self.ordem_prioridade:
            if not self.filas[cor].esta_vazia():
                paciente = self.filas[cor].dequeue()
                self._logar_atendimento(cor, paciente)
                return cor, paciente
        return None, None

    def _logar_atendimento(self, cor, paciente):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] ATENDIDO: Fila {cor} - {paciente}\n"
        try:
            with open(self.log_file, "a") as f: f.write(log_message)
        except IOError: pass 

    def get_status_filas(self):
        status = [f"Fila {cor}: {self.filas[cor].tamanho()} paciente(s)" for cor in self.ordem_prioridade]
        return "\n".join(status)

    def get_log(self, ultimas_n=10):
        try:
            with open(self.log_file, "r") as f:
                linhas = f.readlines()
            if not linhas: return "O log de atendimentos está vazio."
            return "".join(linhas[-ultimas_n:])
        except FileNotFoundError:
            return "Nenhum paciente foi atendido ainda. O log está vazio."