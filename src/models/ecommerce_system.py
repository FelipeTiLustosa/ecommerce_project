from typing import List, Optional
from datetime import datetime
from enum import Enum
import uuid

class PedidoStatus(Enum):
    AGUARDANDO_PAGAMENTO = "Aguardando Pagamento"
    PAGO = "Pago"
    ENVIADO = "Enviado"
    ENTREGUE = "Entregue"

class MetodoPagamento(Enum):
    CARTAO = "Cartão"
    BOLETO = "Boleto"
    PIX = "Pix"

class StatusPagamento(Enum):
    AGUARDANDO = "Aguardando"
    APROVADO = "Aprovado"
    RECUSADO = "Recusado"

class StatusEntrega(Enum):
    AGUARDANDO_ENVIO = "Aguardando Envio"
    EM_TRANSPORTE = "Em Transporte"
    ENTREGUE = "Entregue"

class Produto:
    def __init__(self, nome: str, preco: float):
        self.id: str = str(uuid.uuid4())
        self.nome: str = nome
        self.preco: float = preco

    def __str__(self):
        return f"Produto(id={self.id}, nome={self.nome}, preco={self.preco})"

class ItemPedido:
    def __init__(self, produto: Produto, quantidade: int):
        self.produto = produto
        self.quantidade = quantidade

    @property
    def subtotal(self) -> float:
        return self.produto.preco * self.quantidade

class Cliente:
    def __init__(self, nome: str, endereco: str):
        self.id: str = str(uuid.uuid4())
        self.nome: str = nome
        self.endereco: str = endereco
        self.historico_pedidos: List['Pedido'] = []

    def adicionar_pedido(self, pedido: 'Pedido') -> None:
        if pedido not in self.historico_pedidos:
            self.historico_pedidos.append(pedido)

    def __str__(self):
        return f"Cliente(id={self.id}, nome={self.nome})"

class Pedido:
    def __init__(self, cliente: Cliente):
        self.id: str = str(uuid.uuid4())
        self.cliente: Cliente = cliente
        self.itens: List[ItemPedido] = []
        self.status: PedidoStatus = PedidoStatus.AGUARDANDO_PAGAMENTO
        self.data_criacao: datetime = datetime.now()
        self.cliente.adicionar_pedido(self)

    def adicionar_produto(self, produto: Produto, quantidade: int) -> None:
        if quantidade <= 0:
            raise ValueError("Quantidade deve ser maior que zero")
        
        # Verifica se o produto já existe no pedido
        for item in self.itens:
            if item.produto.id == produto.id:
                item.quantidade += quantidade
                return
        
        self.itens.append(ItemPedido(produto, quantidade))

    def calcular_total(self) -> float:
        return sum(item.subtotal for item in self.itens)

    def atualizar_status(self, novo_status: PedidoStatus) -> None:
        self.status = novo_status

    def __str__(self):
        return f"Pedido(id={self.id}, cliente={self.cliente.nome}, total={self.calcular_total()})"

class Pagamento:
    def __init__(self, pedido: Pedido, metodo: MetodoPagamento):
        self.id: str = str(uuid.uuid4())
        self.pedido: Pedido = pedido
        self.metodo: MetodoPagamento = metodo
        self.status_pagamento: StatusPagamento = StatusPagamento.AGUARDANDO
        self.data_processamento: Optional[datetime] = None

    def processar_pagamento(self) -> bool:
        """
        Simula o processamento do pagamento.
        Retorna True se o pagamento foi aprovado, False caso contrário.
        """
        # Simulação simplificada - aprova pagamentos com valor total menor que 1000
        self.data_processamento = datetime.now()
        
        if self.pedido.calcular_total() < 1000:
            self.status_pagamento = StatusPagamento.APROVADO
            self.pedido.atualizar_status(PedidoStatus.PAGO)
            return True
        
        self.status_pagamento = StatusPagamento.RECUSADO
        return False

class Entrega:
    def __init__(self, pedido: Pedido):
        self.id: str = str(uuid.uuid4())
        self.pedido: Pedido = pedido
        self.status_entrega: StatusEntrega = StatusEntrega.AGUARDANDO_ENVIO
        self.codigo_rastreamento: str = str(uuid.uuid4())[:8].upper()
        self.data_criacao: datetime = datetime.now()
        self.data_atualizacao: datetime = datetime.now()

    def iniciar_entrega(self) -> None:
        if self.pedido.status != PedidoStatus.PAGO:
            raise ValueError("Não é possível iniciar entrega de pedido não pago")
        
        self.status_entrega = StatusEntrega.EM_TRANSPORTE
        self.pedido.atualizar_status(PedidoStatus.ENVIADO)
        self.data_atualizacao = datetime.now()

    def finalizar_entrega(self) -> None:
        if self.status_entrega != StatusEntrega.EM_TRANSPORTE:
            raise ValueError("Não é possível finalizar entrega não iniciada")
        
        self.status_entrega = StatusEntrega.ENTREGUE
        self.pedido.atualizar_status(PedidoStatus.ENTREGUE)
        self.data_atualizacao = datetime.now()

    def __str__(self):
        return f"Entrega(codigo={self.codigo_rastreamento}, status={self.status_entrega.value})"