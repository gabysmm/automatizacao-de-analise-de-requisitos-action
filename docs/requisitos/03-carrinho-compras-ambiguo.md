# Módulo: Carrinho de compras

Sistema: Loja Online

## HU-01 — Adicionar produto ao carrinho

### História de usuário

Como cliente, quero adicionar produtos ao carrinho de forma simples, para que eu possa comprar vários itens de uma vez.

### Critérios de aceitação

- O botão "Adicionar ao carrinho" aparece na página de cada produto com estoque disponível.
- O carregamento do carrinho deve ser rápido após adicionar um produto.
- O ícone do carrinho mostra a quantidade total de itens adicionados.

## HU-02 — Alterar quantidade de um produto

### História de usuário

Como cliente, quero alterar a quantidade de um produto que já está no carrinho, para que eu compre exatamente o que preciso.

### Critérios de aceitação

- O campo de quantidade deve ser intuitivo para qualquer cliente.
- A quantidade mínima é 1 e a máxima é 10 unidades por produto.
- O valor total do carrinho é recalculado sempre que a quantidade muda.
- Remover um produto do carrinho deve ser fácil.

## HU-03 — Aplicar cupom de desconto

### História de usuário

Como cliente, quero aplicar um cupom de desconto no carrinho, para que eu pague menos na compra.

### Critérios de aceitação

- Apenas um cupom pode ser aplicado por compra.
- Um cupom vencido ou inexistente exibe a mensagem "Cupom inválido".
- O desconto aparece como uma linha separada, abaixo do subtotal.