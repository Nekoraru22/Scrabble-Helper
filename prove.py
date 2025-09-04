from main import Scrabble
from flask import Flask, send_from_directory, jsonify

app = Flask(__name__, static_folder='static')

# Serve the Next.js static files from the .next/static directory
@app.route('/_next/<path:filename>')
def serve_next_static(filename):
    return send_from_directory('front/.next/', filename)

# Serve the main index.html page
@app.route('/')
def serve_index():
    return send_from_directory('front/.next/server/app', 'index.html')

@app.route('/search/<string:substring>/<int:length>', methods=['GET'])
def search(substring, length):
    scrabble = Scrabble("data.txt")
    if not length:
        length = 0
    resultados = scrabble.search_for_containing_string(substring, length)
    return jsonify(resultados)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)