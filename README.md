# Dos formas de ejecutar FastAPI
    1. uvicorn:main app
    2. Agregar las líneas de código
        if __name__ == "__main__":
            uvicorn.run("main:app", port=8000)
            
        Y luego correr main.py