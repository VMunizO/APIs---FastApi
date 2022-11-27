from typing import Optional
from pydantic import BaseModel
from fastapi import FastAPI,HTTPException
import datetime

app= FastAPI()  

class Cliente(BaseModel):
    posicao: Optional[int] = 0
    nome: str
    Tipo_de_atendimento: str
    atendimento: bool
    data_de_chegada: str

fila = [
    Cliente(posicao=1, nome="Mbappe", Tipo_de_atendimento="N", atendimento= False, data_de_chegada= datetime.datetime.now().strftime("%c")),
    Cliente(posicao=2, nome="Kunta kinte", Tipo_de_atendimento="N", atendimento= False, data_de_chegada= datetime.datetime.now().strftime("%c")),
    Cliente(posicao=3, nome="Kante", Tipo_de_atendimento="N", atendimento= False, data_de_chegada= datetime.datetime.now().strftime("%c")),
    Cliente(posicao=4, nome="Neymar", Tipo_de_atendimento="P", atendimento= False, data_de_chegada= datetime.datetime.now().strftime("%c")),
]

@app.get("/")
def home():
    return {"mensagem": "Avaliação de API"}

@app.get("/fila")
async def exibir_clientes_fila():
    if len(fila) == 0:
        return HTTPException(status_code=200, detail="")
    return {"clientes na fila": fila}

@app.get("/fila/{id}")
async def buscar_cliente_por_id(id: int):
    for i in fila:
        if id == i.posicao:
            return {"client": [cliente for cliente in fila if cliente.posicao == id]}
    return HTTPException(status_code=404, detail="Cliente não encontrado na fila!!")
               
@app.post("/fila")
async def adicionar_cliente(cliente: Cliente):
    cliente.posicao = fila[-1].posicao + 1
    cliente.atendimento = False
    cliente.data_de_chegada = datetime.datetime.now().strftime("%c")
    fila.append(cliente)
    return {"Mensagem": "Cliente adicionado a fila!!", "cliente": cliente}

@app.put("/fila")
def atualizar_fila():
    for i in fila:
        if i.posicao - 1 == 0:
            i.atendimento = True
            i.posicao -= 1
        else:
            i.posicao -= 1
    return {"mensagem": "Fila atualizada!!","Fila": fila}

@app.delete("/fila/{posicao}")
async def deletar_cliente_por_id(id: int):
        cliente = [cliente for cliente in fila if cliente.posicao == id]
        fila.remove(cliente[0])
        atualizar_fila()
        return {"Mensagem": "Cliente deletado da fila!!","fila": fila}