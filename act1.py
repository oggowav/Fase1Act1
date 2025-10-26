import os
import time
import re
from collections import Counter, defaultdict

# --- Configuraciones ---
project_folder = 'C:/Users/OGGO/Desktop/Ultimo Semestre/Fase1Act1'
folder_path = 'C:/Users/OGGO/Desktop/Ultimo Semestre/Fase1Act1/CS13309_Archivos_HTML/Files'
output_folder = 'C:/Users/OGGO/Desktop/Ultimo Semestre/Fase1Act1/CS13309_Archivos_TEXT'

os.makedirs(output_folder, exist_ok=True)

# Parámetros para la Hash Table (Actividad A8)
HASH_TABLE_SIZE = 20000 
EMPTY_SLOT_INDICATOR = "vacio"
EMPTY_POSTING_POSITION = -1


# --- Funciones Auxiliares ---

def extract_words(text):
    words = re.findall(r"[A-Za-zÁÉÍÓÚÜÑáéíóúüñ0-9\-]+", text)
    return words

def hash_function(key, size):
    """Implementa una versión simple de la función hash DJB2."""
    hash_value = 5381
    for char in key:
        hash_value = ((hash_value << 5) + hash_value) + ord(char) # hash * 33 + char
    return hash_value % size

# --- Funciones de Procesamiento Originales (A1 a A4) ---

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

            # A1: Lectura
            start_reading = time.time()
            with open(path, 'r', encoding="latin-1") as f:
                content = f.read()
            end_reading = time.time()
            reading_duration = end_reading - start_reading

            # A2: Limpieza (Eliminar HTML)
            start_cleanning = time.time()
            cleaned_text = re.sub(r'<.*?>', '', content)
            
            output_file = os.path.join(output_folder, file.replace(".html", ".txt"))
            with open(output_file, "w", encoding="utf-8") as out:
                out.write(cleaned_text)
            end_cleanning = time.time()
            cleanning_duration = end_cleanning - start_cleanning

            # A3: Conteo de Palabras y Archivo de Palabras Ordenadas
            words_file = os.path.join(output_folder, file.replace(".html", "_alphabetic_order_words.txt"))
            words_duration = process_words(cleaned_text, words_file)

            reading_results.append((file, reading_duration))
            cleanning_results.append((file, cleanning_duration))
            words_results.append((file, words_duration))

        return reading_results, cleanning_results, words_results
    
    except Exception as e:
        print(f"Ocurrió un error en list_html_files: {e}")
        return [], [], []


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

# --- Funciones de Procesamiento Originales (A5 a A7) ---

def create_specific_consolidated_file(folder_path, project_folder):
    files_to_process = ['simple.html', 'medium.html', 'hard.html', '049.html']
    all_words = []
    file_durations = []

    start_total = time.time()

    for filename in files_to_process:
        path = os.path.join(folder_path, filename)

        start_file = time.time()
        try:
            with open(path, "r", encoding="latin-1") as f:
                text = f.read()
                cleaned_text = re.sub(r'<.*?>', '', text)
                words = extract_words(cleaned_text)
                all_words.extend([w.lower() for w in words])
        except Exception as e:
            print(f"Error en A5 al procesar {filename}: {e}")
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

        archivo.write(f"Tiempo total de procesamiento de palabras y conteo (sin incluir archivos individuales): {sort_duration:.4f} segundos\n")
        archivo.write(f"Tiempo total de ejecucion: {total_time:.4f} segundos\n")

    return file_durations, sort_duration, total_time

def create_dictionary_with_file_count(folder_path, project_folder):
    files_to_process = [f for f in os.listdir(folder_path) if f.endswith(".html")]
    token_counter = Counter()
    token_files = defaultdict(set)
    file_durations = []

    start_total = time.time()

    for filename in files_to_process:
        path = os.path.join(folder_path, filename)

        start_file = time.time()
        try:
            with open(path, "r", encoding="latin-1") as f:
                text = f.read()
                cleaned_text = re.sub(r'<.*?>', '', text)
                words = extract_words(cleaned_text)

                for w in words:
                    word = w.lower()
                    token_counter[word] += 1
                    token_files[word].add(filename)
        except Exception as e:
            print(f"Error en A6 al procesar {filename}: {e}")
            
        end_file = time.time()
        file_durations.append((filename, end_file - start_file))

    end_total = time.time()
    total_time = end_total - start_total

    # Archivo de Diccionario (A6_dictionary.txt)
    output_file = os.path.join(project_folder, "a6_dictionary.txt")
    with open(output_file, "w", encoding="utf-8") as archivo:
        for token, count in sorted(token_counter.items()):
            archivo.write(f"{token};{count};{len(token_files[token])}\n")

    # Archivo de Log (A6_03038135.txt)
    log_file = os.path.join(project_folder, "a6_03038135.txt")
    with open(log_file, "w", encoding="utf-8") as log:
        for filename, duration in file_durations:
            log.write(f"{filename}            {duration:.4f} \n")
        log.write(f"Tiempo total de ejecucion: {total_time:.4f} segundos\n")        

    return file_durations, total_time

