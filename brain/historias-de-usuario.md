---
tipo: referencia
versao: 0.1
---
# Histórias de usuário (referência)

Use este texto para entender o que é uma HU correta. Ele não é uma lista de
falhas: as falhas estão nos arquivos de cada categoria.

Uma HU é um resumo curto de uma necessidade, escrito do ponto de vista de quem
vai usar o sistema. A equipe detalha o restante conversando. Por isso a HU
descreve o problema, e não a solução técnica: não exija tela, botão,
tecnologia ou forma de implementar.

## A história
Modelo: "Como [quem], quero [o quê], para [por quê]".
Variações aceitas: "Como ..., Eu quero ..., Para que ...", "Como ..., quero
..., para que ...". Não aponte a escolha entre essas variações.
- Quem (papel): quem precisa da funcionalidade. Obrigatório.
- O quê (ação): o que a pessoa quer fazer. Obrigatório.
- Por quê (benefício): o objetivo ou ganho para a pessoa. Obrigatório.
  O benefício deve ser uma razão, não outra funcionalidade.

## Os critérios de aceitação
Condições que a HU precisa cumprir para ser considerada pronta. Toda HU deve
ter critérios. Formatos aceitos: "Dado [situação], quando [ação ou evento],
então [resultado]" ou uma lista de condições.
Um bom critério:
- descreve um resultado que dá para observar e testar (passa ou falha);
- cobre também o que acontece quando uma condição da HU não é atendida.

## Avalie o conteúdo, não a forma
Títulos de seção ("História de usuário", "Critérios de aceitação") são
opcionais. Uma parte existe se o conteúdo estiver lá, com ou sem título.
Uma HU pode seguir o modelo e ainda assim ter falhas: leia o que está escrito.

## Exemplo de HU correta (não faz parte do documento analisado)
Ver encomendas na portaria
Como morador, quero ver no app as encomendas que estão na portaria, para
buscá-las sem precisar perguntar ao porteiro.
1. Dado que o porteiro registrou uma encomenda para meu apartamento, quando
   eu abrir o app, então vejo a encomenda com a data de chegada.
2. Dado que retirei a encomenda, quando o porteiro confirmar a retirada,
   então ela sai da minha lista.
3. Dado que não há encomendas para meu apartamento, quando eu abrir o app,
   então vejo a mensagem "Nenhuma encomenda na portaria".
