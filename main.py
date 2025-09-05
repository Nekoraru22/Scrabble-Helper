from flask import Flask, send_from_directory, jsonify, request
from multiprocessing import Pool, cpu_count
from collections import defaultdict

import json


class Scrabble:
    def __init__(self, path: str):
        self.data = self._load_data(path) or set()
        self._length_cache = {}

    def _split_letters(self, texto) -> list[str]:
        """
        Separa un texto en una lista de letras, incluyendo 'ch', 'll' y 'rr'
        como unidades únicas. Es una función auxiliar interna de la clase.

        Args:
            texto: El texto a separar.

        Returns: Una lista de letras y combinaciones especiales.
        """
        # Use cache to avoid recalculating
        if texto in self._length_cache:
            return self._length_cache[texto]
            
        letras_separadas = []
        i = 0
        while i < len(texto):
            if i < len(texto) - 1 and texto[i:i+2] in ['ch', 'll', 'rr']:
                letras_separadas.append(texto[i:i+2])
                i += 2
            else:
                letras_separadas.append(texto[i])
                i += 1
        
        self._length_cache[texto] = letras_separadas
        return letras_separadas

    def _load_data(self, ruta_archivo) -> set:
        """
        Carga un diccionario de palabras desde un archivo de texto y lo
        almacena en un set para una búsqueda y lectura óptimas.

        Args:
            ruta_archivo: La ruta al archivo de texto que contiene

        Returns: Un set con las palabras del diccionario.
        """
        diccionario = set()
        try:
            with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
                for linea in archivo:
                    palabra = linea.strip()
                    if palabra:
                        diccionario.add(palabra.lower())
            print(f"Diccionario cargado exitosamente. Se encontraron {len(diccionario)} palabras.")
            return diccionario
        except FileNotFoundError:
            raise FileNotFoundError(f"Error: El archivo en la ruta '{ruta_archivo}' no se encontró.")
        except Exception as e:
            raise IOError(f"Ocurrió un error al leer el archivo: {e}")

    def _check_word_chunk(self, args) -> set:
        """
        Función auxiliar para paralelización. Verifica si las palabras en un chunk
        están contenidas en otras palabras más largas.

        Args:
            args: Una tupla que contiene (words_to_check, longer_words_set).

        Returns: Un set de palabras que están contenidas en otras.
        """
        words_to_check, longer_words_set = args
        contained_words = set()
        
        for word in words_to_check:
            for longer_word in longer_words_set:
                if word != longer_word and word in longer_word:
                    contained_words.add(word)
                    break  # No need to check further if already found
        
        return contained_words

    def get_letter_length(self, palabra):
        """
        Get the length of a word considering double letters as single units.

        Args:
            palabra: The word to evaluate.

        Returns: The length of the word considering double letters.
        """
        return len(self._split_letters(palabra))

    def sort_by_length_with_double_letters(self):
        """
        Ordena una lista de palabras por su longitud, teniendo en cuenta
        las letras dobles como una sola unidad.

        Returns: Una nueva lista de palabras ordenada.
        """
        if not self.data:
            return []

        return sorted(self.data, key=lambda p: self.get_letter_length(p))
    
    def find_bloque_words(self) -> set:
        """
        Encuentra palabras "bloque" de manera optimizada usando paralelización.
        Una palabra es "bloque" si NO está contenida en ninguna otra palabra del diccionario.
        
        Returns: Un conjunto de palabras bloque (palabras NO contenidas en otras).
        """
        print("Iniciando búsqueda de palabras bloque optimizada...")
        
        # Group words by their lengths
        words_by_length = defaultdict(set)
        for word in self.data:
            length = self.get_letter_length(word)
            words_by_length[length].add(word)
        
        contained_words = set()
        total_comparisons = 0

        # Process lengths in ascending order
        lengths = sorted(words_by_length.keys())
        
        for i, current_length in enumerate(lengths):
            current_words = words_by_length[current_length]
            
            # Get all longer words
            longer_words = set()
            for j in range(i + 1, len(lengths)):
                longer_words.update(words_by_length[lengths[j]])
            
            if not longer_words:
                continue
            print(f"Verificando {len(current_words)} palabras de longitud {current_length} contra {len(longer_words)} palabras más largas...")
            
            # Divide the work into chunks for parallelization
            num_processes = min(cpu_count(), len(current_words))
            if num_processes > 1 and len(current_words) > 100:
                chunk_size = max(1, len(current_words) // num_processes)
                word_chunks = [list(current_words)[i:i + chunk_size] for i in range(0, len(current_words), chunk_size)]
                
                args = [(chunk, longer_words) for chunk in word_chunks]
                
                with Pool(num_processes) as pool:
                    results = pool.map(self._check_word_chunk, args)

                for result in results:
                    contained_words.update(result)
            else:
                # Single process for small datasets
                result = self._check_word_chunk((current_words, longer_words))
                contained_words.update(result)
            
            total_comparisons += len(current_words) * len(longer_words)
        
        bloque_words = self.data - contained_words
        
        print(f"Total de comparaciones estimadas: {total_comparisons:,}")
        print(f"Palabras contenidas en otras: {len(contained_words)}")
        print(f"Palabras BLOQUE encontradas: {len(bloque_words)}")
        
        return bloque_words


def load_data_api(path_api: str) -> list:
    """
    Carga los datos de la API desde un archivo JSON.
    
    Args:
        path_api: La ruta al archivo JSON.
        
    Returns: Una lista con los datos de la API o None si no se pudo cargar.
    """
    try:
        with open(path_api, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        print(f"Warning: Could not load API data from {path_api}. The web app will not have nothing to show.")
        return []


def search_for_containing_string(data_api: list, substring: str, length_word: int = 0, or_more: bool = False) -> list:
    """
    Busca palabras que contengan una subcadena específica.

    Args:
        substring: La subcadena a buscar.
        length_word: La longitud exacta de las palabras a buscar.
                        Si es 0, no se filtra por longitud.

    Returns: Una lista de palabras que contienen la subcadena.
    """
    substring = substring.lower()
    if length_word == 0:
        resultados = [word for word in data_api if substring in word['value']]
    else:
        if or_more:
            resultados = [word for word in data_api if substring in word['value'] and word['length'] >= length_word]
        else:
            resultados = [word for word in data_api if substring in word['value'] and word['length'] == length_word]
    return resultados


def main():
    scrabble = Scrabble("data.txt")
    bloque_words = scrabble.find_bloque_words()
    
    print("Sorting data...")
    sorted_data = scrabble.sort_by_length_with_double_letters()
    
    print("Writing sorted data to files...")
    with open("sorted_data.txt", "w", encoding="utf-8") as f:
        for word in sorted_data:
            bloque_status = ' - BLOQUE' if word in bloque_words else ''
            f.write(f"{word} ({scrabble.get_letter_length(word)}){bloque_status}\n")

    data_api = []
    for word in sorted_data:
        entry = {
            "value": word,
            "length": scrabble.get_letter_length(word),
            "is_bloque": word in bloque_words
        }
        data_api.append(entry)

    with open("data_api.json", "w", encoding="utf-8") as f:
        json.dump(data_api, f, ensure_ascii=False, indent=4)


### FLASK APP ###
app = Flask(__name__, static_folder='static')

# Serve the Next.js static files from the .next/static directory
@app.route('/_next/<path:filename>')
def serve_next_static(filename):
    return send_from_directory('scrabble-helper/.next/', filename)

# Serve other public files (like images, etc.) from the public directory
@app.route('/<path:filename>')
def serve_public(filename):
    return send_from_directory('scrabble-helper/public', filename)

# Serve the main index.html page
@app.route('/')
def serve_index():
    return send_from_directory('scrabble-helper/.next/server/app', 'index.html')

# Endpoint to search for a word
@app.route('/search/<string:substring>/<int:length>', methods=['GET'])
def search(substring, length):
    if not length:
        length = 0

    resultados = search_for_containing_string(data_api, substring, length, request.args.get('or_more') == 'true')
    return jsonify(resultados)


if __name__ == "__main__":
    # UNCOMENT TO RUN THE SCRABBLE PROCESS (IT TAKES A WHILE)
    # main()
    data_api = load_data_api("data_api.json")
    app.run(host='0.0.0.0', port=5000)
