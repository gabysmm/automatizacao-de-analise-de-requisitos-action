---
categoria: armadilha
versao: 1.0
regras:
  ARM-01: { severidade: media }
  ARM-02: { severidade: media }
  ARM-03: { severidade: media }
---
# Armadilha

Vício de escrita comum na fala do dia a dia: a frase parece correta e completa,
mas a forma como foi escrita esconde uma lacuna ou uma ambiguidade.
Existem três padrões de armadilha (ARM-01, ARM-02 e ARM-03). Os sinais e
exemplos de cada um são ilustrativos, não uma lista fechada: interprete o texto
e aponte também construções semelhantes, com outras palavras, que caiam no
mesmo padrão. Não crie padrões novos fora desses três. Na mensagem, diga qual
padrão foi encontrado e o que ele esconde.

Fronteira: palavra ou frase com mais de um sentido ("rápido", "fácil") é
AMBIGUIDADE. Informação que simplesmente não está escrita (falta a história,
faltam critérios, falta o caso de erro) é LACUNA. Se o problema vem de um dos
padrões abaixo, classifique como ARMADILHA.

Quando não apontar (regra geral): o padrão só é falha se deixar a pergunta sem
resposta. Se a própria HU (a frase, a história ou os critérios) já deixa claro
quem faz, com o que se compara ou o que é pedido, não aponte.

## ARM-01 — Voz passiva sem responsável
- O que é: frase na voz passiva que não diz quem executa a ação (uma pessoa
  ou o sistema).
- Sinais (exemplos): verbo "ser" + particípio sem dizer por quem: "deve ser
  recebida", "é enviado", "os dados são fornecidos", "será aprovado".
- Com falha: "Dado que a encomenda chegou, quando o morador não estiver em casa,
  então a encomenda deve ser recebida e guardada."
- Por quê: não diz quem recebe e guarda a encomenda: o porteiro, o síndico ou
  outra pessoa.
- Corrigida: "Dado que a encomenda chegou, quando o morador não estiver em casa,
  então o porteiro recebe a encomenda e a registra no app."
- Não apontar quando:
  - quem faz está na mesma frase ("é recebida pelo porteiro");
  - a frase descreve um estado ou um evento que já aconteceu e ao qual a
    funcionalidade reage ("Dado que a encomenda foi retirada", "quando um QR
    code válido for lido");
  - na história, o usuário pede algo que só o sistema pode fazer por ele
    ("quero ser avisado quando minha encomenda chegar").
- Orientar: pergunte quem faz a ação: uma pessoa (qual papel?) ou o sistema.

## ARM-02 — Comparação sem referência
- O que é: comparação ("mais", "menos", "melhor", "pior", "maior") sem dizer
  com o que se compara nem quanto.
- Sinais (exemplos): "mais rápido", "menos passos", "mais fácil",
  "muito melhor", "com mais segurança".
- Com falha: "Como porteiro, quero registrar visitantes em menos passos, para
  não formar fila na entrada."
- Por quê: menos passos do que o quê, e quantos? Não dá para saber quando a
  meta foi atingida.
- Corrigida: "Como porteiro, quero registrar um visitante em no máximo 3 passos
  (hoje são 7), para não formar fila na entrada."
- Não apontar quando: a comparação traz a referência e o valor ("em até 30
  segundos, em vez dos 2 minutos de hoje", "mais rápido que 0,1 ms").
- Atenção: "rápido" sozinho, sem comparação, é AMBIGUIDADE.
- Orientar: pergunte como é hoje e qual valor seria aceitável.

## ARM-03 — Modelo preenchido sem conteúdo
- O que é: a HU segue o modelo (Como/quero/para, Dado/quando/então), mas uma
  parte foi preenchida só para cumprir o modelo: genérica, circular ou repetindo
  outra parte. Parece pronta, mas não diz o que é pedido.
- Sinais (exemplos): ação genérica ("usar o sistema", "gerenciar os dados", "acessar as
  funcionalidades"); benefício que repete a ação ("para poder cadastrar");
  critério que só repete a história ou diz apenas que "funciona corretamente".
- Com falha: "Como morador, quero gerenciar minhas encomendas, para ter minhas
  encomendas gerenciadas."
- Por quê: segue o modelo, mas não diz o que o morador faz (consultar? retirar?
  autorizar alguém?) nem o que ganha com isso.
- Corrigida: "Como morador, quero ver no app as encomendas que estão na
  portaria, para buscá-las sem precisar perguntar ao porteiro."
- Não apontar quando:
  - o papel é genérico ("Como usuário"), mas a ação e o benefício são concretos;
  - um verbo amplo ("gerenciar") é detalhado nos critérios de aceitação da
    mesma HU;
  - o benefício é curto ou óbvio, mas diferente da ação ("para não perder
    entregas").
- Atenção: se só uma palavra é vaga e o resto tem conteúdo, é AMBIGUIDADE; se a
  parte inteira não existe, é LACUNA.
- Orientar: pergunte o que a pessoa faz hoje e o que muda para ela com a
  funcionalidade.
