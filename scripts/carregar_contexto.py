import argparse
import hashlib
import re
import sys
from pathlib import Path
import yaml

REGRAS = "brain/regras-teste.yml"
BASE = "brain"
REQUISITOS = "docs/requisitos"
ARQUIVOS_IGNORADOS = {"README.md"}

ORDEM_BASE = (
    "historias-de-usuario.md",
    "ambiguidade.md",
    "lacunas.md",
    "inconsistencias.md",
    "armadilhas.md",
)
SEVERIDADES_VALIDAS = {"critica", "alta", "media", "baixa"}
PADRAO_CABECALHO = re.compile(r"\A---[ \t]*\n(.*?)\n---[ \t]*\n", re.DOTALL)
PADRAO_TITULO_REGRA = re.compile(r"^##\s+([A-Z]{3}-\d{2})\s+—\s+(.+?)\s*$", re.MULTILINE)

PADRAO_HU = re.compile(r"^##\s+(HU-\d+)\b")
PADRAO_SECAO = re.compile(r"^###\s+(.+?)\s*$")
PADRAO_TITULO = re.compile(r"^#{1,6}\s")

def carregar_regras(caminho: Path) -> list[dict]:
    with caminho.open(encoding="utf-8") as arquivo:
        dados = yaml.safe_load(arquivo)

    if not isinstance(dados, dict) or not isinstance(dados.get("regras"), list):
        raise ValueError(f"{caminho}: o arquivo deve ter uma chave 'regras' com uma lista.")

    return dados["regras"]

def separar_cabecalho(texto: str, caminho: Path) -> tuple[dict, str]:
    encontrou = PADRAO_CABECALHO.match(texto)
    if not encontrou:
        raise ValueError(f"{caminho}: o arquivo deve começar com um cabeçalho entre '---'.")
    cabecalho = yaml.safe_load(encontrou.group(1)) or {}
    if not isinstance(cabecalho, dict):
        raise ValueError(f"{caminho}: o cabeçalho deve ser um mapa YAML.")
    return cabecalho, texto[encontrou.end():].strip()

def carregar_base(pasta: Path) -> dict:
    partes, regras, versoes = [], [], {}
    conteudo_bruto = []
    for nome in ORDEM_BASE:
        caminho = pasta / nome
        texto = caminho.read_text(encoding="utf-8")
        conteudo_bruto.append(texto)
        cabecalho, corpo = separar_cabecalho(texto, caminho)

        regras_cabecalho = cabecalho.get("regras") or {}
        titulos = dict(PADRAO_TITULO_REGRA.findall(corpo))
        if set(regras_cabecalho) != set(titulos):
            raise ValueError(
                f"{caminho}: as regras do cabeçalho {sorted(regras_cabecalho)} não batem "
                f"com os títulos '## ID — nome' do texto {sorted(titulos)}.")
        if regras_cabecalho and not cabecalho.get("categoria"):
            raise ValueError(f"{caminho}: arquivo com regras precisa de 'categoria' no cabeçalho.")

        for id_regra, configuracao in regras_cabecalho.items():
            severidade = (configuracao or {}).get("severidade")
            if severidade not in SEVERIDADES_VALIDAS:
                raise ValueError(f"{caminho}: severidade inválida em {id_regra}: {severidade!r}.")
            regras.append({
                "id": id_regra,
                "nome": titulos[id_regra],
                "categoria": cabecalho["categoria"],
                "severidade": severidade,
            })
        versoes[nome] = str(cabecalho.get("versao", "?"))
        partes.append(corpo)

    ids = [regra["id"] for regra in regras]
    if len(ids) != len(set(ids)):
        raise ValueError(f"{pasta}: há IDs de regra repetidos na base.")

    hash_base = hashlib.sha256("\n".join(conteudo_bruto).encode("utf-8")).hexdigest()[:12]
    return {
        "texto": "\n\n".join(partes),
        "regras": regras,
        "versao": {"arquivos": versoes, "hash": hash_base},
    }

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
    parser.add_argument("--base",
                        help="mostra só o catálogo e o tamanho da base de conhecimento "
                             f"desta pasta (ex.: {BASE})")
    return parser.parse_args()

def mostrar_base(pasta: Path) -> int:
    try:
        base = carregar_base(pasta)
    except (OSError, ValueError, yaml.YAMLError) as erro:
        print(f"Erro ao carregar a base: {erro}", file=sys.stderr)
        return 1
    print(f"== Base de conhecimento — {pasta} (hash {base['versao']['hash']})")
    for nome, versao in base["versao"]["arquivos"].items():
        print(f"- {nome} (versão {versao})")
    print(f"\n== Regras ({len(base['regras'])})")
    for regra in base["regras"]:
        print(f"- {regra['id']} — {regra['nome']} "
              f"[{regra['categoria']}, {regra['severidade']}]")
    print(f"\nTexto enviado à LLM: {len(base['texto'])} caracteres "
          f"(~{len(base['texto']) // 4} tokens, estimativa grosseira)")
    return 0

def main() -> int:
    args = ler_argumentos()
    if args.base:
        return mostrar_base(Path(args.base))

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
