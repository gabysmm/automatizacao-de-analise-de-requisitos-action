---
categoria: ambiguidade
versao: 0.2
regras:
  AMB-01: { severidade: media }
  AMB-02: { severidade: media }
  AMB-03: { severidade: media }
  AMB-04: { severidade: media }
---
# Ambiguidade

O texto permite mais de uma interpretação. Analise as palavras e também a
frase inteira. Teste: se duas pessoas pudessem implementar ou testar a frase
de jeitos diferentes, as duas de acordo com o texto, é ambiguidade.

Fronteira (é ARMADILHA, não ambiguidade): voz passiva sem quem executa;
comparação ("mais", "menos", "melhor") sem referência nem valor ("mais
rápido"; já "rápido" sozinho é AMB-01); ação genérica que ocupa a história
inteira ("quero gerenciar"). Informação não escrita é LACUNA.
Não aponte "deve", "pode" ou "deveria" em minúsculas.
Não apontar (geral): se o resto da HU ou do documento deixa um só sentido.

## AMB-01 — Termo vago ou sem medida
- Sinais: "rápido", "fácil", "intuitivo", "seguro", "adequado", "eficiente";
  "melhorar", "otimizar"; "alguns", "vários", "se possível", "etc.".
- Com falha: "Quero um cadastro de visitantes fácil de usar."
- Por quê: "fácil" muda de pessoa para pessoa e não dá para testar.
- Corrigida: "Quero cadastrar um visitante só com nome e documento, em até 1 minuto."
- Não apontar: um critério da mesma HU já dá a medida.
- Orientar: qual número, limite ou exemplo mostraria que está bom?

## AMB-02 — Palavra com mais de um sentido
- Sinais: substantivo que pode ser várias coisas ("ocorrências", "conteúdo",
  "dados"); "usuário" quando há papéis diferentes e a ação depende de quem é.
- Com falha: "Como síndico, quero ver as ocorrências do mês."
- Por quê: reclamações de moradores, registros da portaria ou os dois?
- Corrigida: "...ver as reclamações feitas pelos moradores no mês."
- Não apontar: o contexto deixa um só sentido; "Como usuário" em documento
  com um só tipo de usuário.
- Orientar: "[termo] quer dizer [A] ou [B]?"

## AMB-03 — Referência sem dono claro
- Sinais: "ele", "ela", "isso", "o mesmo" com mais de um candidato antes.
- Com falha: "Dado que o porteiro registrou a encomenda do morador, quando
  ele confirmar, então a encomenda é liberada."
- Por quê: quem confirma, o porteiro ou o morador?
- Não apontar: só há um candidato possível.
- Orientar: troque o pronome pelo nome de quem ou do que se fala.

## AMB-04 — Frase com mais de uma leitura
- Sinais: sem palavra suspeita, mas não fica claro a que parte se aplica uma
  condição ou complemento; "e/ou".
- Com falha: "Moradores e visitantes cadastrados podem usar a academia."
- Por quê: "cadastrados" vale só para visitantes ou para os dois?
- Corrigida: "Moradores podem usar a academia. Visitantes, se um morador
  cadastrou a visita."
- Não apontar: os critérios mostram qual leitura vale.
- Orientar: reescreva em frases curtas, uma para cada caso.
