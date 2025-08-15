import os
import time

folder_path = 'C:/Users/OGGO/Desktop/Ultimo Semestre/Fase1Act1/CS13309_Archivos_HTML/Files'

def list_html_files(folder_path):
    results = []
    try:
        files = os.listdir(folder_path)
        html_files = [f for f in files if f.endswith('.html')]

        for file in html_files:
            path = os.path.join(folder_path, file)

            start = time.time()
            with open(path, 'r', encoding="latin-1") as f:
                content = f.read()
            end = time.time()

            duration = end - start

            results.append((file, duration))

        return results
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return []
    
starting_total_time = time.time()
results = list_html_files(folder_path)
ending_total_time = time.time()

total_time = ending_total_time - starting_total_time

with open("a1_03038135.txt", "w", encoding="utf-8") as archivo:
    for file, duration in results:
        archivo.write(f"{file}            {duration:.4f} \n")

    archivo.write(f"tiempo total en abrir los archivos: {sum(d for _, d in list_html_files(folder_path)):.4f} segundos\n")
    archivo.write(f"tiempo total de ejecucion {total_time:.4f} segundos\n")
    