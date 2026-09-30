# automatizacao-de-analise-de-requisitos-action

Protótipo experimental de uma solução baseada em LLM para análise automatizada de requisitos de software especificados e documentados por usuários leigos, com foco na identificação de problemas como ambiguidades, incompletudes e inconsistências, além da geração de feedback para auxiliar sua melhoria.

> **Versão atual: MVP sem IA.** A análise atual é feita por regras fixas. Integração com LLM em desenvolvimento.

## O que o MVP verifica

| Regra | Problema | Severidade |
|---|---|---|
| DOC-001 | A história de usuário não tem todas as suas seções obrigatórias como a história de usuário em si ou seus critérios de aceitação. | crítica |
| REQ-001 | O texto usa um termo ambíguo da lista (ex.: rápido, fácil, intuitivo, adequado, eficiente) | média |

As regras e seus parâmetros ficam em `brain/regras-teste.yml`.

## Estrutura

```text
.github/workflows/   -> pipeline
brain/ -> base de conhecimento

docs/requisitos/  -> requisitos em formato de HU e gabarito de reposta

scripts/ -> codigo das analise
```

A análise segue a arquitetura de **tubos e filtros**: cada script é uma etapa independente, e elas se comunicam pelo arquivo `saida/resultado.json`.


## Como rodar localmente?

Requer Python 3.12.

```bash
python -m pip install -r requirements.txt

python scripts/analisar_documentos.py --saida saida/resultado.json
python scripts/gerar_relatorio.py saida/resultado.json
python scripts/verificar_achados.py saida/resultado.json
```

1. `analisar_documentos.py`: aplica as regras e grava os achados em `saida/resultado.json`.
2. `gerar_relatorio.py`: mostra o relatório em Markdown, agrupado por documento.
3. `verificar_achados.py`: termina com erro se houver achado de severidade média, alta ou crítica.

## Como funciona a pipeline?

O workflow `.github/workflows/analise-requisitos.yml` roda:

- automaticamente, a cada `push` que altere `docs/requisitos/**.md` ou `brain/**`;
- manualmente, pela aba **Actions** (**Run workflow**).
- localmente via os comandos na seção acima.

> **OBS:** Quando é rodado localmente, a pipeline gera a resposta no terminal e não no actions. 

Na página da execução aparecem:

- **Summary**: o relatório com os achados;
- **Anotações**: cada problema apontando o arquivo e a linha;
- **Artifacts**: o `resultado.json` para download.

A pipeline **falha** quando existe algum achado de severidade **média, alta ou crítica**, para indicar que os requisitos precisam ser corrigidos. Achados de severidade baixa não fazem a pipeline falhar.

## Limitações conhecidas dessa versão

- A REQ-001 só encontra termos que estão na lista de `brain/regras-teste.yml`. Termos ambíguos fora da lista (ex.: "simples") não são detectados. Esse é um dos pontos a comparar com a análise por LLM. Tal situação ocorreu com a história de usuário de id 03-01
- Advérbios (ex.: "rapidamente") e plurais irregulares podem não ser reconhecidos.
