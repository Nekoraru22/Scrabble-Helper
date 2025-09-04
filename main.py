from flask import Flask, send_from_directory, jsonify, request


class Scrabble:
    def __init__(self, path):
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

    def search_for_containing_string(self, substring: str, length_word: int = 0, or_more: bool = False) -> list:
        """
        Busca palabras que contengan una subcadena específica.

        Args:
            substring: La subcadena a buscar.
            length_word: La longitud exacta de las palabras a buscar.
                         Si es 0, no se filtra por longitud.

        Returns: Una lista de palabras que contienen la subcadena.
        """
        if not self.data:
            return []

        substring = substring.lower()
        if length_word == 0:
            resultados = [word for word in self.data if substring in word]
        else:
            if or_more:
                resultados = [word for word in self.data if substring in word and self.get_letter_length(word) >= length_word]
            else:
                resultados = [word for word in self.data if substring in word and self.get_letter_length(word) == length_word]
        return resultados

    def find_bloque_words(self) -> set:
        """
        Encuentra palabras "bloque" en el conjunto de datos. Una palabra
        es considerada "bloque" si no está contenida en ninguna otra

        Returns: Un conjunto de palabras bloque.
        """
        # Group words by their letter length
        words_by_length = {}
        for word in self.data:
            length = self.get_letter_length(word)
            if length not in words_by_length:
                words_by_length[length] = set()
            words_by_length[length].add(word)
        
        bloque_words = set()
        total_checks = 0
        
        # For each length group, check if words appear in the next length group
        for length in sorted(words_by_length.keys()):
            if length + 1 not in words_by_length:
                continue
            
            current_words = words_by_length[length]
            next_length_words = words_by_length[length + 1]
            
            print(f"Checking {len(current_words)} words of length {length} against {len(next_length_words)} words of length {length + 1}")
            
            # Check if this word is contained in any word of the next length
            for word in current_words:
                for longer_word in next_length_words:
                    if word in longer_word:
                        bloque_words.add(word)
                        break
                total_checks += len(next_length_words)
        
        print(f"Total comparisons made: {total_checks:,}")
        print(f"Found {len(bloque_words)} bloque words")
        return bloque_words


def main():
    scrabble = Scrabble("data.txt")
    bloque_words = scrabble.find_bloque_words()
    
    print("Sorting data...")
    sorted_data = scrabble.sort_by_length_with_double_letters()
    
    print("Writing sorted data to file...")
    with open("sorted_data.txt", "w", encoding="utf-8") as f:
        for word in sorted_data:
            bloque_status = '' if word in bloque_words else ' - BLOQUE'
            f.write(f"{word} ({scrabble.get_letter_length(word)}){bloque_status}\n")
    
    print("Process completed!")


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
    scrabble = Scrabble("data.txt")
    if not length:
        length = 0

    resultados = scrabble.search_for_containing_string(substring, length, request.args.get('or_more') == 'true')
    return jsonify(resultados)


if __name__ == "__main__":
    # UNCOMENT TO RUN THE SCRABBLE PROCESS (IT TAKES A WHILE)
    main()
    app.run(host='0.0.0.0', port=5000)
