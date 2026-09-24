import os
import glob
import pandas as pd
from dbfread import DBF

PASTA_BRUTOS = "./data/fat/raw"
PASTA_FINAL_CSV = "./data/fat/processed"

def converter_dbc_para_csv_lote():
    print("⏳ Iniciando a Fábrica de Conversão (DBC/DBF para CSV)...")
    
    # Cria a pasta de destino dos CSVs se ela não existir
    if not os.path.exists(PASTA_FINAL_CSV):
        os.makedirs(PASTA_FINAL_CSV)
        
    # Mapeia todos os arquivos baixados na pasta de brutos
    arquivos_dbc = glob.glob(os.path.join(PASTA_BRUTOS, "*.dbc")) + glob.glob(os.path.join(PASTA_BRUTOS, "*.dbf"))
    
    if not arquivos_dbc:
        print("❌ Nenhum arquivo encontrado para conversão. Aguarde os downloads terminarem!")
        return
        
    print(f"📌 Encontrados {len(arquivos_dbc)} arquivos para processar.")
    
    # LINHA CORRIGIDA: Varre diretamente a lista mapeada de arquivos
    for caminho_arquivo in sorted(arquivos_dbc):
        nome_arquivo = os.path.basename(caminho_arquivo)
        nome_sem_extensao = os.path.splitext(nome_arquivo)[0]
        caminho_csv_destino = os.path.join(PASTA_FINAL_CSV, f"{nome_sem_extensao}.csv")
        
        # Regra de Engenharia: Evita reprocessar arquivos que já foram convertidos
        if not os.path.exists(caminho_csv_destino):
            print(f"🔄 Convertendo estrutura: {nome_arquivo} ➔ {nome_sem_extensao}.csv")
            try:
                # O dbfread lê o arquivo de forma direta e o pandas transforma em dataframe
                tabela = DBF(caminho_arquivo, encoding='iso-8859-1', ignore_missing_memofile=True)
                df = pd.DataFrame(iter(tabela))
                df.to_csv(caminho_csv_destino, index=False, sep=";")
                print(f"✅ Convertido com sucesso!")
            except Exception as e:
                print(f"⚠️ Erro ao converter {nome_arquivo}: {e}. Pulando para o próximo.")
        else:
            print(f"⏩ CSV já integrado e pronto: {nome_sem_extensao}.csv")
            
    print(f"\n🚀 Sucesso! Todos os arquivos disponíveis foram convertidos em: {PASTA_FINAL_CSV}")

if __name__ == "__main__":
    converter_dbc_para_csv_lote()
