---
categoria: lacuna
versao: 0.2
regras:
  LAC-01: { severidade: critica }
  LAC-02: { severidade: critica }
  LAC-03: { severidade: media }
  LAC-04: { severidade: media }
---
# Lacuna

Informação necessária para entender ou testar a HU que não está escrita.
A HU deve ser autossuficiente: quem lê não deve precisar adivinhar o que falta.
Os sinais e exemplos são ilustrativos, não uma lista fechada: interprete o
texto e aponte o que falta, mesmo com outras palavras, dentro dos quatro
subtipos abaixo. Não crie subtipos novos.

Fronteira: se a informação está escrita, mas permite mais de um sentido, é
AMBIGUIDADE. Se a parte existe, mas foi preenchida só para cumprir o modelo,
é ARMADILHA (ARM-03). Se falta quem executa a ação por causa da voz passiva,
é ARMADILHA (ARM-01).

Quando não apontar (regra geral): uma HU é um resumo da necessidade, que a
equipe detalha conversando. Falta de detalhe só é lacuna quando impede
entender o que é pedido ou verificar os critérios da própria HU. Não aponte:
- detalhes de tela, tecnologia ou implementação (a equipe decide);
- informação que está em outra parte da mesma HU ou em outra HU do documento;
- falta de HUs que podem estar em outros arquivos. Aponte dependência só
  quando a HU cita algo do mesmo documento que não existe nele.

## LAC-01 — Falta a história
- Sinais (exemplos): a HU tem título e critérios, mas não diz quem precisa,
  o que precisa e para quê.
- Avalie pelo conteúdo, não pelo título: a história existe se houver o texto
  "Como [quem], quero [o quê], para [por quê]" (ou "Como ..., Eu quero ...,
  Para que ..."), com ou sem o título "História de usuário".
- Orientar: escreva quem vai usar, o que quer fazer e o que ganha com isso.

## LAC-02 — Faltam os critérios de aceitação
- Sinais (exemplos): a HU tem a história, mas nenhuma condição que diga quando
  ela está pronta.
- Avalie pelo conteúdo: os critérios existem se houver condições verificáveis
  ("Dado ..., quando ..., então ..." ou lista), com ou sem título.
- Orientar: descreva situações concretas e o resultado esperado em cada uma.

## LAC-03 — Situação de erro ou exceção não tratada
- O que é: os critérios descrevem só o caminho em que tudo dá certo, embora a
  própria HU indique uma situação que pode dar errado.
- Sinais (exemplos): a HU depende de uma condição (autorização, prazo, limite,
  "se") e nenhum critério diz o que acontece quando ela não é atendida.
- Com falha: "Dado que o morador autorizou o visitante, quando ele chegar,
  então o porteiro libera a entrada." (e se o visitante não foi autorizado?)
- Corrigida: acrescentar "Dado que o visitante não foi autorizado, quando ele
  chegar, então o porteiro avisa o morador pelo app antes de liberar."
- Não apontar quando:
  - a exceção está em outro critério ou em outra HU do mesmo documento;
  - a HU não tem nenhuma condição que possa falhar;
  - a exceção seria técnica (queda de internet, erro no servidor).
- Orientar: pergunte "e se não der certo?" para cada condição da HU.

## LAC-04 — Ação incompleta (falta o quê, para quem ou onde)
- O que é: um verbo da HU sem as informações que ele exige para ser entendido.
- Sinais (exemplos): "enviar" sem dizer o quê ou para quem; "avisar" sem dizer
  quem; "mostrar" sem dizer o quê.
- Com falha: "Dado que a encomenda foi retirada, então o sistema envia um aviso."
- Por quê: não diz para quem vai o aviso (morador, porteiro, síndico).
- Corrigida: "... então o sistema envia um aviso ao morador pelo app."
- Não apontar quando:
  - a informação está na história ou em outro critério da mesma HU;
  - o complemento é óbvio pelo contexto (na HU do morador, "quero ser avisado"
    já diz quem recebe);
  - o que falta é só a forma técnica (canal, formato, tela) e a HU continua
    verificável sem isso.
- Orientar: pergunte quem recebe, o que exatamente e onde.
