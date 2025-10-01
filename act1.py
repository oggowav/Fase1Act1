import os
import time
import re
from collections import Counter, defaultdict

project_folder = 'C:/Users/OGGO/Desktop/Ultimo Semestre/Fase1Act1'
folder_path = 'C:/Users/OGGO/Desktop/Ultimo Semestre/Fase1Act1/CS13309_Archivos_HTML/Files'
output_folder = 'C:/Users/OGGO/Desktop/Ultimo Semestre/Fase1Act1/CS13309_Archivos_TEXT'

os.makedirs(output_folder, exist_ok=True)


def extract_words(text):
    words = re.findall(r"[A-Za-zÁÉÍÓÚÜÑáéíóúüñ0-9\-]+", text)
    return words

def process_words(cleaned_text, output_file):
    start_processing = time.time()

    words = extract_words(cleaned_text)
    words = [w.lower() for w in words]
    counter = Counter(words)
    sorted_words = sorted(counter.items())

    with open(output_file, "w", encoding="utf-8") as f:
        for word, count in sorted_words:
            f.write(f"{word} se repite: {count} veces.\n")

    end_processing = time.time()
    processing_time = end_processing - start_processing
    return processing_time

def list_html_files(folder_path, output_folder):
    reading_results = []
    cleanning_results = []
    words_results = []

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

            words_file = os.path.join(output_folder, file.replace(".html", "_alphabetic_order_words.txt"))
            words_duration = process_words(cleaned_text, words_file)

            reading_results.append((file, reading_duration))
            cleanning_results.append((file, cleanning_duration))
            words_results.append((file, words_duration))

        return reading_results, cleanning_results, words_results
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return [], [], []
    
starting_total_time = time.time()
reading_results, cleanning_results, words_results = list_html_files(folder_path, output_folder)
ending_total_time = time.time()
total_time = ending_total_time - starting_total_time

def create_consolidated_words_file(output_folder, project_folder):
    file_durations = []
    all_words = []

    txt_files = [f for f in os.listdir(output_folder) if f.endswith('.txt') and not f.endswith('_alphabetic_order_words.txt')]
    for file in txt_files:
        start_file = time.time()
        path = os.path.join(output_folder, file)
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()
            words = extract_words(text)
            all_words.extend([w.lower() for w in words])
        end_file = time.time()
        duration = end_file - start_file
        file_durations.append((file, duration))

    start_sort = time.time()
    all_words_sorted = sorted(all_words)
    end_sort = time.time()
    sort_duration = end_sort - start_sort

    consolidated_file = os.path.join(project_folder, "consolidado_palabras.txt")
    with open(consolidated_file, "w", encoding="utf-8") as f:
        for word in all_words_sorted:
            f.write(f"{word}\n")

    total_consolidated_duration = sum(d for _, d in file_durations) + sort_duration
    return file_durations, sort_duration, total_consolidated_duration

starting_total_time = time.time()
reading_results, cleanning_results, words_results = list_html_files(folder_path, output_folder)

consolidated_duration = create_consolidated_words_file(output_folder, project_folder)

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

with open(os.path.join(project_folder, "a3_03038135.txt"), "w", encoding="utf-8") as archivo:
    for file, duration in words_results:
        archivo.write(f"{file}            {duration:.4f} \n")

    archivo.write(f"tiempo total en eliminar las etiquetas HTML: {sum(d for _, d in words_results):.4f} segundos\n")
    archivo.write(f"tiempo total de ejecucion {total_time:.4f} segundos\n")

file_durations, sort_duration, consolidated_duration = create_consolidated_words_file(output_folder, project_folder)

with open(os.path.join(project_folder, "a4_03038135.txt"), "w", encoding="utf-8") as archivo:
    for file, duration in file_durations:
        archivo.write(f"{file}            {duration:.4f} \n")

    archivo.write(f"tiempo total en crear el nuevo archivo: {consolidated_duration:.4f} segundos\n")
    archivo.write(f"tiempo total de ejecucion: {total_time:.4f} segundos\n")

def create_specific_consolidated_file(folder_path, project_folder):
    files_to_process = ['simple.html', 'medium.html', 'hard.html', '049.html']
    all_words = []
    file_durations = []

    start_total = time.time()

    for filename in files_to_process:
        path = os.path.join(folder_path, filename)

        start_file = time.time()
        with open(path, "r", encoding="latin-1") as f:
            text = f.read()
            cleaned_text = re.sub(r'<.*?>', '', text)
            words = extract_words(cleaned_text)
            all_words.extend([w.lower() for w in words])
        end_file = time.time()
        file_durations.append((filename, end_file - start_file))

    counter = Counter(all_words)

    start_sort = time.time()
    all_words_sorted = sorted(counter.items())
    end_sort = time.time()
    sort_duration = end_sort - start_sort
    
    end_total = time.time()
    total_time = end_total - start_total

    output_file = os.path.join(project_folder, "a5_03038135.txt")
    with open(output_file, "w", encoding="utf-8") as archivo:
        for word, count in all_words_sorted:
            archivo.write(f"{word} {count}\n")

        archivo.write(f"Tiempo total en crear el nuevo archivo: {sort_duration:.4f} segundos\n")
        archivo.write(f"Tiempo total de ejecucion: {total_time:.4f} segundos\n")

    return file_durations, sort_duration, total_time

file_durations, sort_duration, total_time_a5 = create_specific_consolidated_file(folder_path, project_folder)

def create_dictionary_with_file_count(folder_path, project_folder):
    files_to_process = [f for f in os.listdir(folder_path) if f.endswith(".html")]
    token_counter = Counter()
    token_files = defaultdict(set)
    file_durations = []

    start_total = time.time()

    for filename in files_to_process:
        path = os.path.join(folder_path, filename)

        start_file = time.time()
        with open(path, "r", encoding="latin-1") as f:
            text = f.read()
            cleaned_text = re.sub(r'<.*?>', '', text)
            words = extract_words(cleaned_text)

            for w in words:
                word = w.lower()
                token_counter[word] += 1
                token_files[word].add(filename)
        end_file = time.time()
        file_durations.append((filename, end_file - start_file))

    end_total = time.time()
    total_time = end_total - start_total

    output_file = os.path.join(project_folder, "a6_dictionary.txt")
    with open(output_file, "w", encoding="utf-8") as archivo:
        for token, count in token_counter.items():
            archivo.write(f"{token};{count};{len(token_files[token])}\n")

    log_file = os.path.join(project_folder, "a6_03038135.txt")
    with open(log_file, "w", encoding="utf-8") as log:
        for filename, duration in file_durations:
            log.write(f"{filename}            {duration:.4f} \n")
        log.write(f"Tiempo total de ejecucion: {total_time:.4f} segundos\n")        

    return file_durations, total_time


file_durations_a6, total_time_a6 = create_dictionary_with_file_count(folder_path, project_folder)