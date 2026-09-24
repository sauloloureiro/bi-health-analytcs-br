import os
import sys
from ftplib import FTP

# ⚙️ CONFIGURAÇÕES DA PIPELINE NACIONAL
# Lista com a sigla de TODOS os 27 estados do Brasil
ESTADOS_BRASIL = [
    "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", 
    "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", 
    "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"
]
ANOS_FOCO = ["24", "25", "26"]  # Anos recentes e estratégicos para o produto comercial
PASTA_DOWNLOADS = "./data/fat/raw"

def conectar_ftp_datasus():
    """Conecta ao servidor FTP oficial do DATASUS"""
    try:
        ftp = FTP("ftp.datasus.gov.br")
        ftp.login() 
        ftp.cwd("/dissemin/publicos/SIASUS/200801_/Dados/")
        return ftp
    except Exception as e:
        print(f"❌ Erro ao conectar ao FTP: {e}")
        sys.exit(1)

def baixar_producao_nacional():
    print("🌍 Iniciando Pipeline de Extração Nacional (SIA/SUS)...")
    
    if not os.path.exists(PASTA_DOWNLOADS):
        os.makedirs(PASTA_DOWNLOADS)
        
    ftp = conectar_ftp_datasus()
    print("2. Mapeando arquivos globais do servidor...")
    todos_arquivos = ftp.nlst()
    
    # Loop que vai passar de estado em estado baixando os dados
    for estado in ESTADOS_BRASIL:
        print(f"\n──────────────────────────────────────────")
        print(f"📂 Processando Estado: {estado}")
        print(f"──────────────────────────────────────────")
        
        # Filtra os arquivos do estado atual para os anos escolhidos
        # Padrão: PA + UF + ANO + MES .dbc (Ex: PASP2401.dbc)
        arquivos_estado = [
            nome for nome in todos_arquivos 
            if nome.startswith(f"PA{estado}") and any(ano in nome[4:6] for ano in ANOS_FOCO)
        ]
        
        print(f"📌 Encontrados {len(arquivos_estado)} arquivos para {estado}.")
        
        for nome_arquivo in sorted(arquivos_estado):
            caminho_local = os.path.join(PASTA_DOWNLOADS, nome_arquivo)
            
            if not os.path.exists(caminho_local):
                print(f"📥 Baixando: {nome_arquivo}...")
                try:
                    with open(caminho_local, "wb") as arquivo_local:
                        ftp.retrbinary(f"RETR {nome_arquivo}", arquivo_local.write)
                except Exception as e:
                    print(f"⚠️ Falha ao baixar {nome_arquivo}: {e}. Tentando reestabelecer conexão...")
                    # Se o FTP derrubar a conexão por tempo (timeout), o script se reconecta sozinho
                    ftp = conectar_ftp_datasus()
            else:
                print(f"⏩ Arquivo já existe localmente: {nome_arquivo}")
                
    ftp.quit()
    print(f"\n✅ VITÓRIA! Todos os estados do Brasil foram baixados na pasta: {PASTA_DOWNLOADS}")

if __name__ == "__main__":
    baixar_producao_nacional()
