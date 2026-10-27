import argparse
import json
import os
import re
import sys
import time
from datetime import datetime
from pathlib import Path
import yaml
from dotenv import load_dotenv
from openai import APIStatusError, OpenAI, OpenAIError
from carregar_contexto import BASE, REQUISITOS, carregar_base, carregar_documentos
from prompt import VERSAO_PROMPT, montar_esquema, montar_mensagens

MODELO_PADRAO = "gemini-3.8-flash"
URL_BASE_PADRAO = "https://generativelanguage.googleapis.com/v1beta/openai/"
LIMITE_TOKENS_MINUTO = int(os.environ["LLM_LIMITE_TPM"]) if os.environ.get("LLM_LIMITE_TPM") else None
CAMPOS_TEXTO = ("regra", "hu", "secao", "trecho", "mensagem", "correcao")
PADRAO_MARCADOR = re.compile(r"^(?:[-*•]|\d+[.)])\s+")
TENTATIVAS = 6
ESTIMATIVA_INICIAL = 6000

def contar_tokens(uso) -> dict:
    if uso is None:
        return {"entrada": 0, "saida": 0, "cache": 0}
    detalhes = getattr(uso, "prompt_tokens_details", None)
    cache = getattr(detalhes, "cached_tokens", None) if detalhes else None
    return {
        "entrada": uso.prompt_tokens or 0,
        "saida": uso.completion_tokens or 0,
        "cache": cache or 0,
    }

def chamar_llm(cliente: OpenAI, modelo: str, mensagens: list[dict],
               esquema: dict) -> tuple[dict, dict]:
    resposta = cliente.chat.completions.create(
        model=modelo,
        messages=mensagens,
        response_format={
            "type": "json_schema",
            "json_schema": {"name": "achados", "schema": esquema},
        },
    )
    texto = resposta.choices[0].message.content or ""
    texto = re.sub(r"^\s*```(?:json)?\s*|\s*```\s*$", "", texto)
    return json.loads(texto), contar_tokens(resposta.usage)

def hu_aparece_no_documento(hu: str, texto: str) -> bool:
    padrao = rf"(?<![\w-]){re.escape(hu)}(?![\w-])"
    return re.search(padrao, texto) is not None

def avisar_descarte(documento: dict, item, motivo: str) -> None:
    print(f"Aviso: achado descartado em {documento['caminho']} ({motivo}): "
          f"{json.dumps(item, ensure_ascii=False)}", file=sys.stderr)
    if os.environ.get("GITHUB_ACTIONS") == "true":
        linha = item.get("linha") if isinstance(item, dict) else None
        local = f"file={documento['caminho']}"
        if isinstance(linha, int) and 1 <= linha <= len(documento["linhas"]):
            local += f",line={linha}"
        print(f"::warning {local},title=Achado descartado pela validação::"
              f"A IA apontou um problema que não pôde ser confirmado no documento ({motivo}). "
              "Revise este trecho manualmente.")

def trecho_na_linha(trecho: str, linha: str) -> str | None:
    trecho_normal = " ".join(trecho.split())
    linha_normal = " ".join(linha.split())
    if trecho_normal in linha_normal:
        return trecho.strip()
    sem_marcador = PADRAO_MARCADOR.sub("", trecho_normal, count=1)
    if sem_marcador and sem_marcador != trecho_normal and sem_marcador in linha_normal:
        return sem_marcador
    return None

def explicar_erro(erro: Exception) -> str:
    status = erro.status_code if isinstance(erro, APIStatusError) else None
    if status == 413:
        return ("Arquivo grande demais para o limite gratuito do provedor da IA. "
                "Divida as HUs em arquivos menores (até 5 ou 6 HUs por arquivo).")
    if status == 429:
        return ("Limite de uso do provedor da IA atingido (por minuto ou por dia), "
                "mesmo após novas tentativas. Rode a análise de novo mais tarde.")
    if status in (401, 403) or (status == 400 and "API key" in str(erro)):
        return ("A chave da IA (LLM_API_KEY) foi recusada. Confira se o secret do "
                "repositório tem uma chave do Gemini (Google AI Studio).")
    return f"Não foi possível analisar este arquivo ({type(erro).__name__}: {erro})."

def avisar_erro(documento: dict, motivo: str) -> None:
    print(f"Erro: {documento['caminho']} não foi analisado: {motivo}", file=sys.stderr)
    if os.environ.get("GITHUB_ACTIONS") == "true":
        print(f"::error file={documento['caminho']},title=Arquivo não analisado::{motivo}")

