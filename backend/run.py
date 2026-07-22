import os
os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"

from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=5000)
