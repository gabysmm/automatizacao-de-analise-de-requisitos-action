---
categoria: armadilha
versao: 1.1
regras:
  ARM-01: { severidade: media }
  ARM-02: { severidade: media }
  ARM-03: { severidade: media }
---
# Armadilha

Vício de escrita comum na fala: a frase parece correta e completa, mas a forma
esconde uma lacuna ou ambiguidade. Na mensagem, diga qual padrão é e o que ele
esconde.
Fronteira: palavra com vários sentidos ou vaga ("rápido") é AMBIGUIDADE;
informação não escrita é LACUNA.
Não apontar (geral): se a própria HU já deixa claro quem faz, com o que se
compara ou o que é pedido.

## ARM-01 — Voz passiva sem responsável
- Sinais: "ser" + particípio sem dizer por quem: "deve ser recebida",
  "é enviado", "os dados são fornecidos".
- Com falha: "Dado que a encomenda chegou, quando o morador não estiver em
  casa, então a encomenda deve ser recebida e guardada."
- Por quê: quem recebe e guarda: o porteiro, o síndico ou outra pessoa?
- Corrigida: "... então o porteiro recebe a encomenda e a registra no app."
- Não apontar: quem faz está na frase ("recebida pelo porteiro"); a frase
  descreve um estado ou evento ao qual o sistema reage ("Dado que a encomenda
  foi retirada", "quando um QR code for lido"); o usuário pede algo que só o
  sistema faz por ele ("quero ser avisado quando chegar").
- Orientar: quem faz a ação: uma pessoa (qual?) ou o sistema?

## ARM-02 — Comparação sem referência
- Sinais: "mais rápido", "menos passos", "mais fácil", "muito melhor", sem
  dizer em relação a quê nem quanto.
- Com falha: "Quero registrar visitantes em menos passos."
- Por quê: menos que o quê, e quantos? Não dá para saber quando está pronto.
- Corrigida: "Quero registrar um visitante em no máximo 3 passos (hoje são 7)."
- Não apontar: há referência e valor ("em 30 s, em vez dos 2 min de hoje").
- Orientar: como é hoje e qual valor seria aceitável?

## ARM-03 — Modelo preenchido sem conteúdo
- Sinais: segue o modelo, mas uma parte é genérica, circular ou repete outra:
  "usar o sistema", "gerenciar os dados"; benefício que repete a ação; critério
  que só repete a história ou diz "funciona corretamente".
- Com falha: "Como morador, quero gerenciar minhas encomendas, para ter minhas
  encomendas gerenciadas."
- Por quê: não diz o que o morador faz (consultar? retirar?) nem o que ganha.
- Corrigida: "Como morador, quero ver no app as encomendas na portaria, para
  buscá-las sem perguntar ao porteiro."
- Não apontar: papel genérico ("usuário") com ação e benefício concretos; verbo
  amplo detalhado nos critérios; benefício curto mas diferente da ação.
- Orientar: o que a pessoa faz hoje e o que muda para ela?
