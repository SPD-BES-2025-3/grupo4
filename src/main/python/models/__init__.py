from models.pedido import Pedido
from models.cliente import Cliente
from models.item_pedido import ItemPedido
from models.pagamento import Pagamento
from models.envio import Envio

Pedido.model_rebuild()
Cliente.model_rebuild()
ItemPedido.model_rebuild()
Pagamento.model_rebuild()
Envio.model_rebuild()
