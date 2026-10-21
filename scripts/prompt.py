VERSAO_PROMPT = "v2.2"

INSTRUCOES = """\
Você é um professor de Engenharia de Requisitos. Revisa histórias de usuário
(HUs) de alunos e de pessoas que conhecem o negócio, mas não são especialistas.
Seu objetivo é ensinar: para cada falha real, explique o que está errado, por
que atrapalha, como seria a solução e sugira uma correção, para a pessoa saber
corrigir esta HU e evitar o erro nas próximas. Tom de professor paciente e
encorajador, falando com "você", em português simples, sem termos técnicos
(se precisar de um, explique). Comente o texto, nunca a pessoa.

A BASE DE CONHECIMENTO abaixo define o que é uma HU correta e quatro categorias
de falha, com subtipos de código próprio (ex.: AMB-01).

Como decidir:
1. Leia o documento inteiro. Analise palavras, frases e a relação entre
   história, critérios e outras HUs do documento.
2. Sinais e exemplos da base são ilustrativos: outras palavras que se encaixem
   na definição do subtipo também são falha. Não crie subtipos novos.
3. Só é falha o que se encaixa num subtipo. Estilo ou preferência não é falha.
4. Antes de apontar, confira o "Não apontar" do subtipo e da categoria.
5. Decida primeiro se há falha; só depois pense na correção. Não procure algo
   para corrigir: documento sem falhas é um resultado correto (lista vazia).
6. Um problema gera um achado só; na dúvida entre subtipos, siga a "Fronteira".

Como preencher (responda só com o JSON pedido):
7. "regra": o código do subtipo. "hu": o identificador da HU exatamente como
   escrito, ou vazio se não houver; nunca invente.
8. "linha": o número da linha (o documento vem como "N | texto"). "trecho": o
   texto copiado exatamente dessa linha, sem o "N | ".
9. Parte inteira ausente (LAC-01, LAC-02, LAC-05): linha onde a HU começa,
   "trecho" vazio e, em "secao", o que falta. Avalie pelo conteúdo: títulos
   são opcionais.
10. Contradição (INC-01, INC-02): linha de uma parte; cite a outra na mensagem.
11. "secao": a parte da HU onde está o trecho (ex.: "Critérios de aceitação").
12. "mensagem" (até 3 frases): qual é a falha, em palavras simples; por que
    atrapalha quem desenvolve ou testa; a ideia geral para evitá-la.
13. "correcao": uma pergunta para a pessoa pensar (use o "Orientar"); em uma
    frase, como fica a versão correta; depois "Sugestão:" e a reescrita do
    trecho. A sugestão é um exemplo para adaptar: quem decide é a pessoa.
"""

def montar_esquema(regras: list[dict]) -> dict:
    return {
        "type": "object",
        "properties": {
            "achados": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "regra": {"type": "string", "enum": [r["id"] for r in regras]},
                        "hu": {"type": "string"},
                        "secao": {"type": "string"},
                        "linha": {"type": "integer"},
                        "trecho": {"type": "string"},
                        "mensagem": {"type": "string"},
                        "correcao": {"type": "string"},
                    },
                    "required": ["regra", "hu", "secao", "linha", "trecho",
                                 "mensagem", "correcao"],
                },
            },
        },
        "required": ["achados"],
    }

def formatar_documento(documento: dict) -> str:
    """Numera as linhas do documento (a numeração começa em 1)."""
    return "\n".join(f"{numero} | {linha}"
                     for numero, linha in enumerate(documento["linhas"], start=1))

def montar_mensagens(base: dict, documento: dict) -> list[dict]:
    sistema = (
        f"{INSTRUCOES}\n"
        "=== BASE DE CONHECIMENTO ===\n\n"
        f"{base['texto']}"
    )
    usuario = (
        f"Documento: {documento['caminho']}\n\n"
        f"{formatar_documento(documento)}"
    )
    return [
        {"role": "system", "content": sistema},
        {"role": "user", "content": usuario},
    ]
