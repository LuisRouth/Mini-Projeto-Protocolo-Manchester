# Mini-Projeto - Protocolo de Manchester

![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)

## Segunda Avaliação - Protocolo de Manchester

Este projeto é uma implementação em Python de um sistema de triagem de pacientes baseado no Protocolo de Manchester, desenvolvido como parte da avaliação da disciplina de Estrutura de Dados na Fatec Rio Claro.

## Sobre o Projeto

O objetivo deste sistema é simular o processo de triagem de emergência hospitalar, classificando os pacientes por nível de prioridade com base em suas queixas e sintomas. O sistema utiliza estruturas de dados fundamentais para gerenciar a lógica de classificação e as filas de espera.

## Funcionalidades Principais

-   **Duas Interfaces de Usuário:** O usuário pode escolher entre interagir via **Terminal (console)** ou através de uma **Interface Gráfica (GUI)** construída com Tkinter.
-   **Triagem Baseada em Fluxogramas:** O sistema replica a lógica real do Protocolo de Manchester, onde a triagem começa com a **queixa principal** do paciente (ex: "Dor de Cabeça"), selecionando a árvore de decisão (fluxograma) apropriada.
-   **Classificação por Cores:** Pacientes são classificados em 5 níveis de prioridade, representados por cores:
    -   🔴 **Vermelho** (Emergência)
    -   🟠 **Laranja** (Muito Urgente)
    -   🟡 **Amarelo** (Urgente)
    -   🟢 **Verde** (Pouco Urgente)
    -   🔵 **Azul** (Não Urgente)
-   **Filas de Prioridade:** Cada nível de urgência possui uma fila de espera independente que opera no modelo **FIFO** (First-In, First-Out).
-   **Gerenciamento de Pacientes:** O sistema permite cadastrar novos pacientes, chamar o próximo paciente de maior prioridade disponível e visualizar o status de todas as filas.
-   **Log de Atendimentos:** Todas as chamadas de pacientes são registradas em um arquivo de log (`log_atendimentos.txt`) com data e hora, podendo ser consultadas através da interface.
-   **Validação de Entradas:** O nome do paciente não pode conter números ou ser deixado em branco, garantindo a integridade dos dados.

## Tecnologias e Conceitos Utilizados

-   **Linguagem:** Python 3
-   **Biblioteca Gráfica:** Tkinter (com o módulo `ttk` para uma aparência mais moderna)
-   **Estruturas de Dados Fundamentais:**
    -   **Árvore de Decisão:** Implementada com uma classe `NodoArvore` para guiar a triagem através de perguntas.
    -   **Fila (Queue):** Implementada com uma classe `Fila` para gerenciar a espera dos pacientes, garantindo a ordem de chegada (FIFO) dentro de cada prioridade.
-   **Princípios de Software:**
    -   **Programação Orientada a Objetos (POO):** O projeto é altamente modularizado em classes (`SistemaTriagem`, `Paciente`, `GuiApplication`, etc.).
    -   **Separação de Preocupações (SoC):** A lógica do sistema (backend) é completamente separada da apresentação (frontend), permitindo que tanto a interface de console quanto a gráfica utilizem o mesmo "motor" sem modificações.

## Como Executar

O projeto foi consolidado em um **único arquivo fonte** (`main.py`) para facilitar a entrega e execução.

1.  **Pré-requisitos:**
    -   Ter o [Python 3](https://www.python.org/downloads/) instalado em seu sistema.

2.  **Execução:**
    -   Abra um terminal ou prompt de comando.
    -   Navegue até o diretório onde você salvou o arquivo `main.py`.
    -   Execute o seguinte comando:
        ```bash
        python main.py
        ```
    -   Ao iniciar, o programa perguntará qual interface você deseja utilizar:
        ```
        Escolha a interface para o sistema:
        1. Terminal (baseado em texto)
        2. Interface Gráfica (GUI)
        0. Sair
        ```
    -   Digite `1` ou `2` e pressione Enter para iniciar o sistema na interface de sua escolha.

## Arquitetura do Projeto (em um único arquivo)

Embora o código esteja em um só arquivo, ele foi desenvolvido e está organizado logicamente em camadas:

1.  **Estruturas de Dados (`NodoArvore`, `Fila`, `Paciente`):** A base de tudo, definindo como os dados são estruturados e manipulados.
2.  **Backend (`SistemaTriagem`):** O "cérebro" da aplicação. Contém toda a lógica de negócio, montagem das árvores, gerenciamento das filas e geração do log. É completamente agnóstico à interface.
3.  **Frontend (Interfaces):** A "face" da aplicação. Duas classes são responsáveis por apresentar os dados e capturar as entradas do usuário:
    -   `ConsoleInterface`: Para a experiência no terminal.
    -   `GuiApplication`: Para a experiência gráfica com janelas e botões.
4.  **Lançador (`main`):** O ponto de entrada que simplesmente pergunta ao usuário qual "face" ele quer usar para interagir com o "cérebro".