import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


# Модель данных для операций
class Operation(BaseModel):
    num1: float
    num2: float
    operation: str  # "add", "subtract", "multiply", "divide"


# Имитация базы данных для хранения записей
database = []
а = 2

@app.post("/calculate/")
async def calculate(op: Operation):
    if op.operation == "add":
        result = op.num1 + op.num2
    elif op.operation == "subtract":
        result = op.num1 - op.num2
    elif op.operation == "multiply":
        result = op.num1 * op.num2
    elif op.operation == "divide":
        if op.num2 == 0:
            raise HTTPException(status_code=400, detail="Деление на ноль недопустимо.")
        result = op.num1 / op.num2
    else:
        raise HTTPException(status_code=400, detail="Неверная операция. Доступны: add, subtract, multiply, divide.")

    # Добавление записи в базу данных
    entry = {"num1": op.num1, "num2": op.num2, "operation": op.operation, "result": result}
    database.append(entry)

    return {"message": "Операция выполнена и добавлена в базу данных", "entry": entry}


@app.get("/operations/")
async def get_operations():
    if not database:
        return {"message": "Записей нет."}
    return {"operations": database}


@app.delete("/operations/{operation_id}")
async def delete_operation(operation_id: int):
    if 0 <= operation_id < len(database):
        removed_entry = database.pop(operation_id)
        return {"message": "Запись успешно удалена", "entry": removed_entry}
    else:
        raise HTTPException(status_code=404, detail="Запись с указанным ID не найдена")

if __name__ == '__main__':
    uvicorn.run("main:app", host='0.0.0.0', port=8080, reload=True)