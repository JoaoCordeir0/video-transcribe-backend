import uvicorn
import logging
import dotenv
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from routes import router

# Carrega as variáveis de ambiente
dotenv.load_dotenv()

# Configuração de logging
logging.basicConfig(
    filename='errors.log',
    level=logging.ERROR,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Instância da API
app = FastAPI()

# Configuração de CORS
app.add_middleware(
    CORSMiddleware, 
    allow_origins=["*"],     
    allow_methods=["*"], 
    allow_headers=["*"]
)

""" NOTE: Middleware para capturar exceções """
@app.middleware("http")
async def log_exceptions(request: Request, call_next):
    try:
        response = await call_next(request)
        return response
    except Exception:
        logger.error(f"Error without request: {request.method} {request.url}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal Server Error"}
        )
    
# Inclui as rotas do arquivo routes.py
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)