def create_copy_log(folder_path, project_folder):
    files_to_process = [f for f in os.listdir(folder_path) if f.endswith(".html")]
    file_durations = []

    start_total = time.time()

    for filename in sorted(files_to_process):
        path = os.path.join(folder_path, filename)

        start_file = time.time()
        try:
            with open(path, "r", encoding="latin-1") as f:
                text = f.read()
        except Exception as e:
            print(f"Error en A7 al procesar {filename}: {e}")
            
        end_file = time.time()
        file_durations.append((filename, end_file - start_file))

    end_total = time.time()
    total_time = end_total - start_total

    log_file = os.path.join(project_folder, "a7_03038135.txt")
    with open(log_file, "w", encoding="utf-8") as log:
        for filename, duration in file_durations:
            log.write(f"{filename}            {duration:.4f}\n")
        log.write(f"Tiempo total de ejecucion: {total_time:.4f} segundos\n")

    return file_durations, total_time

# --- Función de Procesamiento A8: Hash Table Implementada (NUEVA) ---

# --- Función de Procesamiento A8: Hash Table Implementada (Corregida) ---

def create_hash_table_dictionary(folder_path, project_folder, matricula="03038135"):
    files_to_process = [f for f in os.listdir(folder_path) if f.endswith(".html")]
    
    # Inicialización de la Hash Table con encadenamiento
    hash_table = [[] for _ in range(HASH_TABLE_SIZE)]
    
    token_freq = Counter()
    token_files = defaultdict(set)
    
    file_durations = []
    total_collisions = 0
    
    start_total = time.time()

    # --- Fase 1: Extracción de Tokens y Recolección de Datos ---
    for filename in files_to_process:
        path = os.path.join(folder_path, filename)
        start_file = time.time()
        
        try:
            with open(path, "r", encoding="latin-1") as f:
                text = f.read()
                cleaned_text = re.sub(r'<.*?>', '', text)
                words = extract_words(cleaned_text)

                for w in words:
                    word = w.lower()
                    token_freq[word] += 1
                    token_files[word].add(filename)
        except Exception as e:
            print(f"Error en A8 al procesar {filename}: {e}")
            
        end_file = time.time()
        file_durations.append((filename, end_file - start_file))
    
    end_data_collection = time.time()
    data_collection_time = end_data_collection - start_total
    
    # --- Fase 2: Construcción de la Hash Table ---
    start_hash_build = time.time()
    sorted_tokens = sorted(token_freq.keys())
    
    for token in sorted_tokens:
        freq = token_freq[token]
        num_files = len(token_files[token])
        
        index = hash_function(token, HASH_TABLE_SIZE)
        
        # Conteo de colisiones
        if hash_table[index]:
            total_collisions += 1
        
        # Almacenamiento con encadenamiento
        hash_table[index].append((token, freq, num_files, index))
        
    end_hash_build = time.time()
    hash_build_time = end_hash_build - start_hash_build
    
    end_total = time.time()
    total_time = end_total - start_total

    # --- Fase 3: Escribir el Diccionario (a8_dictionary.txt) ---
    output_file = os.path.join(project_folder, f"a8_dictionary.txt")
    
    with open(output_file, "w", encoding="utf-8") as archivo:
        # Escribir la tabla hash, incluyendo los slots vacíos
        for i, slot in enumerate(hash_table):
            if not slot:
                # Slot vacío
                archivo.write(f"Posición Hash: {i}, Token: {EMPTY_SLOT_INDICATOR}, Frecuencia: 0, Archivos: 0, Posición Posting: {EMPTY_POSTING_POSITION}\n")
            else:
                # Slot con elementos (posibles colisiones)
                for token, freq, num_files, _ in slot:
                    archivo.write(f"Posición Hash: {i}, Token: {token}, Frecuencia: {freq}, Archivos: {num_files}, Posición Posting: {i}\n")
                    
    # --- Fase 4: Escribir el Log (a8_matricula.txt) ---
    log_file = os.path.join(project_folder, f"a8_{matricula}.txt")
    with open(log_file, "w", encoding="utf-8") as log:
        log.write(f"--- Metadatos de la Hash Table ---\n")
        log.write(f"Tamaño de la Hash Table (m): {HASH_TABLE_SIZE}\n")
        log.write(f"Número de Tokens Únicos (n): {len(token_freq)}\n")
        log.write(f"Número de Colisiones (Chainings): {total_collisions}\n")
        if HASH_TABLE_SIZE > 0:
             log.write(f"Factor de Carga (n/m): {len(token_freq) / HASH_TABLE_SIZE:.4f}\n")
        else:
             log.write(f"Factor de Carga (n/m): N/A (Tamaño de tabla es 0)\n")
        log.write(f"\n--- Tiempos por Archivo (Extracción/Recolección) ---\n")
        for filename, duration in file_durations:
            log.write(f"{filename}           {duration:.4f} \n")
        
        log.write(f"\n--- Tiempos Totales ---\n")
        log.write(f"Tiempo Total de Recolección de Datos: {data_collection_time:.4f} segundos\n")
        log.write(f"Tiempo Total de Construcción de Hash: {hash_build_time:.4f} segundos\n")
        log.write(f"Tiempo Total de Ejecución del Proceso A8: {total_time:.4f} segundos\n") 

    return file_durations, total_time, total_collisions, HASH_TABLE_SIZE

