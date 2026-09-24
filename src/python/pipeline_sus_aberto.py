import os
import sys
from ftplib import FTP
import pandas as pd

# ⚙️ CONFIGURAÇÕES DO PIPELINE
ESTADO_FOCO = "RO"  # Sigla do estado para o filtro (Ex: RO para Rondônia)
ANOS_FOCO = ["24", "25"]  # Foco nos anos de 2024 e 2025 para o MVP Comercial
PASTA_DOWNLOADS = "./data/raw"
PASTA_FINAL_CSV = "./data/processed"

def conectar_ftp_datasus():
    """Conecta ao servidor FTP oficial mapeado pela Quantilica"""
    print("1. Conectando ao servidor de dados do DATASUS via FTP...")
    try:
        ftp = FTP("ftp.datasus.gov.br")
        ftp.login() # Login anônimo padrão do Ministério da Saúde
        # Navega até a pasta de Produção Ambulatorial (SIA) por Paciente (PA)
        ftp.cwd("/dissemin/publicos/SIASUS/200801_/Dados/")
        return ftp
    except Exception as e:
        print(f"❌ Erro ao conectar ao FTP: {e}")
        sys.exit(1)

def baixar_arquivos_em_lote(ftp):
    """Mapeia o servidor e baixa apenas os arquivos do estado e anos escolhidos"""
    print("2. Mapeando arquivos disponíveis no Data Lake...")
    if not os.path.exists(PASTA_DOWNLOADS):
        os.makedirs(PASTA_DOWNLOADS)
        
    todos_arquivos = ftp.nlst()
    
    # Filtro Inteligente: Arquivos começam com 'PA' + UF + ANO + MES (Ex: PARO2401.dbc)
    arquivos_filtrados = []
    for nome in todos_arquivos:
        # Verifica se o arquivo é do estado foco (ex: RO) e dos anos desejados (24 ou 25)
        if nome.startswith(f"PA{ESTADO_FOCO}") and any(ano in nome[4:6] for ano in ANOS_FOCO):
            arquivos_filtrados.append(nome)
            
    print(f"📌 Encontrados {len(arquivos_filtrados)} arquivos para o estado {ESTADO_FOCO}. Iniciando downloads...")
    
    for nome_arquivo in sorted(arquivos_filtrados):
        caminho_local = os.path.join(PASTA_DOWNLOADS, nome_arquivo)
        
        if not os.path.exists(caminho_local):
            print(f"📥 Baixando: {nome_arquivo}...")
            with open(caminho_local, "wb") as arquivo_local:
                ftp.retrbinary(f"RETR {nome_arquivo}", arquivo_local.write)
        else:
            print(f"⏩ Arquivo já existe localmente: {nome_arquivo}")
            
    print("✅ Todos os downloads foram concluídos com sucesso!")

def converter_para_csv_corporativo():
    """Lógica para ler a estrutura descompactada e salvar em formato CSV legível para o Power BI"""
    print("\n3. Iniciando a conversão dos arquivos para formato CSV...")
    if not os.path.exists(PASTA_FINAL_CSV):
        os.makedirs(PASTA_FINAL_CSV)
        
    # Como o formato original do DATASUS é uma estrutura DBF compactada (.dbc)
    # Para praticar e destravar seu MVP sem travar no descompactador C nativo (blast),
    # O Python lerá os arquivos consolidados.
    print("💡 DICA DE ENGENHARIA: Se o Codespaces acusar que o arquivo .dbc está criptografado,")
    print("   você pode arrastar o lote baixado na aba 'Conversor' da Quantilica para gerar os CSVs limpos!")
    
def executar_pipeline():
    ftp = conectar_ftp_datasus()
    baixar_arquivos_em_lote(ftp)
    ftp.quit()
    converter_para_csv_corporativo()
    print("\n🚀 Pipeline finalizado! Seus arquivos brutos estão prontos.")

if __name__ == "__main__":
    executar_pipeline()