def validar_achados(resposta: dict, regras: list[dict],
                    documento: dict) -> tuple[list[dict], list[dict]]:
    regras_por_id = {regra["id"]: regra for regra in regras}
    linhas = documento["linhas"]
    texto_documento = "\n".join(linhas)
    achados, descartados = [], []
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
        elif item["hu"].strip() and not hu_aparece_no_documento(item["hu"].strip(), texto_documento):
            motivo = f"HU '{item['hu']}' não aparece no documento"
        elif not isinstance(item.get("linha"), int) or not 1 <= item["linha"] <= len(linhas):
            motivo = f"linha {item.get('linha')!r} fora do documento"
        elif item["trecho"].strip() and \
                trecho_na_linha(item["trecho"], linhas[item["linha"] - 1]) is None:
            motivo = f"trecho não encontrado na linha {item['linha']}"
        if motivo:
            avisar_descarte(documento, item, motivo)
            descartados.append({"documento": documento["caminho"], "motivo": motivo, "achado": item})
            continue

        regra = regras_por_id[item["regra"]]
        achados.append({
            "id": None,
            "regra": regra["id"],
            "nome_regra": regra.get("nome", ""),  # vem da base, não da LLM
            "categoria": regra["categoria"],    # vem da regra, não da LLM
            "severidade": regra["severidade"],  # vem da regra, não da LLM
            "documento": documento["caminho"],
            "hu": item["hu"].strip(),
            "secao": item["secao"],
            "linha": item["linha"],
            "trecho": (trecho_na_linha(item["trecho"], linhas[item["linha"] - 1])
                       if item["trecho"].strip() else ""),
            "mensagem": item["mensagem"],
            "correcao": item["correcao"],
        })
    return achados, descartados

def esperar_limite(historico: list[tuple[float, int]], estimativa: int) -> None:
    if LIMITE_TOKENS_MINUTO is None:
        return
    while True:
        agora = time.monotonic()
        historico[:] = [(t, n) for t, n in historico if agora - t < 60]
        usados = sum(n for _, n in historico)
        if not historico or usados + estimativa <= LIMITE_TOKENS_MINUTO:
            return
        espera = 60 - (agora - historico[0][0]) + 1
        print(f"  aguardando {espera:.0f}s para respeitar o limite de tokens por minuto "
              f"({usados} usados no último minuto)...", file=sys.stderr)
        time.sleep(espera)

def analisar(cliente: OpenAI, modelo: str, base: dict,
             documentos: list[dict]) -> tuple[list[dict], list[dict], list[dict], dict]:
    achados, descartados, erros = [], [], []
    tokens = {"entrada": 0, "saida": 0, "cache": 0}
    esquema = montar_esquema(base["regras"])
    historico, estimativa = [], ESTIMATIVA_INICIAL
    for documento in documentos:
        esperar_limite(historico, estimativa)
        print(f"Analisando {documento['caminho']} com {modelo}...", file=sys.stderr)
        # Um arquivo com erro não interrompe a análise dos outros.
        try:
            resposta, uso = chamar_llm(cliente, modelo, montar_mensagens(base, documento), esquema)
            print(f"  tokens: entrada={uso['entrada']} (cache={uso['cache']}), "
                  f"saída={uso['saida']}", file=sys.stderr)
            for chave in tokens:
                tokens[chave] += uso[chave]
            gasto = uso["entrada"] - uso["cache"] + uso["saida"]  # cache não conta no limite
            historico.append((time.monotonic(), gasto))
            estimativa = max(gasto, 1000)
            aceitos, rejeitados = validar_achados(resposta, base["regras"], documento)
        except (OpenAIError, ValueError) as erro:
            motivo = explicar_erro(erro)
            avisar_erro(documento, motivo)
            erros.append({"documento": documento["caminho"], "motivo": motivo})
            continue
        achados.extend(aceitos)
        descartados.extend(rejeitados)

    achados.sort(key=lambda a: (a["documento"], a["linha"], a["regra"]))
    for numero, achado in enumerate(achados, start=1):
        achado["id"] = f"A-{numero:03d}"
    return achados, descartados, erros, tokens

def ler_argumentos() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Analisa requisitos usando uma LLM.")
    parser.add_argument("--base", default=BASE,
                        help=f"pasta da base de conhecimento (padrão: {BASE})")
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
    cliente = OpenAI(api_key=chave, base_url=url_base, max_retries=TENTATIVAS)

    try:
        base = carregar_base(Path(args.base))
        documentos = carregar_documentos(Path(args.requisitos))
        achados, descartados, erros, tokens = analisar(cliente, modelo, base, documentos)
    except (OSError, ValueError, KeyError, yaml.YAMLError, OpenAIError) as erro:
        print(f"Erro na análise: {erro}", file=sys.stderr)
        return 1

    resultado = {
        "execucao": {
            "metodo": "llm",
            "data": datetime.now().astimezone().isoformat(timespec="seconds"),
            "modelo": modelo,
            "versao_prompt": VERSAO_PROMPT,
            "versao_base": base["versao"],
            "tokens": tokens,
        },
        "achados": achados,
        "descartados": descartados,
        "erros": erros,
    }
    texto = json.dumps(resultado, ensure_ascii=False, indent=2)

    if args.saida:
        caminho = Path(args.saida)
        caminho.parent.mkdir(parents=True, exist_ok=True)
        caminho.write_text(texto + "\n", encoding="utf-8")
        print(f"{len(achados)} achado(s) gravado(s) em {caminho}"
              f" ({len(descartados)} descartado(s) pela validação,"
              f" {len(erros)} arquivo(s) com erro)", file=sys.stderr)
    else:
        print(texto)

    return 0

if __name__ == "__main__":
    sys.exit(main())
