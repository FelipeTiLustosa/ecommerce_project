import unittest
from datetime import datetime
from src.models.ecommerce_system import (
    Produto, Cliente, Pedido, Pagamento, Entrega,
    PedidoStatus, MetodoPagamento, StatusPagamento, StatusEntrega
)

class TestSistemaEcommerce(unittest.TestCase):
    def setUp(self):
        # Configuração inicial para cada teste
        self.cliente = Cliente("João Silva", "Rua das Flores, 123")
        self.produto1 = Produto("Notebook", 2500.00)
        self.produto2 = Produto("Mouse", 50.00)
        self.pedido = Pedido(self.cliente)

    def test_criar_cliente_e_pedido(self):
        """Teste de criação de cliente e vinculação com pedido"""
        self.assertEqual(self.pedido.cliente, self.cliente)
        self.assertIn(self.pedido, self.cliente.historico_pedidos)
        self.assertEqual(self.pedido.status, PedidoStatus.AGUARDANDO_PAGAMENTO)

    def test_adicionar_produtos_pedido(self):
        """Teste de adição de produtos ao pedido"""
        self.pedido.adicionar_produto(self.produto1, 1)
        self.pedido.adicionar_produto(self.produto2, 2)

        self.assertEqual(len(self.pedido.itens), 2)
        self.assertEqual(self.pedido.itens[0].produto, self.produto1)
        self.assertEqual(self.pedido.itens[0].quantidade, 1)
        self.assertEqual(self.pedido.itens[1].produto, self.produto2)
        self.assertEqual(self.pedido.itens[1].quantidade, 2)

    def test_calcular_total_pedido(self):
        """Teste de cálculo do valor total do pedido"""
        self.pedido.adicionar_produto(self.produto1, 1)  # 2500.00
        self.pedido.adicionar_produto(self.produto2, 2)  # 100.00

        total_esperado = 2600.00
        self.assertEqual(self.pedido.calcular_total(), total_esperado)

    def test_adicionar_quantidade_produto_existente(self):
        """Teste de adição de quantidade a um produto já existente no pedido"""
        self.pedido.adicionar_produto(self.produto1, 1)
        self.pedido.adicionar_produto(self.produto1, 2)

        self.assertEqual(len(self.pedido.itens), 1)
        self.assertEqual(self.pedido.itens[0].quantidade, 3)

    def test_processar_pagamento_aprovado(self):
        """Teste de processamento de pagamento aprovado"""
        self.pedido.adicionar_produto(self.produto2, 1)  # 50.00 (menor que 1000)
        pagamento = Pagamento(self.pedido, MetodoPagamento.CARTAO)

        resultado = pagamento.processar_pagamento()

        self.assertTrue(resultado)
        self.assertEqual(pagamento.status_pagamento, StatusPagamento.APROVADO)
        self.assertEqual(self.pedido.status, PedidoStatus.PAGO)

    def test_processar_pagamento_recusado(self):
        """Teste de processamento de pagamento recusado"""
        self.pedido.adicionar_produto(self.produto1, 1)  # 2500.00 (maior que 1000)
        pagamento = Pagamento(self.pedido, MetodoPagamento.CARTAO)

        resultado = pagamento.processar_pagamento()

        self.assertFalse(resultado)
        self.assertEqual(pagamento.status_pagamento, StatusPagamento.RECUSADO)
        self.assertEqual(self.pedido.status, PedidoStatus.AGUARDANDO_PAGAMENTO)

    def test_fluxo_entrega(self):
        """Teste do fluxo completo de entrega"""
        # Preparar pedido e pagamento
        self.pedido.adicionar_produto(self.produto2, 1)
        pagamento = Pagamento(self.pedido, MetodoPagamento.CARTAO)
        pagamento.processar_pagamento()

        # Criar e processar entrega
        entrega = Entrega(self.pedido)
        
        # Verificar status inicial
        self.assertEqual(entrega.status_entrega, StatusEntrega.AGUARDANDO_ENVIO)
        
        # Iniciar entrega
        entrega.iniciar_entrega()
        self.assertEqual(entrega.status_entrega, StatusEntrega.EM_TRANSPORTE)
        self.assertEqual(self.pedido.status, PedidoStatus.ENVIADO)
        
        # Finalizar entrega
        entrega.finalizar_entrega()
        self.assertEqual(entrega.status_entrega, StatusEntrega.ENTREGUE)
        self.assertEqual(self.pedido.status, PedidoStatus.ENTREGUE)

    def test_entrega_pedido_nao_pago(self):
        """Teste de tentativa de entrega de pedido não pago"""
        entrega = Entrega(self.pedido)
        
        with self.assertRaises(ValueError):
            entrega.iniciar_entrega()

    def test_finalizar_entrega_nao_iniciada(self):
        """Teste de tentativa de finalização de entrega não iniciada"""
        entrega = Entrega(self.pedido)
        
        with self.assertRaises(ValueError):
            entrega.finalizar_entrega()

if __name__ == '__main__':
    unittest.main()