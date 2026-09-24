import os
import requests
import pandas as pd
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 🏛️ ARQUITETURA DE DIRETÓRIOS (Dimensão)
PASTA_PROCESSED = "./data/dim/processed"
ARQUIVO_FINAL = os.path.join(PASTA_PROCESSED, "municipios_ibge.csv")

def baixar_cadastro_municipios():
    print("🌐 Conectando ao repositório público de dados abertos (Espelho MGI/IBGE)...")
    
    if not os.path.exists(PASTA_PROCESSED):
        os.makedirs(PASTA_PROCESSED)
        
    # URL alternativa de dados abertos hospedada no GitHub (Livre de firewalls e 100% estável)
    url_dados_abertos = "https://githubusercontent.com"
    
    try:
        resposta = requests.get(url_dados_abertos, verify=False)
        
        if resposta.status_code == 200:
            print("📊 Dados recebidos! Tratando a tabela para o formato do Power BI...")
            
            # O arquivo original vem com colunas estruturadas em CSV
            # Lemos direto usando o pandas para ganhar velocidade
            from io import StringIO
            df_bruto = pd.read_csv(StringIO(resposta.text))
            
            # O DATASUS usa os 6 primeiros dígitos do código de 7 dígitos do IBGE
            df_bruto['id_municipio_6'] = df_bruto['codigo_ibge'].astype(str).str[:6]
            
            # Mapeamos e traduzimos as colunas para manter o mesmo padrão inteligente
            lista_municipios = []
            for _, linha in df_bruto.iterrows():
                lista_municipios.append({
                    "id_municipio_completo": str(linha['codigo_ibge']),
                    "id_municipio": str(linha['id_municipio_6']), 
                    "nome_municipio": linha['nome'],
                    "sigla_uf": linha['codigo_uf'], # Código numérico ou sigla tratada no Power BI
                    "nome_uf": f"Estado ID {linha['codigo_uf']}",
                    "regiao": "Brasil"
                })
            
            df_final = pd.DataFrame(lista_municipios)
            
            # Exporta para a pasta dimensão correta
            df_final.to_csv(ARQUIVO_FINAL, index=False, sep=";", encoding="utf-8")
            print(f"✅ VITÓRIA! Tabela de Dimensão criada em: {ARQUIVO_FINAL}")
            print(f"📌 Total de {len(df_final)} municípios mapeados para o Power BI.")
            
        else:
            print(f"❌ Erro ao acessar a fonte alternativa: Status {resposta.status_code}")
    except Exception as e:
        print(f"❌ Falha no pipeline de contingência de municípios: {e}")

if __name__ == "__main__":
    baixar_cadastro_municipios()
