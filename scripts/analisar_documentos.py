import argparse
import json
import re
import sys
import unicodedata
from datetime import datetime
from pathlib import Path
import yaml
from carregar_contexto import (REGRAS, REQUISITOS, carregar_documentos, carregar_regras)

PADRAO_HU = re.compile(r"^##\s+(HU-\d+)\b")
PADRAO_SECAO = re.compile(r"^###\s+(.+?)\s*$")
PADRAO_TITULO = re.compile(r"^#{1,6}\s")
PADRAO_PALAVRA = re.compile(r"\w+")

def normalizar(texto: str) -> str:
    decomposto = unicodedata.normalize("NFD", texto.casefold())
    return "".join(c for c in decomposto if unicodedata.category(c) != "Mn")

def gerar_variacoes(termo: str) -> set[str]:
    t = normalizar(termo)
    variacoes = {t}
    if t.endswith("o") or t.endswith("a"):
        radical = t[:-1]
        variacoes |= {radical + "o", radical + "a", radical + "os", radical + "as"}
    elif t.endswith("il"):
        variacoes.add(t[:-2] + "eis")          # facil -> faceis
    elif t.endswith(("al", "el", "ol", "ul")):
        variacoes.add(t[:-1] + "is")           # normal -> normais
    elif t.endswith(("r", "z")):
        variacoes.add(t + "es")                # simples ja termina em s
    elif t.endswith("m"):
        variacoes.add(t[:-1] + "ns")
    elif not t.endswith("s"):
        variacoes.add(t + "s")                 # eficiente -> eficientes
    return variacoes

def separar_hus(documento: dict) -> list[dict]:
    hus = []
    hu_atual = None
    secao_atual = None

    for numero, linha in enumerate(documento["linhas"], start=1):
        encontrou_hu = PADRAO_HU.match(linha)
        if encontrou_hu:
            hu_atual = {"id": encontrou_hu.group(1), "linha": numero, "secoes": []}
            hus.append(hu_atual)
            secao_atual = None
            continue

        encontrou_secao = PADRAO_SECAO.match(linha)
        if encontrou_secao and hu_atual is not None:
            secao_atual = {"nome": encontrou_secao.group(1), "linha": numero, "conteudo": []}
            hu_atual["secoes"].append(secao_atual)
            continue

        if PADRAO_TITULO.match(linha):
            secao_atual = None
            continue

        if secao_atual is not None and linha.strip():
            secao_atual["conteudo"].append((numero, linha))

    return hus

def criar_achado(regra: dict, documento: dict, hu: dict, nome_secao: str,
                 linha: int, trecho: str, **marcadores) -> dict:
    """Monta um achado no formato do contrato"""
    return {
        "id": None,
        "regra": regra["id"],
        "categoria": regra["categoria"],
        "severidade": regra["severidade"],
        "documento": documento["caminho"],
        "hu": hu["id"],
        "secao": nome_secao,
        "linha": linha,
        "trecho": trecho,
        "mensagem": regra["mensagem"].format(**marcadores),
        "correcao": regra["correcao"],
    }

def regra_secao_obrigatoria(regra: dict, documento: dict, hus: list[dict]) -> list[dict]:
    parametros = regra["parametros"]
    if parametros.get("escopo", "hu") != "hu":
        raise ValueError(f"{regra['id']}: escopo '{parametros['escopo']}' não suportado.")

    achados = []
    for hu in hus:
        secoes_da_hu = {normalizar(s["nome"]) for s in hu["secoes"]}
        for secao_exigida in parametros["secoes"]:
            if normalizar(secao_exigida) not in secoes_da_hu:
                achados.append(criar_achado(
                    regra, documento, hu, secao_exigida, hu["linha"], "",
                    secao=secao_exigida,
                ))
    return achados


def regra_termos_ambiguos(regra: dict, documento: dict, hus: list[dict]) -> list[dict]:
    formas = {}
    for termo in regra["parametros"]["termos"]:
        for variacao in gerar_variacoes(termo):
            formas[variacao] = termo

    achados = []
    for hu in hus:
        for secao in hu["secoes"]:
            for numero, linha in secao["conteudo"]:
                for palavra in PADRAO_PALAVRA.findall(linha):
                    if normalizar(palavra) in formas:
                        achados.append(criar_achado(
                            regra, documento, hu, secao["nome"], numero,
                            trecho=linha.strip(),
                            termo=palavra,    
                        ))
    return achados

REGRAS_IMPLEMENTADAS = {
    "secao_obrigatoria": regra_secao_obrigatoria,
    "termos_ambiguos": regra_termos_ambiguos,
}

def analisar(regras: list[dict], documentos: list[dict]) -> list[dict]:
    achados = []
    for documento in documentos:
        hus = separar_hus(documento)
        for regra in regras:
            funcao = REGRAS_IMPLEMENTADAS.get(regra.get("tipo"))
            if funcao is None:
                print(f"Aviso: regra {regra.get('id')} com tipo '{regra.get('tipo')}' "
                      "não implementado; ignorada.", file=sys.stderr)
                continue
            achados.extend(funcao(regra, documento, hus))

    achados.sort(key=lambda a: (a["documento"], a["linha"], a["regra"]))
    for numero, achado in enumerate(achados, start=1):
        achado["id"] = f"A-{numero:03d}"
    return achados

def ler_argumentos() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Analisa requisitos aplicando as regras.")
    parser.add_argument("--regras", default=REGRAS,
                        help=f"arquivo YAML de regras (padrão: {REGRAS})")
    parser.add_argument("--requisitos", default=REQUISITOS,
                        help=f"pasta com os .md de requisitos (padrão: {REQUISITOS})")
    parser.add_argument("--saida",
                        help="arquivo JSON de saída; se omitido, imprime na tela")
    return parser.parse_args()

def main() -> int:
    args = ler_argumentos()

    try:
        regras = carregar_regras(Path(args.regras))
        documentos = carregar_documentos(Path(args.requisitos))
        achados = analisar(regras, documentos)
    except (OSError, ValueError, KeyError, yaml.YAMLError) as erro:
        print(f"Erro na análise: {erro}", file=sys.stderr)
        return 1

    resultado = {
        "execucao": {
            "metodo": "regras",
            "data": datetime.now().astimezone().isoformat(timespec="seconds"),
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
