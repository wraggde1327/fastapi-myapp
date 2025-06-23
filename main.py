from fastapi import FastAPI

app = FastAPI()

# Главная страница
@app.get("/")
def read_root():
    return {"message": "Привет с FastAPI!"}

# Эндпоинт для приветствия по имени
@app.get("/hello/{name}")
def say_hello(name: str):
    return {"message": f"Привет, {name}!"}

# Эндпоинт для сложения двух чисел
@app.get("/add")
def add_numbers(a: int, b: int):
    return {"result": a + b}
