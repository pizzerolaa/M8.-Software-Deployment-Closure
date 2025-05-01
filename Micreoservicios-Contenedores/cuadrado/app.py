from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/area', methods=['GET'])
def calc_area():
    try:
        lado = float(request.args.get('lado', 0))
        if lado <= 0:
            return jsonify({'error': 'El lado debe ser mayor que 0'}), 400
        area = lado ** 2
        return jsonify({
            'figura': 'cuadrado',
            'lado': lado,
            'area': area
        })
    except ValueError:
        return jsonify({'error': 'Parámetros inválidos'}), 400
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
