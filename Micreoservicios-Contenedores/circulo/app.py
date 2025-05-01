from flask import Flask, request, jsonify
import math

app = Flask(__name__)

@app.route('/area', methods=['GET'])
def calc_area():
    try:
        radio = float(request.args.get('radio', 0))
        if radio <= 0:
            return jsonify({'error': 'El radio debe ser mayor que 0'}), 400
        area = math.pi * (radio ** 2)
        return jsonify({
            'figura': 'circulo',
            'radio': radio,
            'area': area
        })
    except ValueError:
        return jsonify({'error': 'Parámetros inválidos'}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)