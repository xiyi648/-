import random
from datetime import datetime

class UserProcessor:
    def __init__(self):
        # 模拟数据库
        self.users = [
            {'id': i, 'name': f'user{i}', 'created_at': datetime.now().isoformat()}
            for i in range(1, 21)
        ]
    
    def get_users(self, page=1, limit=10):
        # 模拟分页查询
        start = (page-1)*limit
        end = start + limit
        return self.users[start:end]
    
    def create_user(self, data):
        # 模拟创建逻辑
        new_id = len(self.users) + 1
        user = {
            'id': new_id,
            'name': data.get('name', f'user{new_id}'),
            'created_at': datetime.now().isoformat()
        }
        self.users.append(user)
        return user