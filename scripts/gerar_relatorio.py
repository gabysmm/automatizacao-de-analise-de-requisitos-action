import argparse
import json
import os
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path

SEVERIDADES = {
    "critica": "crítica",
    "alta": "alta",
    "media": "média",
    "baixa": "baixa",
}

CATEGORIAS = {
    "ambiguidade": "ambiguidade",
    "lacuna": "lacuna",
    "inconsistencia": "inconsistência",
    "armadilha": "armadilha",
    "incompletude": "incompletude",
    "verificabilidade": "verificabilidade",
}

AVISO_IA = ("> **ATENÇÃO: Esta análise é feita por inteligência artificial e pode errar.** "
            "Ela pode apontar algo que não é um problema ou deixar passar um problema real. "
            "Leia cada apontamento e a orientação, e decida se faz sentido "
            "antes de mudar a sua história de usuário.")

def ler_argumentos() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Gera o relatório em Markdown a partir do JSON de achados.")
    parser.add_argument("entrada", help="arquivo JSON gerado por analisar_documentos.py")
    return parser.parse_args()

def carregar_resultado(caminho: Path) -> dict:
    with caminho.open(encoding="utf-8") as arquivo:
        resultado = json.load(arquivo)

    if not isinstance(resultado, dict) or "execucao" not in resultado \
            or not isinstance(resultado.get("achados"), list):
        raise ValueError(f"{caminho}: o JSON deve ter 'execucao' e uma lista 'achados'.")

    return resultado

def nome_exibicao(valor: str, nomes: dict) -> str:
    return nomes.get(valor, valor)

def ordenar_por(nomes: dict):
    posicoes = {valor: i for i, valor in enumerate(nomes)}
    return lambda valor: (posicoes.get(valor, len(posicoes)), str(valor))

def escapar(texto) -> str:
    if texto is None:
        return ""
    return str(texto).replace("|", "\\|").replace("\n", " ").strip()

def formatar_data(data_iso: str) -> str:
    try:
        return datetime.fromisoformat(data_iso).strftime("%d/%m/%Y %H:%M")
    except (TypeError, ValueError):
        return str(data_iso)

def montar_tabela_contagem(titulo: str, contagem: Counter, nomes: dict) -> list[str]:
    linhas = [f"| {titulo} | Qtd. |", "|---|---|"]
    for valor in sorted(contagem, key=ordenar_por(nomes)):
        linhas.append(f"| {nome_exibicao(valor, nomes)} | {contagem[valor]} |")
    return linhas

def montar_resumo(resultado: dict) -> str:
    execucao = resultado["execucao"]
    achados = resultado["achados"]
    descartados = resultado.get("descartados") or []
    erros = resultado.get("erros") or []

    cabecalho = f"**Método:** {execucao.get('metodo', '?')} · "
    if execucao.get("modelo"):
        cabecalho += f"**Modelo:** `{escapar(execucao['modelo'])}` · "
    linhas = [
        "## Relatório de análise de requisitos",
        "",
        cabecalho +
        f"**Data:** {formatar_data(execucao.get('data'))} · "
        f"**Achados:** {len(achados)}",
    ]
    if execucao.get("metodo") == "llm":
        linhas += ["", AVISO_IA]
    if erros:
        linhas += ["", f"❌ **{len(erros)} arquivo(s) não puderam ser analisados:**", ""]
        linhas += [f"- `{escapar(e.get('documento'))}`: {escapar(e.get('motivo'))}" for e in erros]
    if descartados:
        linhas += ["", f"⚠️ **{len(descartados)} achado(s) descartado(s) pela validação.** "
                       "A IA apontou problemas que não puderam ser confirmados no documento "
                       "(por exemplo, linha ou trecho inexistente). Veja os avisos na página "
                       "da execução e revise esses pontos manualmente."]
    if not achados:
        if descartados or erros:
            linhas += ["", "Nenhum achado foi confirmado."]
        else:
            linhas += ["", "✅ Nenhum problema encontrado."]
        return "\n".join(linhas)

    linhas.append("")
    linhas += montar_tabela_contagem("Severidade", Counter(a.get("severidade") for a in achados), SEVERIDADES)
    linhas.append("")
    linhas += montar_tabela_contagem("Categoria", Counter(a.get("categoria") for a in achados), CATEGORIAS)
    return "\n".join(linhas)

def agrupar_por_documento(achados: list[dict]) -> dict[str, list[dict]]:
    grupos = {}
    for achado in achados:
        grupos.setdefault(achado.get("documento", "?"), []).append(achado)
    return dict(sorted(grupos.items()))

def montar_secao_documento(documento: str, achados: list[dict]) -> str:
    linhas = [
        f"### 📄 `{documento}` ({len(achados)} achado{'s' if len(achados) != 1 else ''})",
        "",
        "| Linha | HU | Seção | Regra | Severidade | Problema | Sugestão |",
        "|---|---|---|---|---|---|---|",
    ]
    for achado in achados:
        regra = escapar(achado.get("regra"))
        if achado.get("nome_regra"):
            regra += f" — {escapar(achado['nome_regra'])}"
        linhas.append(
            f"| {escapar(achado.get('linha'))} "
            f"| {escapar(achado.get('hu')) or '—'} "
            f"| {escapar(achado.get('secao'))} "
            f"| {regra} "
            f"| {escapar(nome_exibicao(achado.get('severidade'), SEVERIDADES))} "
            f"| {escapar(achado.get('mensagem'))} "
            f"| {escapar(achado.get('correcao'))} |"
        )
    return "\n".join(linhas)

def gerar_relatorio(resultado: dict) -> str:
    partes = [montar_resumo(resultado)]
    for documento, achados in agrupar_por_documento(resultado["achados"]).items():
        partes.append(montar_secao_documento(documento, achados))
    return "\n\n".join(partes) + "\n"

def escrever_saidas(texto: str) -> None:
    print(texto)
    caminho_resumo = os.environ.get("GITHUB_STEP_SUMMARY")
    if caminho_resumo:
        with open(caminho_resumo, "a", encoding="utf-8") as arquivo:
            arquivo.write(texto)

def main() -> int:
    args = ler_argumentos()

    try:
        resultado = carregar_resultado(Path(args.entrada))
        texto = gerar_relatorio(resultado)
        escrever_saidas(texto)
    except (OSError, ValueError, json.JSONDecodeError) as erro:
        print(f"Erro ao gerar o relatório: {erro}", file=sys.stderr)
        return 1

    return 0

if __name__ == "__main__":
    sys.exit(main())
