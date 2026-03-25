import math
from flask import jsonify, request
from .database import get_db
from .calculations import *

# 获取所有学科
def get_subjects():
    db = get_db()
    subjects = db.get_all_subjects()
    return jsonify(subjects)

# 获取内容列表
def get_contents():
    db = get_db()
    subject = request.args.get('subject')
    if subject:
        contents = db.get_contents_by_subject(subject)
    else:
        contents = db.get_all_contents()
    return jsonify(contents)

# 获取单个内容详情
def get_content(id):
    db = get_db()
    content = db.get_content_by_id(id)
    if not content:
        return jsonify({'error': 'Content not found'}), 404
    return jsonify(content)

# 1.1.计算调和级数
def calculate_harmonic_series():
    data = request.get_json()
    if not data or 'n' not in data:
        return jsonify({'error': 'Invalid request data'}), 400

    n = data['n']
    if not isinstance(n, int) or n < 0:
        return jsonify({'error': 'n must be a non-negative integer'}), 400

    sum_value = calculate_harmonic_sum(n)
    approx = math.log(n) + 0.5772156649 if n > 0 else 0.0

    response = {
        'sum': sum_value,
        'approx': approx
    }

    return jsonify(response)

# 1.2.寻找调和级数和超过目标值的最小n
def find_harmonic_n():
    data = request.get_json()
    if not data or 'target' not in data:
        return jsonify({'error': 'Invalid request data'}), 400

    target = data['target']
    if not isinstance(target, (int, float)) or target < 0:
        return jsonify({'error': 'target must be a non-negative number'}), 400

    n = find_n_for_target(target)
    sum_value = calculate_harmonic_sum(n)

    response = {
        'n': n,
        'sum': sum_value,
        'exceeds': sum_value >= target
    }

    return jsonify(response)

# 2.计算洛伦兹变换
def calculate_lorentz_transformation_handler():
    data = request.get_json()
    if not data or 'x' not in data or 't' not in data or 'v' not in data:
        return jsonify({'error': 'Invalid request data'}), 400

    x = data['x']
    t = data['t']
    v = data['v']

    if not all(isinstance(val, (int, float)) for val in [x, t, v]):
        return jsonify({'error': 'x, t, and v must be numbers'}), 400

    try:
        x_prime, t_prime, gamma = calculate_lorentz_transformation(x, t, v)
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

    response = {
        'xPrime': x_prime,
        'tPrime': t_prime,
        'gamma': gamma
    }

    return jsonify(response)

# 3.计算1~n的和
def calculate_sum_of_n_handler():
    data = request.get_json()
    if not data or 'n' not in data:
        return jsonify({'error': 'Invalid request data'}), 400

    n = data['n']
    # 处理浮点数输入，特别是科学计数法表示的数值
    if isinstance(n, float):
        # 检查是否是整数
        if n.is_integer():
            n = int(n)
        else:
            return jsonify({'error': 'n must be a non-negative integer'}), 400
    if not isinstance(n, int) or n < 0:
        return jsonify({'error': 'n must be a non-negative integer'}), 400

    sum_value = calculate_sum_of_n(n)
    overflow = sum_value is None
    if overflow:
        sum_value = 0

    response = {
        'sum': sum_value,
        'overflow': overflow
    }

    return jsonify(response)
