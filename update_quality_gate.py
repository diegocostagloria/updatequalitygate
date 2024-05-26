import requests
import json
import os
import base64

# Defina a URL do seu SonarQube e as credenciais de autenticação
SONARQUBE_URL = os.getenv("SONARQUBE_URL", "http://localhost:9001")
SONARQUBE_TOKEN = os.getenv("SONARQUBE_TOKEN", "squ_ec3d9b77b0e832ec1747b4c6021f949680c0df7b")
EXPECTED_QUALITY_GATES = ["Gate1", "Gate2", "sonar-way"]  # Substitua pelos nomes dos Quality Gates esperados

# Cabeçalho de autenticação
auth_header = {
    'Authorization': f'Basic {base64.b64encode((SONARQUBE_TOKEN + ":").encode()).decode()}'
}

# Função para obter o Quality Gate de um projeto
def get_quality_gate(project_key):
    url = f"{SONARQUBE_URL}/api/qualitygates/project_status"
    params = {"projectKey": project_key}
    response = requests.get(url, headers=auth_header, params=params)
    if response.status_code == 200:
        project_status = response.json()
        return project_status.get("projectStatus", {}).get("qualityGateStatus", "Unknown")
    else:
        print(f"Erro ao obter o Quality Gate para o projeto {project_key}: {response.status_code}")
        return None

# Função para atualizar o Quality Gate de um projeto
def set_quality_gate(project_key, gate_name):
    url = f"{SONARQUBE_URL}/api/qualitygates/select"
    params = {"projectKey": project_key, "gateName": gate_name}
    print(f"Parâmetros enviados: {params}")  # Adiciona o print aqui para verificar os parâmetros
    response = requests.post(url, headers=auth_header, params=params)
    if response.status_code == 204:
        print(f"Quality Gate do projeto {project_key} atualizado para {gate_name}")
    elif response.status_code == 400:
        print(f"Erro ao atualizar o Quality Gate para o projeto {project_key}: 400 - Solicitação inválida. Verifique o nome do Quality Gate e a chave do projeto.")
    elif response.status_code == 401:
        print(f"Erro ao atualizar o Quality Gate para o projeto {project_key}: 401 - Não autorizado. Verifique seu token de autenticação.")
    elif response.status_code == 403:
        print(f"Erro ao atualizar o Quality Gate para o projeto {project_key}: 403 - Permissões insuficientes. Verifique as permissões do token.")
    else:
        print(f"Erro ao atualizar o Quality Gate para o projeto {project_key}: {response.status_code}")

# Função para obter o project_key pelo nome do projeto
def get_project_key(project_name):
    url = f"{SONARQUBE_URL}/api/projects/search"
    params = {"q": project_name}
    response = requests.get(url, headers=auth_header, params=params)
    if response.status_code == 200:
        projects = response.json().get("components", [])
        for project in projects:
            if project.get("name") == project_name:
                return project.get("key")
        print(f"Projeto {project_name} não encontrado.")
        return None
    elif response.status_code == 401:
        print(f"Erro ao buscar o projeto {project_name}: 401 - Não autorizado. Verifique seu token de autenticação.")
        return None
    elif response.status_code == 403:
        print(f"Erro ao buscar o projeto {project_name}: 403 - Permissões insuficientes. Verifique as permissões do token.")
        return None
    else:
        print(f"Erro ao buscar o projeto {project_name}: {response.status_code}")
        return None

# Ler a lista de projetos do arquivo txt
def read_project_list(file_path):
    with open(file_path, "r") as file:
        projects = file.read().splitlines()
    return projects

# Função principal
def main():
    file_path = "project_list.txt"  # Caminho para o arquivo txt com a lista de projetos
    projects = read_project_list(file_path)

    for project_name in projects:
        project_key = get_project_key(project_name)
        if project_key:
            current_quality_gate = get_quality_gate(project_key)
            if current_quality_gate and current_quality_gate not in EXPECTED_QUALITY_GATES:
                set_quality_gate(project_key, EXPECTED_QUALITY_GATES[0])  # Defina para o primeiro Quality Gate da lista esperada

if __name__ == "__main__":
    main()