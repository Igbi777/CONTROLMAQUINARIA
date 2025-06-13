import pandas as pd

def extraer_columnas_excel(ruta_archivo, columnas_deseadas):
    """
    Lee un archivo de Excel y devuelve solo las columnas especificadas.

    Parámetros:
    ruta_archivo (str): Ruta al archivo de Excel (.xlsx o .xls).
    columnas_deseadas (list): Lista con los nombres de las columnas que deseas obtener.

    Retorna:
    DataFrame con solo las columnas especificadas.
    """
    try:
        df = pd.read_excel(ruta_archivo)
        columnas_encontradas = [col for col in columnas_deseadas if col in df.columns]
        return df[columnas_encontradas]
    except Exception as e:
        print(f"Error al leer el archivo: {e}")
        return None