# --- Bloque de Ejecución Principal Consolidado ---
# Este bloque sustituye las llamadas y escrituras de archivos que tenías dispersas en el código.

if __name__ == "__main__":
    
    starting_total_time = time.time()
    
    # 1. Ejecutar A1, A2, A3 (Lectura, Limpieza, Conteo/Archivo individual)
    reading_results, cleanning_results, words_results = list_html_files(folder_path, output_folder)
    
    # 2. Ejecutar A4 (Consolidado de palabras de A2)
    file_durations_a4, sort_duration_a4, consolidated_duration_a4 = create_consolidated_words_file(output_folder, project_folder)
    
    # 3. Ejecutar A5 (Consolidado de archivos específicos)
    file_durations_a5, sort_duration_a5, total_time_a5 = create_specific_consolidated_file(folder_path, project_folder)

    # 4. Ejecutar A6 (Diccionario usando Python dict/Counter)
    file_durations_a6, total_time_a6 = create_dictionary_with_file_count(folder_path, project_folder)

    # 5. Ejecutar A7 (Copia/Lectura simple de HTML)
    file_durations_a7, total_time_a7 = create_copy_log(folder_path, project_folder)

    # 6. Ejecutar A8 (Diccionario usando Hash Table Implementada)
    file_durations_a8, total_time_a8, total_collisions_a8, hash_size_a8 = create_hash_table_dictionary(folder_path, project_folder)
    
    ending_total_time = time.time()
    total_execution_time = ending_total_time - starting_total_time

    # --- Generación de Archivos de Log A1 a A4 (Usando el tiempo total correcto) ---

    # Log A1
    with open(os.path.join(project_folder, "a1_03038135.txt"), "w", encoding="utf-8") as archivo:
        for file, duration in reading_results:
            archivo.write(f"{file}            {duration:.4f} \n")
        archivo.write(f"tiempo total en abrir los archivos: {sum(d for _, d in reading_results):.4f} segundos\n")
        archivo.write(f"tiempo total de ejecucion {total_execution_time:.4f} segundos\n")
        
    # Log A2
    with open(os.path.join(project_folder, "a2_03038135.txt"), "w", encoding="utf-8") as archivo:
        for file, duration in cleanning_results:
            archivo.write(f"{file}            {duration:.4f} \n")
        archivo.write(f"tiempo total en eliminar las etiquetas HTML: {sum(d for _, d in cleanning_results):.4f} segundos\n")
        archivo.write(f"tiempo total de ejecucion {total_execution_time:.4f} segundos\n")

    # Log A3
    with open(os.path.join(project_folder, "a3_03038135.txt"), "w", encoding="utf-8") as archivo:
        for file, duration in words_results:
            archivo.write(f"{file}            {duration:.4f} \n")
        archivo.write(f"tiempo total en conteo de palabras y escritura de archivo: {sum(d for _, d in words_results):.4f} segundos\n")
        archivo.write(f"tiempo total de ejecucion {total_execution_time:.4f} segundos\n")

    # Log A4
    with open(os.path.join(project_folder, "a4_03038135.txt"), "w", encoding="utf-8") as archivo:
        for file, duration in file_durations_a4:
            archivo.write(f"{file}            {duration:.4f} \n")
        archivo.write(f"tiempo total en crear el nuevo archivo (incluye sort): {consolidated_duration_a4:.4f} segundos\n")
        archivo.write(f"tiempo total de ejecucion: {total_execution_time:.4f} segundos\n")
        
    print(f"Proceso completado. Archivos de log (a1 a a8) y diccionarios generados en: {project_folder}")