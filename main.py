from colorama import Fore, init
from flask import Flask, send_from_directory, jsonify

init(autoreset=True)


class Scrabble:
    def __init__(self, path):
        self.data = self.load_data(path) or []

    def _separar_letras(self, texto):
        """
        Separa un texto en una lista de letras, incluyendo 'ch', 'll' y 'rr'
        como unidades únicas. Es una función auxiliar interna de la clase.
        """
        letras_separadas = []
        i = 0
        while i < len(texto):
            if i < len(texto) - 1 and texto[i:i+2] in ['ch', 'll', 'rr']:
                letras_separadas.append(texto[i:i+2])
                i += 2
            else:
                letras_separadas.append(texto[i])
                i += 1
        return letras_separadas

    def load_data(self, ruta_archivo):
        """
        Carga un diccionario de palabras desde un archivo de texto y lo
        almacena en un set para una búsqueda y lectura óptimas.
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
            print(f"Error: El archivo en la ruta '{ruta_archivo}' no se encontró.")
            return None
        except Exception as e:
            print(f"Ocurrió un error al leer el archivo: {e}")
            return None

    def sort_by_length_with_double_letters(self):
        """
        Ordena una lista de palabras por su longitud, teniendo en cuenta
        las letras dobles (ch, ll, rr) como una sola unidad.

        Args:
            palabras (list): Una lista de palabras para ordenar.

        Returns:
            list: Una nueva lista de palabras ordenada.
        """
        if not self.data:
            return []

        return sorted(self.data, key=lambda p: len(self._separar_letras(p)))


    def search_for_containing_string(self, substring: str, length_word: int = 0):
        """
        Busca palabras que contengan una subcadena específica.

        Args:
            substring (str): La subcadena a buscar.

        Returns:
            list: Una lista de palabras que contienen la subcadena.
        """
        if not self.data:
            return []

        substring = substring.lower()
        if length_word == 0:
            resultados = [word for word in self.data if substring in word]
        else:
            resultados = [word for word in self.data if substring in word and len(self._separar_letras(word)) == length_word]
        return resultados
    

def main(save_sorted: bool):
    scrabble = Scrabble("data.txt")
    sorted_data = scrabble.sort_by_length_with_double_letters()

    if save_sorted:
        # Pre-calculate the "BLOQUE" words
        bloque_words = set()
        for word in scrabble.data:
            if len(scrabble.search_for_containing_string(word, len(scrabble._separar_letras(word)) + 1)) == 0:
                bloque_words.add(word)

        # Write to file
        with open("sorted_data.txt", "w", encoding="utf-8") as f:
            for word in sorted_data:
                bloque_status = 'BLOQUE' if word in bloque_words else ''
                f.write(f"{word} ({len(scrabble._separar_letras(word))}) {bloque_status}\n")

    # Search methods
    resultados_busqueda = scrabble.search_for_containing_string("cogecha", len("cogecha"))
    print(resultados_busqueda)


### FLASK APP ###
app = Flask(__name__, static_folder='static')

# Serve the Next.js static files from the .next/static directory
@app.route('/_next/<path:filename>')
def serve_next_static(filename):
    return send_from_directory('front/.next/', filename)

# Serve the main index.html page
@app.route('/')
def serve_index():
    return send_from_directory('front/.next/server/app', 'index.html')

# Endpoint to search for a word
@app.route('/search/<string:substring>/<int:length>', methods=['GET'])
def search(substring, length):
    scrabble = Scrabble("data.txt")
    if not length:
        length = 0
    resultados = scrabble.search_for_containing_string(substring, length)
    return jsonify(resultados)


if __name__ == "__main__":
    # main(save_sorted=True)
    app.run(host='0.0.0.0', port=5000)
