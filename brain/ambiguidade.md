---
categoria: ambiguidade
versao: 0.1
regras:
  AMB-01: { severidade: media }
  AMB-02: { severidade: media }
  AMB-03: { severidade: media }
  AMB-04: { severidade: media }
---
# Ambiguidade

O texto permite mais de uma interpretação: pessoas diferentes leem a mesma
frase e entendem coisas diferentes, achando que concordaram.
Analise nos dois níveis:
- palavras: termos que, sozinhos, admitem mais de um sentido ou não têm medida;
- frase inteira: mesmo sem nenhuma palavra suspeita, a frase pode ter mais de
  uma leitura. Teste: imagine duas pessoas implementando ou testando a frase.
  Se elas puderem fazer coisas diferentes e as duas estarem de acordo com o
  texto, é ambiguidade.
Os sinais e exemplos são ilustrativos, não uma lista fechada. Não crie
subtipos novos fora dos quatro abaixo.

Fronteira (estes casos são ARMADILHA, não ambiguidade):
- voz passiva que não diz quem executa a ação ("deve ser recebida");
- comparação ("mais", "menos", "melhor", "pior") sem dizer com o que se
  compara nem quanto ("mais rápido", "menos passos"). Já "rápido" sozinho,
  sem comparação, é AMB-01;
- ação genérica que ocupa a história inteira ("quero gerenciar").
Informação que não está escrita é LACUNA.
Não aponte "deve", "pode" ou "deveria" escritos em minúsculas.

Quando não apontar (regra geral): se o resto da HU (história, critérios ou
outra HU do documento) deixa um único sentido possível, não aponte.

## AMB-01 — Termo vago ou sem medida
- O que é: palavra de qualidade, quantidade ou intensidade que não diz quanto
  nem como medir.
- Sinais (exemplos): "rápido", "fácil", "intuitivo", "seguro", "adequado",
  "eficiente", "amigável"; "melhorar", "otimizar"; "alguns", "vários",
  "normalmente", "se possível", "quando necessário", "etc.", "entre outros".
- Com falha: "Como porteiro, quero um cadastro de visitantes fácil de usar,
  para não formar fila."
- Por quê: "fácil" muda de pessoa para pessoa e não dá para testar.
- Corrigida: "Como porteiro, quero cadastrar um visitante informando só nome
  e documento, em até 1 minuto, para não formar fila."
- Não apontar quando: os critérios da mesma HU dão a medida (a história diz
  "rápido", mas um critério diz "em até 1 minuto").
- Orientar: pergunte qual número, limite ou exemplo mostraria que está bom.

## AMB-02 — Palavra com mais de um sentido
- O que é: palavra que, no contexto da HU, pode se referir a coisas diferentes.
- Sinais (exemplos): substantivo que pode ser várias coisas no contexto
  ("ocorrências", "conteúdo", "dados", "cadastro"); papel genérico ("usuário")
  quando o documento tem papéis diferentes e a ação depende de quem é.
- Com falha: "Como síndico, quero ver as ocorrências do mês."
- Por quê: podem ser reclamações de moradores, registros da portaria ou os dois.
- Corrigida: "Como síndico, quero ver as reclamações feitas pelos moradores
  no mês."
- Não apontar quando: o contexto da HU deixa um só sentido; "Como usuário"
  em documento que só tem um tipo de usuário.
- Orientar: pergunte "[termo] quer dizer [opção A] ou [opção B]?".

## AMB-03 — Referência sem dono claro
- O que é: pronome ou referência que pode apontar para mais de uma pessoa
  ou coisa citada antes.
- Sinais (exemplos): "ele", "ela", "isso", "o mesmo", "este", "lá" quando há
  mais de um candidato antes na frase.
- Com falha: "Dado que o porteiro registrou a encomenda do morador, quando ele
  confirmar, então a encomenda é liberada."
- Por quê: quem confirma, o porteiro ou o morador?
- Corrigida: "... quando o morador confirmar a retirada no app, então ..."
- Não apontar quando: só existe um candidato possível.
- Orientar: troque o pronome pelo nome de quem ou do que se fala.

## AMB-04 — Frase com mais de uma leitura
- O que é: a frase não tem palavra suspeita, mas a forma como as partes se
  ligam permite entender o texto de mais de um jeito.
- Sinais (exemplos): não fica claro a que parte se aplica uma condição ou um
  complemento; "e/ou" que pode significar "os dois" ou "qualquer um".
- Com falha: "Moradores e visitantes cadastrados podem usar a academia."
- Por quê: "cadastrados" vale só para os visitantes ou para os dois?
- Corrigida: "Todos os moradores podem usar a academia. Visitantes podem
  usar se um morador tiver cadastrado a visita."
- Não apontar quando: os critérios da HU mostram qual leitura vale.
- Orientar: reescreva em duas frases curtas, uma para cada caso.
