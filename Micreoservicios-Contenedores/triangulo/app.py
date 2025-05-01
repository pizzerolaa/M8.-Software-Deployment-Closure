from flask import Flask, request, jsonify
import math

app = Flask(__name__)

@app.route('/area', methods=['GET'])
def calc_area():
    try:
        base = float(request.args.get('base', 0))
        altura = float(request.args.get('altura', 0))
        if base <= 0 or altura <= 0:
            return jsonify({'error': 'La base y la altura deben ser mayores que 0'}), 400
        area = (base * altura) / 2
        return jsonify({
            'figura': 'triangulo',
            'base': base,
            'altura': altura,
            'area': area
        })
    except ValueError:
        return jsonify({'error': 'Parámetros inválidos'}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)