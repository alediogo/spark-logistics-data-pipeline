import os
import urllib.request
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, explode, current_timestamp

# --- CONFIGURAÇÕES ---
URL_FONTE = "https://raw.githubusercontent.com/andre-marcos-perez/ebac-course-utils/main/dataset/deliveries.json"
ARQUIVO_ENTRADA = "data/deliveries.json"
PASTA_SAIDA = "output/loggi_processed"

def get_spark_session():
    """Inicia a sessão do Spark."""
    return SparkSession.builder \
        .appName("LoggiLogisticsETL") \
        .master("local[*]") \
        .getOrCreate()

def baixar_dados():
    """Baixa o arquivo JSON da fonte se ele não existir."""
    if not os.path.exists("data"):
        os.makedirs("data")
    
    if not os.path.exists(ARQUIVO_ENTRADA):
        print(f"📥 Baixando dados de: {URL_FONTE}...")
        urllib.request.urlretrieve(URL_FONTE, ARQUIVO_ENTRADA)
        print("✅ Download concluído.")
    else:
        print("📂 Arquivo já existe localmente.")

def processar_dados():
    spark = get_spark_session()
    
    print("📖 Lendo arquivo JSON...")
    df_raw = spark.read.json(ARQUIVO_ENTRADA)
    
    print("⚙️  Transformando dados (Explode & Flatten)...")
    # O comando explode transforma 1 linha (hub) em várias linhas (entregas)
    df_exploded = df_raw.withColumn("delivery_data", explode(col("deliveries")))

    # Selecionando e renomeando para uma tabela plana
    df_final = df_exploded.select(
        col("name").alias("hub_name"),
        col("region").alias("hub_region"),
        col("origin.lat").alias("hub_latitude"),
        col("origin.lng").alias("hub_longitude"),
        col("vehicle_capacity"),
        col("delivery_data.id").alias("delivery_id"),
        col("delivery_data.size").alias("delivery_size"),
        col("delivery_data.point.lat").alias("delivery_lat"),
        col("delivery_data.point.lng").alias("delivery_lng"),
        current_timestamp().alias("data_processamento")
    )

    print(f"💾 Salvando resultado em Parquet na pasta: {PASTA_SAIDA}")
    df_final.write.mode("overwrite").parquet(PASTA_SAIDA)
    
    print("🚀 Pipeline finalizado com sucesso!")
    df_final.show(5)

if __name__ == "__main__":
    baixar_dados()
    processar_dados()