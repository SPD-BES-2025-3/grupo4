from models.envio import Envio
from repositories.repositorio_envio import RepositorioEnvio
from api.router_base import criar_crud_router

repositorio = RepositorioEnvio()
router = criar_crud_router(Envio, repositorio, "Envio")
