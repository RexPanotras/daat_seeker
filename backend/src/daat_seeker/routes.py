from flask import Blueprint
from .handlers import *
# 创建蓝图
api_bp = Blueprint('api', __name__)

# 注册路由
api_bp.route('/subjects', methods=['GET'])(get_subjects)
api_bp.route('/contents', methods=['GET'])(get_contents)
api_bp.route('/contents/<int:id>', methods=['GET'])(get_content)

api_bp.route('/calculate/harmonic', methods=['POST'])(calculate_harmonic_series)
api_bp.route('/calculate/harmonic/inverse', methods=['POST'])(find_harmonic_n)
api_bp.route('/calculate/lorentz', methods=['POST'])(calculate_lorentz_transformation_handler)
api_bp.route('/calculate/sum1ton', methods=['POST'])(calculate_sum_of_n_handler)