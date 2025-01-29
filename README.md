# Sistema de Gestão de Pedidos - E-commerce

## Sobre o Projeto
Este projeto implementa um sistema de gestão de pedidos para e-commerce, desenvolvido em Python utilizando Programação Orientada a Objetos. O sistema permite que clientes realizem pedidos, escolham produtos, apliquem pagamentos e acompanhem o status da entrega.

## Requisitos do Sistema
- Python 3.7+
- pytest (para execução dos testes)

## Estrutura do Projeto
```
ecommerce_project/
│
├── src/
│   ├── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── ecommerce_system.py
│   └── tests/
│       ├── __init__.py
│       └── test_ecommerce.py
│
├── venv/
├── main.py
└── requirements.txt
```

## Classes Principais

### Produto
- Atributos:
  - id: Identificador único
  - nome: Nome do produto
  - preco: Preço unitário

### Cliente
- Atributos:
  - id: Identificador único
  - nome: Nome do cliente
  - endereco: Endereço de entrega
  - historico_pedidos: Lista de pedidos anteriores
- Métodos:
  - adicionar_pedido(): Associa um pedido ao cliente

### Pedido
- Atributos:
  - id: Identificador único
  - cliente: Cliente que fez o pedido
  - itens: Lista de produtos comprados
  - status: Estado atual do pedido (Aguardando Pagamento/Pago/Enviado/Entregue)
  - valor_total: Soma dos preços dos produtos
- Métodos:
  - adicionar_produto(): Adiciona itens ao pedido
  - calcular_total(): Retorna o valor total do pedido
  - atualizar_status(): Atualiza o status do pedido

### Pagamento
- Atributos:
  - pedido: Pedido associado ao pagamento
  - metodo: Tipo de pagamento (Cartão/Boleto/Pix)
  - status_pagamento: Estado do pagamento (Aguardando/Aprovado/Recusado)
- Métodos:
  - processar_pagamento(): Simula o processamento do pagamento

### Entrega
- Atributos:
  - pedido: Pedido sendo entregue
  - status_entrega: Estado da entrega (Aguardando Envio/Em Transporte/Entregue)
  - codigo_rastreamento: Código único para rastreamento
- Métodos:
  - iniciar_entrega(): Define o status como "Em Transporte"
  - finalizar_entrega(): Define o status como "Entregue"

## Instalação e Configuração

1. Clone o repositório:
```bash
git clone https://github.com/FelipeTiLustosa/ecommerce_project.git
cd ecommerce_project
```

2. Crie e ative um ambiente virtual:
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

## Executando o Projeto

### Testes Automatizados
Para executar os testes:
```bash
python -m pytest src/tests/
```

### Demonstração do Sistema
Para executar o exemplo de uso:
```bash
python main.py
```

## Funcionalidades Implementadas

### Gestão de Produtos
- Cadastro de produtos com ID único
- Definição de preços
- Associação com pedidos

### Gestão de Clientes
- Cadastro de clientes
- Histórico de pedidos
- Endereço para entrega

### Gestão de Pedidos
- Criação de pedidos
- Adição de produtos
- Cálculo de valores
- Acompanhamento de status

### Sistema de Pagamento
- Múltiplos métodos (Cartão, Boleto, Pix)
- Simulação de processamento
- Validação de status

### Sistema de Entrega
- Geração de código de rastreamento
- Acompanhamento de status
- Validações de regras de negócio

## Regras de Negócio Implementadas

1. Um pedido só pode ser enviado após o pagamento ser aprovado
2. A entrega só pode ser finalizada se estiver em transporte
3. O status do pedido é atualizado automaticamente conforme o progresso
4. Pagamentos são simulados com uma regra de valor máximo de R$ 1.000,00
5. Cada entrega recebe um código de rastreamento único

## Cenários de Teste

1. Criação de cliente e pedido
2. Adição de produtos ao pedido
3. Cálculo do valor total
4. Processamento de pagamento (aprovado e recusado)
5. Fluxo completo de entrega
6. Validações de regras de negócio
7. Tratamento de erros


## Observações Importantes

- O sistema atual utiliza simulações para processos como pagamento
- Os IDs são gerados utilizando UUID para garantir unicidade
- O sistema mantém os dados apenas em memória
- A regra de pagamento (limite de R$ 1.000,00) é apenas para demonstração

