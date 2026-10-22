---
categoria: lacuna
versao: 0.5
regras:
  LAC-01: { severidade: critica }
  LAC-02: { severidade: critica }
  LAC-03: { severidade: media }
  LAC-04: { severidade: media }
  LAC-05: { severidade: media }
---
# Lacuna

Falta informação necessária para entender ou testar a HU.
Fronteira: escrito mas com mais de um sentido é AMBIGUIDADE; parte que existe
mas só cumpre o modelo é ARM-03; falta de quem executa por voz passiva é ARM-01.
Não apontar (geral): a HU é um resumo, detalhado em conversa. Só é lacuna o
que impede entender o pedido ou verificar os critérios da própria HU. Não
aponte detalhes de tela ou tecnologia, nem o que está em outra parte da HU ou
em outra HU do documento, nem HUs que podem estar em outros arquivos.

## LAC-01 — Falta a história
- Sinais: há título e critérios, mas não há quem, o quê e por quê.
- Orientar: escreva quem vai usar, o que quer fazer e o que ganha com isso.

## LAC-02 — Faltam os critérios de aceitação
- Sinais: há a história, mas nenhuma condição que diga quando ela está pronta.
- Orientar: descreva situações concretas e o resultado esperado em cada uma.

## LAC-03 — Situação de erro ou exceção não tratada
- Sinais: a HU depende de uma condição (autorização, prazo, limite, "se") e
  nenhum critério diz o que acontece quando ela não é atendida.
- Com falha: "Dado que o morador autorizou o visitante, quando ele chegar,
  então o porteiro libera a entrada." (e se não autorizou?)
- Corrigida: acrescentar "Dado que o visitante não foi autorizado, quando
  chegar, então o porteiro avisa o morador antes de liberar."
- Não apontar: a exceção está em outro critério ou HU; a HU não tem condição
  que possa falhar; a exceção seria técnica (internet, servidor); a própria
  regra já implica o resultado ("no máximo 2 vezes" implica que a 3ª é
  recusada) e faltaria só a mensagem ou a tela.
- Orientar: "e se não der certo?" para cada condição.

## LAC-04 — Ação incompleta (falta o quê, para quem ou onde)
- Sinais: "enviar" sem o quê ou para quem; "avisar" sem quem; "mostrar" sem o quê.
- Com falha: "Dado que a encomenda foi retirada, então o sistema envia um aviso."
- Por quê: para quem vai o aviso?
- Corrigida: "... então o sistema envia um aviso ao morador pelo app."
- Não apontar: a informação está em outra parte da HU ou é óbvia pelo
  contexto; falta só o detalhe técnico (canal, formato, tela).
- Orientar: quem recebe, o que exatamente e onde?

## LAC-05 — Falta o benefício
- Sinais: a história diz quem e o quê, mas termina sem dizer para quê.
- Com falha: "Como morador, quero ver as encomendas que estão na portaria."
- Corrigida: "..., para buscá-las sem perguntar ao porteiro."
- Não apontar: o objetivo aparece com outras palavras. Benefício que só
  repete a ação é ARM-03.
- Orientar: o que a pessoa ganha ou resolve com isso?
