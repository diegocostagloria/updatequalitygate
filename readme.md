# SonarQube Quality Gate Updater

Este projeto contém um script em Python que atualiza o Quality Gate de projetos no SonarQube. Ele lê uma lista de nomes de projetos de um arquivo de texto, verifica o Quality Gate atual de cada projeto e atualiza o Quality Gate se ele não estiver na lista de Quality Gates esperados.

## Funcionalidades

- Lê uma lista de projetos a partir de um arquivo `project_list.txt`.
- Recupera o `project_key` de cada projeto no SonarQube.
- Verifica o Quality Gate atual de cada projeto.
- Atualiza o Quality Gate de um projeto se ele não estiver na lista de Quality Gates esperados.

## Pré-requisitos

- Python 3.6 ou superior.
- Biblioteca `requests` para fazer chamadas à API do SonarQube.
- Acesso ao SonarQube com permissões suficientes para ler e atualizar Quality Gates.

## Configuração

### Instalar dependências

Instale a biblioteca `requests` se ainda não tiver:

```sh
pip install requests
