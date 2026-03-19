from uvicorn import run


if __name__ == '__main__':
    run('src.app.main:app', host='127.0.0.1', port=8000)
