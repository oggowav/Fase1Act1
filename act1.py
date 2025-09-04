import os
import time
import re

project_folder = 'C:/Users/OGGO/Desktop/Ultimo Semestre/Fase1Act1'
folder_path = 'C:/Users/OGGO/Desktop/Ultimo Semestre/Fase1Act1/CS13309_Archivos_HTML/Files'
output_folder = 'C:/Users/OGGO/Desktop/Ultimo Semestre/Fase1Act1/CS13309_Archivos_TEXT'

os.makedirs(output_folder, exist_ok=True)

def list_html_files(folder_path, output_folder):
    reading_results = []
    cleanning_results = []

    try:
        files = os.listdir(folder_path)
        html_files = [f for f in files if f.endswith('.html')]

        for file in html_files:
            path = os.path.join(folder_path, file)

            start_reading = time.time()
            with open(path, 'r', encoding="latin-1") as f:
                content = f.read()
            end_reading = time.time()
            reading_duration = end_reading - start_reading

            start_cleanning = time.time()
            cleaned_text = re.sub(r'<.*?>', '', content)
            output_file = os.path.join(output_folder, file.replace(".html", ".txt"))
            with open(output_file, "w", encoding="utf-8") as out:
                out.write(cleaned_text)
            end_cleanning = time.time()
            cleanning_duration = end_cleanning - start_cleanning

            reading_results.append((file, reading_duration))
            cleanning_results.append((file, cleanning_duration))

        return reading_results, cleanning_results
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return [], []
    
starting_total_time = time.time()
reading_results, cleanning_results = list_html_files(folder_path, output_folder)
ending_total_time = time.time()
total_time = ending_total_time - starting_total_time

with open(os.path.join(project_folder, "a1_03038135.txt"), "w", encoding="utf-8") as archivo:
    for file, duration in reading_results:
        archivo.write(f"{file}            {duration:.4f} \n")

    archivo.write(f"tiempo total en abrir los archivos: {sum(d for _, d in reading_results):.4f} segundos\n")
    archivo.write(f"tiempo total de ejecucion {total_time:.4f} segundos\n")
    
with open(os.path.join(project_folder, "a2_03038135.txt"), "w", encoding="utf-8") as archivo:
    for file, duration in cleanning_results:
        archivo.write(f"{file}            {duration:.4f} \n")

    archivo.write(f"tiempo total en eliminar las etiquetas HTML: {sum(d for _, d in cleanning_results):.4f} segundos\n")
    archivo.write(f"tiempo total de ejecucion {total_time:.4f} segundos\n")