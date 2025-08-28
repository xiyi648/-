from flask import Blueprint, jsonify, request
from app.core.data_processor import UserProcessor

bp = Blueprint('users', __name__)
processor = UserProcessor()

# 模拟：获取用户列表
@bp.get('')
def get_users():
    page = request.args.get('page', 1, type=int)
    users = processor.get_users(page=page, limit=10)
    return jsonify({
        'code': 200,
        'data': users,
        'msg': 'success'
    })

# 模拟：创建用户
@bp.post('')
def create_user():
    data = request.json or {}
    user = processor.create_user(data)
    return jsonify({
        'code': 201,
        'data': user,
        'msg': 'user created'
    })