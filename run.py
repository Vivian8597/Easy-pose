from app import app

if __name__ == '__main__':
    # 启动Flask应用，debug模式便于开发
    app.run(debug=True, host='0.0.0.0', port=5000)
