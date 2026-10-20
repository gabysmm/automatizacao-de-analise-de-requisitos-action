import json
import yaml

VERSAO_PROMPT = "v1"
INSTRUCOES = """\
Você é um analista de requisitos de software sênior. Sua tarefa é revisar a histórias de
usuário (HUs) escritas por pessoas que conhecem o negócio, mas não são
especialistas em Engenharia de Requisitos, e apontar problemas de qualidade.

Regras de trabalho:
1. Use SOMENTE as regras fornecidas. Cada problema apontado deve citar o id de
   uma dessas regras. Não crie regras novas.
2. Os parâmetros de cada regra são referência. Em listas de termos, os termos
   são exemplos: aponte também outras palavras vagas ou subjetivas de mesmo
   sentido, desde que se encaixem na regra.
3. O documento vem com o número de cada linha no formato "N | texto". Informe
   o número exato da linha e copie o trecho exatamente como está nessa linha
   (sem o "N | ").
4. Quando o problema for uma seção ausente, use a linha do título da HU
   ("## HU-..."), deixe o trecho vazio e informe em "secao" o nome da seção que
   falta.
5. Escreva "mensagem" e "correcao" em português, em linguagem simples, para
   quem não é especialista. A correção deve ser concreta e específica para
   aquele trecho, não génerica ensinando como corrigir o erro encontrado e dando exemplos.
6. Se não houver problemas, devolva a lista de achados vazia. Não aponte
   problemas duvidosos só para ter o que responder.
7. Se não souber como responder, devolva a lista de achados vazia. Não invente respostas.
"""

ESQUEMA_RESPOSTA = {
    "type": "object",
    "properties": {
        "achados": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "regra": {"type": "string"},
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

def formatar_regras(regras: list[dict]) -> str:
    blocos = []
    for regra in regras:
        parametros = yaml.safe_dump(regra.get("parametros", {}),
                                    allow_unicode=True, sort_keys=False).strip()
        blocos.append(
            f"- id: {regra['id']}\n"
            f"  tipo: {regra.get('tipo')}\n"
            f"  categoria: {regra.get('categoria')}\n"
            f"  parametros:\n    " + parametros.replace("\n", "\n    ") + "\n"
            f"  mensagem modelo: {regra.get('mensagem')}\n"
            f"  correcao modelo: {regra.get('correcao')}"
        )
    return "\n".join(blocos)

def formatar_documento(documento: dict) -> str:
    """Numera as linhas do documento (a numeração começa em 1)."""
    return "\n".join(f"{numero} | {linha}"
                     for numero, linha in enumerate(documento["linhas"], start=1))

def montar_mensagens(regras: list[dict], documento: dict) -> list[dict]:
    """Monta a conversa enviada à LLM: instruções (system) + contexto (user).

    Ponto de extensão futuro: incluir aqui os arquivos .md do brain/
    (base de conhecimento) como contexto adicional.
    """
    conteudo = (
        "## Regras\n\n"
        f"{formatar_regras(regras)}\n\n"
        f"## Documento: {documento['caminho']}\n\n"
        f"{formatar_documento(documento)}\n\n"
        "## Formato da resposta\n\n"
        "Responda apenas com um JSON neste formato (JSON Schema):\n"
        f"{json.dumps(ESQUEMA_RESPOSTA, ensure_ascii=False)}"
    )
    return [
        {"role": "system", "content": INSTRUCOES},
        {"role": "user", "content": conteudo},
    ]