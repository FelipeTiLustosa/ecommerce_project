from src.models.ecommerce_system import (
    Produto, Cliente, Pedido, Pagamento, 
    MetodoPagamento, Entrega
)

def demonstrar_sistema():
    # Criar alguns produtos
    notebook = Produto("Notebook", 2500.00)
    mouse = Produto("Mouse", 50.00)
    teclado = Produto("Teclado", 150.00)
    
    # Criar cliente
    cliente = Cliente("João Silva", "Rua das Flores, 123")
    
    # Criar e preencher pedido
    pedido = Pedido(cliente)
    pedido.adicionar_produto(notebook, 1)
    pedido.adicionar_produto(mouse, 2)
    pedido.adicionar_produto(teclado, 1)
    
    print("\n=== Detalhes do Pedido ===")
    print(f"Cliente: {cliente.nome}")
    print(f"Total do pedido: R$ {pedido.calcular_total():.2f}")
    
    # Tentar pagamento com valor alto (deve ser recusado)
    pagamento = Pagamento(pedido, MetodoPagamento.CARTAO)
    if pagamento.processar_pagamento():
        print("Pagamento aprovado!")
    else:
        print("Pagamento recusado - valor muito alto!")
    
    # Criar novo pedido apenas com mouse (valor baixo)
    pedido2 = Pedido(cliente)
    pedido2.adicionar_produto(mouse, 1)
    
    print("\n=== Detalhes do Segundo Pedido ===")
    print(f"Cliente: {cliente.nome}")
    print(f"Total do pedido: R$ {pedido2.calcular_total():.2f}")
    
    # Processar pagamento (deve ser aprovado)
    pagamento2 = Pagamento(pedido2, MetodoPagamento.PIX)
    if pagamento2.processar_pagamento():
        print("Pagamento aprovado!")
        
        # Criar e processar entrega
        entrega = Entrega(pedido2)
        print(f"Código de rastreamento: {entrega.codigo_rastreamento}")
        
        # Iniciar entrega
        entrega.iniciar_entrega()
        print("Entrega iniciada - Em transporte")
        
        # Finalizar entrega
        entrega.finalizar_entrega()
        print("Entrega finalizada - Pedido entregue")
    
    # Mostrar histórico de pedidos do cliente
    print("\n=== Histórico de Pedidos do Cliente ===")
    for idx, ped in enumerate(cliente.historico_pedidos, 1):
        print(f"Pedido {idx}: R$ {ped.calcular_total():.2f} - Status: {ped.status.value}")

if __name__ == "__main__":
    demonstrar_sistema()