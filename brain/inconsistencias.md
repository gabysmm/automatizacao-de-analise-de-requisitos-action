---
categoria: inconsistencia
versao: 0.3
regras:
  INC-01: { severidade: critica }
  INC-02: { severidade: critica }
---
# Inconsistência

Duas partes se contradizem: comportamentos opostos ou valores diferentes para
a mesma coisa. Teste: implementadas juntas, na mesma situação e para a mesma
pessoa, cumprir uma obriga a desrespeitar a outra.
Fronteira: uma parte fala do assunto e a outra não é LACUNA. Uma vaga
("rápido") e outra precisa ("em até 1 minuto"): a precisa esclarece, não aponte.
Não apontar (geral): as partes valem para situações que não acontecem juntas
(perfis ou estados diferentes) ou há exceção declarada ("exceto", "a não ser que").

## INC-01 — Contradição dentro da mesma HU
- Sinais: a história e um critério, ou dois critérios, dizem coisas opostas.
- Com falha: história "quero autorizar visitantes a qualquer hora" e critério
  "às 23h o app bloqueia a autorização".
- Corrigida: usar a mesma regra nas duas partes ("das 6h às 22h").
- Orientar: mostre as duas frases e pergunte qual vale.

## INC-02 — Contradição entre HUs do mesmo documento
- Sinais: duas HUs dão regras ou valores diferentes para a mesma situação.
- Com falha: HU-01 "retirar a encomenda em até 7 dias" e HU-03 "encomendas
  não retiradas em 5 dias são devolvidas".
- Corrigida: usar o mesmo prazo nas duas HUs.
- Não apontar: as HUs tratam de perfis ou situações diferentes.
- Orientar: cite as duas HUs e pergunte qual regra está certa.
