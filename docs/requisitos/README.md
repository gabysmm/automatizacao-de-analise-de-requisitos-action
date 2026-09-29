# Conjunto de exemplos de requisitos (com gabarito)

Os documentados encontrados nessa pasta requisitos escritos em formato de história de usuário tentando imitar como um usuário leigo escreveria, cada um
acompanhado de um **gabarito**, que é a lista dos problemas que realmente existem nele. 

O as HU de exemplo e o gabarito tem como objetivo:

1. testar o MVP utilizando só a análise de regras na fase inicial. 
2. comparar, mais tarde, a análise por regras com a análise por LLM usando o mesmo conjunto.

## Documentos

| Arquivo | Cenário | Ocorrências esperadas |
|---|---|---|
| `01-emprestimo-livros-correto.md` | correto (doc de controle) | 0 |
| `02-cadastro-acesso-sem-secao.md` | falta seção obrigatória | 2 (falha em DOC-001) |
| `03-carrinho-compras-ambiguo.md` | termos ambíguos | 4 ( falha em REQ-001), 1 fora do dicionário |
| `04-agendamento-consultas-ambos.md` | os dois problemas | 4 (3 falhas REQ-001 + 1 falha em DOC-001) |

- 12 HUs no total
- 6 HUs sem problema
- 6 HUs com problema, quatro delas tendo 2 problemas cada, totalizando 10 ocorrências/problemas no total

## Formato dos documentos

Cada documento é um módulo com 2 a 3 histórias de usuário (HUs), possuindo este formato:

```markdown
# Módulo: <nome>

## HU-01 — <título do requisito>

### História de usuário

Como <papel>, quero <ação>, para que <benefício>.

### Critérios de aceitação

- <critério verificável>
```

## Formato do gabarito (`gabarito/*.yml`)

Um arquivo por documento, com uma entrada por **ocorrência** de problema:

| Campo | Significado |
|---|---|
| `id` | identificador da ocorrência (`<doc>-<nº>`) |
| `regra` | id da regra em `brain/regras-teste.yml` (DOC-001, REQ-001) |
| `hu` | em qual HU está o problema |
| `secao` | seção onde está o termo, ou qual seção está faltando |
| `linha` | indica a linha que está o erro |
| `termo` | termo ambíguo encontrado (só para erros REQ-001) |
| `no_dicionario` | `true` se o termo está na lista de termos_ambiguos |
| `justificativa` | por que é um problema e dicas (ajuda a avaliar o feedback gerado) |

## Comparar a saída da ferramenta com o gabarito

Uma ocorrência apontada pela ferramenta é um **acerto** quando bate com uma
entrada do gabarito em `documento` + `hu` + `regra` e mais:

- `termo`, para REQ-001 (uma HU pode ter mais de um termo ambíguo);
- `secao`, para DOC-001 (indica qual seção está faltando).

Cada apontamento é então classificado como:

- **Verdadeiro positivo (VP):** apontou e está no gabarito.
- **Falso positivo (FP):** apontou, mas não está no gabarito.
- **Falso negativo (FN):** está no gabarito, mas não foi apontado.

```text
precisão = VP / (VP + FP)   -> dos problemas apontados, quantos eram reais
recall   = VP / (VP + FN)   -> dos problemas reais, quantos foram encontrados
```