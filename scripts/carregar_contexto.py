import argparse
import re
import sys
from pathlib import Path
import yaml

REGRAS = "brain/regras-teste.yml"
REQUISITOS = "docs/requisitos"
ARQUIVOS_IGNORADOS = {"README.md"}
# Estrutura esperada do documento: "## HU-NN" abre uma HU e "### Nome" abre uma seção.
PADRAO_HU = re.compile(r"^##\s+(HU-\d+)\b")
PADRAO_SECAO = re.compile(r"^###\s+(.+?)\s*$")
PADRAO_TITULO = re.compile(r"^#{1,6}\s")

def carregar_regras(caminho: Path) -> list[dict]:
    with caminho.open(encoding="utf-8") as arquivo:
        dados = yaml.safe_load(arquivo)

    if not isinstance(dados, dict) or not isinstance(dados.get("regras"), list):
        raise ValueError(f"{caminho}: o arquivo deve ter uma chave 'regras' com uma lista.")

    return dados["regras"]

def carregar_documentos(pasta: Path) -> list[dict]:
    if not pasta.is_dir():
        raise NotADirectoryError(f"{pasta}: pasta de requisitos não encontrada.")

    documentos = []
    for arquivo in sorted(pasta.rglob("*.md")):
        if arquivo.name in ARQUIVOS_IGNORADOS:
            continue
        texto = arquivo.read_text(encoding="utf-8")
        documentos.append({
            "caminho": arquivo.as_posix(),
            "linhas": texto.splitlines(),
        })

    return documentos

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

def ler_argumentos() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Carrega regras e documentos de requisitos.")
    parser.add_argument("--regras", default=REGRAS,
                        help=f"arquivo YAML de regras (padrão: {REGRAS})")
    parser.add_argument("--requisitos", default=REQUISITOS,
                        help=f"pasta com os .md de requisitos (padrão: {REQUISITOS})")
    return parser.parse_args()

def main() -> int:
    args = ler_argumentos()

    try:
        regras = carregar_regras(Path(args.regras))
        documentos = carregar_documentos(Path(args.requisitos))
    except (OSError, ValueError, yaml.YAMLError) as erro:
        print(f"Erro ao carregar o contexto: {erro}", file=sys.stderr)
        return 1

    print(f"== Regras ({len(regras)}) — {args.regras}")
    for regra in regras:
        print(f"- {regra.get('id')}: tipo={regra.get('tipo')}, "
              f"categoria={regra.get('categoria')}, severidade={regra.get('severidade')}")

    print(f"\n== Documentos ({len(documentos)}) — {args.requisitos}")
    for documento in documentos:
        print(f"\n--- {documento['caminho']} ({len(documento['linhas'])} linhas)")
        for numero, linha in enumerate(documento["linhas"], start=1):
            print(f"{numero:4} | {linha}")

    return 0

if __name__ == "__main__":
    sys.exit(main())
