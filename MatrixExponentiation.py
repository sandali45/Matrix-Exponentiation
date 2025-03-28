from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Matrix multiplication helper
def matrix_mult(A, B):
    # Multiply two matrices A and B
    n = len(A)
    result = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                result[i][j] += A[i][k] * B[k][j]
    return result


# Naive method for matrix exponentiation
def matrix_exponentiation_naive(matrix, exponent):
    n = len(matrix)
    result = [[1 if i == j else 0 for j in range(n)] for i in range(n)]  # Identity matrix
    for _ in range(exponent):
        result = matrix_mult(result, matrix)
    return result


# Exponentiation by squaring
def matrix_exponentiation_squaring(matrix, exponent):
    n = len(matrix)
    result = [[1 if i == j else 0 for j in range(n)] for i in range(n)]  # Identity matrix
    base = matrix
    while exponent > 0:
        if exponent % 2 == 1:
            result = matrix_mult(result, base)
        base = matrix_mult(base, base)
        exponent //= 2
    return result


# Iterative matrix exponentiation
def matrix_exponentiation_iterative(matrix, exponent):
    n = len(matrix)
    result = [[1 if i == j else 0 for j in range(n)] for i in range(n)]  # Identity matrix
    base = matrix
    for _ in range(exponent):
        result = matrix_mult(result, base)
    return result


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/fibonacci')
def fibonacci_page():
    return render_template('fibonacci.html')


@app.route('/tribonacci')
def tribonacci_page():
    return render_template('tribonacci.html')


@app.route('/matrix-exponentiation', methods=['POST'])
def matrix_exponentiation():
    data = request.get_json()
    method = data['method']
    exponent = int(data['exponent'])
    matrix = data['matrix']

    # Perform matrix exponentiation based on selected method
    if method == 'naive':
        result = matrix_exponentiation_naive(matrix, exponent)
    elif method == 'exponentiation':
        result = matrix_exponentiation_squaring(matrix, exponent)
    elif method == 'iterative':
        result = matrix_exponentiation_iterative(matrix, exponent)
    else:
        return jsonify({'error': 'Invalid method'}), 400

    return jsonify({'result': result})


@app.route('/fibonacci/<int:n>')
def calculate_fibonacci(n):
    """Computes the nth Fibonacci number using matrix exponentiation."""
    if n == 0:
        return jsonify({'result': '0'})
    elif n == 1:
        return jsonify({'result': '1'})

    F = [[1, 1], [1, 0]]  # Fibonacci transformation matrix
    result_matrix = matrix_exponentiation_squaring(F, n - 1)  # Get (n-1)th power of F

    return jsonify({'result': str(result_matrix[0][0])})  # Fibonacci(n)


@app.route('/tribonacci/<int:n>')
def calculate_tribonacci(n):
    """Computes the nth Tribonacci number using matrix exponentiation."""
    # Handle base cases
    if n == 0:
        return jsonify({'result': '0'})
    elif n == 1 or n == 2:
        return jsonify({'result': '1'})

    # Tribonacci transformation matrix
    T = [[1, 1, 1],
         [1, 0, 0],
         [0, 1, 0]]  # Tribonacci transformation matrix

    # Initial vector (base cases for Tribonacci sequence)
    initial_vector = [1, 1, 0]  # T(2), T(1), T(0) as [1, 1, 0]

    # Matrix exponentiation by squaring to get the (n-2)th power of the transformation matrix
    result_matrix = matrix_exponentiation_squaring(T, n - 2)

    # Multiply the result matrix with the initial vector to get the nth Tribonacci number
    tribonacci_number = sum(result_matrix[0][i] * initial_vector[i] for i in range(3))

    return jsonify({'result': str(tribonacci_number)})




if __name__ == "__main__":
    app.run(debug=True)
