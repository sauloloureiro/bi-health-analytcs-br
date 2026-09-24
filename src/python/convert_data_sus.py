import os
import glob
from simpledbf import SimpleDbf

PASTA_BRUTOS = "./data/raw"
PASTA_FINAL_CSV = "./data/processed"

def converter_dbc_para_csv_lote():
    print("⏳ Iniciando a Fábrica de Conversão (DBC para CSV)...")
    
    # Cria a pasta de destino dos CSVs se ela não existir
    if not os.path.exists(PASTA_FINAL_CSV):
        os.makedirs(PASTA_FINAL_CSV)
        
    # Mapeia todos os arquivos .dbc baixados na pasta de brutos
    arquivos_dbc = glob.glob(os.path.join(PASTA_BRUTOS, "*.dbc"))
    
    if not arquivos_dbc:
        print("❌ Nenhum arquivo .dbc encontrado para conversão. Aguarde os downloads terminarem!")
        return
        
    print(f"📌 Encontrados {len(arquivos_dbc)} arquivos para processar.")
    
    for caminho_arquivo in sorted(arquivos_dbc):
        nome_arquivo = os.path.basename(caminho_arquivo)
        nome_sem_extensao = os.path.splitext(nome_arquivo)[0]
        caminho_csv_destino = os.path.join(PASTA_FINAL_CSV, f"{nome_sem_extensao}.csv")
        
        # Regra de Engenharia: Evita reprocessar arquivos que já foram convertidos
        if not os.path.exists(caminho_csv_destino):
            print(f"🔄 Convertendo estrutura: {nome_arquivo} ➔ {nome_sem_extensao}.csv")
            try:
                # O SimpleDbf lê a tabela interna do arquivo do SUS e exporta em CSV corporativo
                dbf = SimpleDbf(caminho_arquivo, codec='iso-8859-1')
                dbf.to_csv(caminho_csv_destino)
            except Exception as e:
                print(f"⚠️ Erro ao converter {nome_arquivo}: {e}. Pulando para o próximo.")
        else:
            print(f"⏩ CSV já integrado e pronto: {nome_sem_extensao}.csv")
            
    print(f"\n🚀 Sucesso! Todos os arquivos disponíveis foram convertidos em: {PASTA_FINAL_CSV}")

if __name__ == "__main__":
    converter_dbc_para_csv_lote()
