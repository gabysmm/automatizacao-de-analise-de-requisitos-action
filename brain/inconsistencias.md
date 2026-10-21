---
categoria: inconsistencia
versao: 0.1
regras:
  INC-01: { severidade: alta }
  INC-02: { severidade: alta }
---
# Inconsistência

Duas partes do documento se contradizem: pedem comportamentos opostos ou
valores diferentes para a mesma coisa, de modo que não dá para atender as duas
ao mesmo tempo.
Interprete o sentido, não só as palavras. Teste: imagine as duas partes
implementadas juntas, na mesma situação e para a mesma pessoa. Se cumprir uma
obriga a desrespeitar a outra, é inconsistência.
Os exemplos são ilustrativos. Não crie subtipos novos fora dos dois abaixo.

Fronteira: se uma parte diz algo e a outra não fala do assunto, é LACUNA, não
inconsistência. Se uma parte é vaga ("rápido") e a outra é precisa ("em até
1 minuto"), a precisa esclarece a vaga: não é inconsistência.

Quando não apontar (regra geral): as duas partes valem para situações que não
acontecem ao mesmo tempo: perfis diferentes (morador × visitante), estados
diferentes (antes × depois do pagamento) ou uma exceção declarada ("exceto",
"a não ser que", "nesse caso").

## INC-01 — Contradição dentro da mesma HU
- O que é: a história e um critério, ou dois critérios da mesma HU, dizem
  coisas opostas.
- Com falha: história "Como morador, quero autorizar visitantes pelo app a
  qualquer hora..." e critério "Dado que são 23h, quando o morador tentar
  autorizar, então o app bloqueia a autorização."
- Por quê: "a qualquer hora" e o bloqueio às 23h não podem valer juntos.
- Corrigida: escolher uma regra e usar nas duas partes ("das 6h às 22h").
- Orientar: mostre as duas frases e pergunte qual delas vale.

## INC-02 — Contradição entre HUs do mesmo documento
- O que é: duas HUs do documento dão regras ou valores diferentes para a mesma
  situação.
- Com falha: HU-01 "o morador pode retirar a encomenda em até 7 dias" e HU-03
  "encomendas não retiradas em 5 dias são devolvidas".
- Por quê: entre o 5º e o 7º dia, a encomenda pode ser retirada ou já foi
  devolvida?
- Corrigida: usar o mesmo prazo nas duas HUs.
- Não apontar quando: as HUs tratam de perfis ou situações diferentes
  ("visitante só entra com autorização" × "prestador cadastrado entra direto").
- Orientar: cite as duas HUs e pergunte qual regra está certa.
