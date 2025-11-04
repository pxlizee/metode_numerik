from flask import Flask, render_template, request, jsonify
import numpy as np
import sympy
import google.generativeai as genai
import os

# --- Perbaikan 1: 'app' didefinisikan di atas ---
app = Flask(__name__)

# --- Peringatan Keamanan: Gunakan Environment Variable, jangan hardcode! ---
# Untuk sementara, Anda bisa hapus pagar di baris bawah dan masukkan kunci BARU Anda.
os.environ['GOOGLE_API_KEY'] = 'AIzaSyBri5lA09pa9h5nIaq_ijOtJTbTnyrmpTk' 
genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))


# ==============================================================================
# ROUTING UNTUK HALAMAN HTML & FUNGSI AI
# ==============================================================================

@app.route('/')
def index(): return render_template('index.html')

@app.route('/bisection')
def bisection_page(): return render_template('bisection.html')

@app.route('/regula-falsi')
def regula_falsi_page(): return render_template('regula_falsi.html')

@app.route('/newton-raphson')
def newton_raphson_page(): return render_template('newton_raphson.html')

@app.route('/secant')
def secant_page(): return render_template('secant.html')

@app.route('/maclaurin')
def maclaurin_page(): return render_template('maclaurin.html')

@app.route('/gauss-seidel')
def gauss_seidel_page(): return render_template('gauss_seidel.html')

@app.route('/analyze-case', methods=['POST'])
def analyze_case():
    data = request.get_json()
    case_text = data.get('text', '')
    method_type = data.get('method', '')

    prompt = f"""
    You are an intelligent assistant for a numerical methods calculator.
    Your task is to extract parameters from the user's text for the '{method_type}' method.
    Analyze the following text and return a JSON object containing the parameters.
    The function should be in a Python-readable format (e.g., use '**' for power, 'exp()' for e, 'sin()').
    Text: "{case_text}"
    Respond ONLY with the JSON object.
    """
    try:
        model = genai.GenerativeModel('gemini-1.0-pro')
        response = model.generate_content(prompt)
        cleaned_response = response.text.strip().replace('```json', '').replace('```', '')
        return jsonify({'parameters': cleaned_response})
    except Exception as e:
        return jsonify({'error': f"Error calling Gemini API: {str(e)}"}), 500

# ==============================================================================
# API ENDPOINTS UNTUK PERHITUNGAN
# ==============================================================================

def parse_function(str_func):
    x = sympy.symbols('x')
    func = sympy.sympify(str_func)
    return sympy.lambdify(x, func, 'numpy'), func, x

@app.route('/calculate/bisection', methods=['POST'])
def calculate_bisection():
    data = request.get_json()
    try:
        f, _, _ = parse_function(data['function'])
        a, b, tol = float(data['a']), float(data['b']), float(data['tolerance'])
        
        if f(a) * f(b) >= 0:
            return jsonify({'error': 'f(a) dan f(b) harus memiliki tanda yang berlawanan.'}), 400
        
        c, i = a, 0
        while (b - a) >= tol and i < 100:
            c = (a + b) / 2.0
            if f(c) == 0.0: break
            if f(c) * f(a) < 0: b = c
            else: a = c
            i += 1
        return jsonify({'root': c, 'iterations': i})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/calculate/regula-falsi', methods=['POST'])
def calculate_regula_falsi():
    data = request.get_json()
    try:
        f, _, _ = parse_function(data['function'])
        a, b, tol = float(data['a']), float(data['b']), float(data['tolerance'])
        
        if f(a) * f(b) >= 0:
            return jsonify({'error': 'f(a) dan f(b) harus memiliki tanda yang berlawanan.'}), 400
        
        # --- Perbaikan 2: Inisialisasi 'c' sebelum loop ---
        c, i = a, 0 
        while abs(f(c)) > tol and i < 100:
            # Pengecekan pembagian dengan nol
            if (f(b) - f(a)) == 0:
                return jsonify({'error': 'Pembagi bernilai nol (f(b) - f(a) = 0).'}), 400
            c = (a * f(b) - b * f(a)) / (f(b) - f(a))
            if f(c) == 0: break
            if f(a) * f(c) < 0: b = c
            else: a = c
            i += 1
        return jsonify({'root': c, 'iterations': i})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/calculate/newton-raphson', methods=['POST'])
def calculate_newton_raphson():
    data = request.get_json()
    try:
        f, func_expr, x_sym = parse_function(data['function'])
        df_expr = sympy.diff(func_expr, x_sym)
        df = sympy.lambdify(x_sym, df_expr, 'numpy')
        
        x0, tol = float(data['x0']), float(data['tolerance'])
        
        x_n, i = x0, 0
        while abs(f(x_n)) > tol and i < 100:
            if df(x_n) == 0: return jsonify({'error': 'Turunan bernilai nol.'}), 400
            x_n = x_n - f(x_n) / df(x_n)
            i += 1
        return jsonify({'root': x_n, 'iterations': i})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/calculate/secant', methods=['POST'])
def calculate_secant():
    data = request.get_json()
    try:
        f, _, _ = parse_function(data['function'])
        x0, x1, tol = float(data['x0']), float(data['x1']), float(data['tolerance'])
        
        i = 0
        while abs(f(x1)) > tol and i < 100:
            if (f(x1) - f(x0)) == 0: return jsonify({'error': 'Pembagi bernilai nol.'}), 400
            x_next = x1 - f(x1) * (x1 - x0) / (f(x1) - f(x0))
            x0, x1 = x1, x_next
            i += 1
        return jsonify({'root': x1, 'iterations': i})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/calculate/maclaurin', methods=['POST'])
def calculate_maclaurin():
    data = request.get_json()
    try:
        _, func_expr, x_sym = parse_function(data['function'])
        x_val, n_terms = float(data['x_value']), int(data['terms'])
        
        series_expr = func_expr.series(x_sym, 0, n_terms).removeO()
        series_func = sympy.lambdify(x_sym, series_expr, 'numpy')
        result_val = series_func(x_val)
        
        return jsonify({'result': result_val, 'series_polynomial': str(series_expr)})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/calculate/gauss-seidel', methods=['POST'])
def calculate_gauss_seidel():
    data = request.get_json()
    try:
        A_str, b_str = data['matrix_a'], data['vector_b']
        tol, max_iter = float(data['tolerance']), int(data['max_iter'])
        
        A = np.array([list(map(float, row.split(','))) for row in A_str.strip().split('\n')])
        b = np.array(list(map(float, b_str.strip().split(','))))
        
        if A.shape[0] != A.shape[1] or A.shape[0] != len(b):
            return jsonify({'error': 'Dimensi matriks A dan vektor b tidak sesuai.'}), 400
            
        n = len(b)
        x = np.zeros(n)
        
        for i in range(max_iter):
            x_old = x.copy()
            for j in range(n):
                if A[j, j] == 0:
                    return jsonify({'error': 'Elemen diagonal nol ditemukan.'}), 400
                sum_ax = np.dot(A[j, :j], x[:j]) + np.dot(A[j, j + 1:], x_old[j + 1:])
                x[j] = (b[j] - sum_ax) / A[j, j]
            if np.linalg.norm(x - x_old, ord=np.inf) < tol:
                return jsonify({'solution': x.tolist(), 'iterations': i + 1})
        
        return jsonify({'error': 'Gagal konvergen dalam batas iterasi maksimum.'}), 400
    except Exception as e:
        return jsonify({'error': f'Input tidak valid atau terjadi error: {e}'}), 400

if __name__ == '__main__':
    app.run(debug=True)
