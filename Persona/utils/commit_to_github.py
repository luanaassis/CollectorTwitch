import os
from git import Repo

def commit_and_push(file_path, commit_message, repo_path, branch_name="main"):
    """
    Faz o commit e push de um arquivo para o repositório GitHub.

    :param file_path: Caminho do arquivo a ser commitado (relativo ao repo).
    :param commit_message: Mensagem do commit.
    :param repo_path: Caminho para o repositório local.
    :param branch_name: Nome do branch (padrão: main).
    """
    try:
        # Verifica se o repositório local existe
        if not os.path.exists(repo_path):
            print("Repositório local não encontrado!")
            return
        
        # Abre o repositório
        repo = Repo(repo_path)

        # Garante que não existem problemas no repositório
        if repo.is_dirty(untracked_files=True):
            print("Certifique-se de que o repositório está limpo antes de continuar.")

        # Caminho completo do arquivo
        full_file_path = os.path.join(repo_path, file_path)

        # Adiciona o arquivo ao índice do Git
        repo.git.add(full_file_path)

        # Faz o commit
        repo.index.commit(commit_message)
        print(f"Commit realizado com sucesso: {commit_message}")

        # Verifica se o branch especificado existe
        if branch_name not in repo.heads:
            print(f"Branch {branch_name} não encontrado. Criando branch...")
            repo.git.branch(branch_name)

        # Faz o push para o repositório remoto
        origin = repo.remote(name="origin")
        origin.push(refspec=f"{branch_name}:{branch_name}")
        print(f"Arquivo enviado para o GitHub com sucesso no branch {branch_name}!")

    except Exception as e:
        print(f"Erro ao realizar o commit: {e}")
