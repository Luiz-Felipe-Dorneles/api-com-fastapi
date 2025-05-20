from fastapi import FastAPI
from route import  series, motivos, ator, avaliacao, categoria

app = FastAPI()

app.include_router(series.router, prefix="/series", tags=["Séries"])
app.include_router(ator.router, prefix="/ator", tags=["Atores"])
app.include_router(categoria.router, prefix="/categoria", tags=["Categorias"])
app.include_router(avaliacao.router, prefix="/avaliacao", tags=["Avaliações"])
app.include_router(motivos.router, prefix="/motivos", tags=["Motivos para assistir!"])

