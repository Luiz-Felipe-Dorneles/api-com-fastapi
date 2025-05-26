from fastapi import FastAPI
from route import  series, motivos, ator, avaliacao, categoria

app = FastAPI()

app.include_router(series.router, prefix="/series", tags=["𝚂𝚎́𝚛𝚒𝚎𝚜"])
app.include_router(ator.router, prefix="/ator", tags=["𝙰𝚝𝚘𝚛𝚎𝚜"])
app.include_router(categoria.router, prefix="/categoria", tags=["𝙲𝚊𝚝𝚎𝚐𝚘𝚛𝚒𝚊𝚜"])
app.include_router(avaliacao.router, prefix="/avaliacao", tags=["𝙰𝚟𝚊𝚕𝚒𝚊𝚌̧𝚘̃𝚎𝚜"])
app.include_router(motivos.router, prefix="/motivos", tags=["𝙼𝚘𝚝𝚒𝚟𝚘𝚜 𝚙𝚊𝚛𝚊 𝚊𝚜𝚜𝚒𝚜𝚝𝚒𝚛"])

