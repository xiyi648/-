from app import create_app

app = create_app()

if __name__ == '__main__':
    # 生产环境用Gunicorn启动，此处为本地测试
    app.run(host='0.0.0.0', port=10000)