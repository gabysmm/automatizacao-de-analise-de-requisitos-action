import argparse
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path
import yaml
from dotenv import load_dotenv
from openai import OpenAI, OpenAIError
from analisar_documentos import separar_hus
from carregar_contexto import REGRAS, REQUISITOS, carregar_documentos, carregar_regras
from prompt import ESQUEMA_RESPOSTA, VERSAO_PROMPT, montar_mensagens

MODELO_PADRAO = "openai/gpt-oss-120b"
URL_BASE_PADRAO = "https://api.groq.com/openai/v1"
CAMPOS_TEXTO = ("regra", "hu", "secao", "trecho", "mensagem", "correcao")

def chamar_llm(cliente: OpenAI, modelo: str, mensagens: list[dict]) -> dict:
    resposta = cliente.chat.completions.create(
        model=modelo,
        messages=mensagens,
        temperature=0,
        response_format={
            "type": "json_schema",
            "json_schema": {"name": "achados", "schema": ESQUEMA_RESPOSTA},
        },
    )
    texto = resposta.choices[0].message.content or ""
    texto = re.sub(r"^\s*```(?:json)?\s*|\s*```\s*$", "", texto)
    return json.loads(texto)


def validar_achados(resposta: dict, regras: list[dict], documento: dict) -> list[dict]:
    regras_por_id = {regra["id"]: regra for regra in regras}
    hus_existentes = {hu["id"] for hu in separar_hus(documento)}
    linhas = documento["linhas"]
    achados = []
    itens = resposta.get("achados") if isinstance(resposta, dict) else None
    if not isinstance(itens, list):
        raise ValueError("a resposta da LLM não tem uma lista 'achados'.")
    for item in itens:
        motivo = None
        if not isinstance(item, dict) or not all(
                isinstance(item.get(c), str) for c in CAMPOS_TEXTO):
            motivo = "campos ausentes ou com tipo errado"
        elif item["regra"] not in regras_por_id:
            motivo = f"regra '{item['regra']}' não existe"
        elif item["hu"] not in hus_existentes:
            motivo = f"HU '{item['hu']}' não existe no documento"
        elif not isinstance(item.get("linha"), int) or not 1 <= item["linha"] <= len(linhas):
            motivo = f"linha {item.get('linha')!r} fora do documento"
        elif item["trecho"].strip() and \
                " ".join(item["trecho"].split()) not in " ".join(linhas[item["linha"] - 1].split()):
            motivo = f"trecho não encontrado na linha {item['linha']}"
        if motivo:
            print(f"Aviso: achado descartado em {documento['caminho']} ({motivo}): "
                  f"{json.dumps(item, ensure_ascii=False)}", file=sys.stderr)
            continue

        regra = regras_por_id[item["regra"]]
        achados.append({
            "id": None,
            "regra": regra["id"],
            "categoria": regra["categoria"],    # vem da regra, não da LLM
            "severidade": regra["severidade"],  # vem da regra, não da LLM
            "documento": documento["caminho"],
            "hu": item["hu"],
            "secao": item["secao"],
            "linha": item["linha"],
            "trecho": item["trecho"].strip(),
            "mensagem": item["mensagem"],
            "correcao": item["correcao"],
        })
    return achados

def analisar(cliente: OpenAI, modelo: str, regras: list[dict],
             documentos: list[dict]) -> list[dict]:
    achados = []
    for documento in documentos:
        print(f"Analisando {documento['caminho']} com {modelo}...", file=sys.stderr)
        resposta = chamar_llm(cliente, modelo, montar_mensagens(regras, documento))
        achados.extend(validar_achados(resposta, regras, documento))

    achados.sort(key=lambda a: (a["documento"], a["linha"], a["regra"]))
    for numero, achado in enumerate(achados, start=1):
        achado["id"] = f"A-{numero:03d}"
    return achados

def ler_argumentos() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Analisa requisitos usando uma LLM.")
    parser.add_argument("--regras", default=REGRAS,
                        help=f"arquivo YAML de regras (padrão: {REGRAS})")
    parser.add_argument("--requisitos", default=REQUISITOS,
                        help=f"pasta com os .md de requisitos (padrão: {REQUISITOS})")
    parser.add_argument("--saida",
                        help="arquivo JSON de saída; se omitido, imprime na tela")
    return parser.parse_args()

def main() -> int:
    args = ler_argumentos()
    load_dotenv(override=False)
    chave = os.environ.get("LLM_API_KEY")
    if not chave:
        print("Erro: defina a variável de ambiente LLM_API_KEY.", file=sys.stderr)
        return 1
    modelo = os.environ.get("LLM_MODELO") or MODELO_PADRAO
    url_base = os.environ.get("LLM_URL_BASE") or URL_BASE_PADRAO
    cliente = OpenAI(api_key=chave, base_url=url_base, max_retries=3)

    try:
        regras = carregar_regras(Path(args.regras))
        documentos = carregar_documentos(Path(args.requisitos))
        achados = analisar(cliente, modelo, regras, documentos)
    except (OSError, ValueError, KeyError, yaml.YAMLError, OpenAIError) as erro:
        print(f"Erro na análise: {erro}", file=sys.stderr)
        return 1

    resultado = {
        "execucao": {
            "metodo": "llm",
            "data": datetime.now().astimezone().isoformat(timespec="seconds"),
            "modelo": modelo,
            "versao_prompt": VERSAO_PROMPT,
        },
        "achados": achados,
    }
    texto = json.dumps(resultado, ensure_ascii=False, indent=2)

    if args.saida:
        caminho = Path(args.saida)
        caminho.parent.mkdir(parents=True, exist_ok=True)
        caminho.write_text(texto + "\n", encoding="utf-8")
        print(f"{len(achados)} achado(s) gravado(s) em {caminho}", file=sys.stderr)
    else:
        print(texto)

    return 0

if __name__ == "__main__":
    sys.exit(main())
