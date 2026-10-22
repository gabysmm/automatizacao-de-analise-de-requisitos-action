import argparse
import json
import sys
from pathlib import Path
from gerar_relatorio import SEVERIDADES, carregar_resultado, nome_exibicao

SEVERIDADES_SEM_FALHA = {"baixa"}

def ler_argumentos() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Falha (código 1) se houver achados de severidade média, alta ou crítica.")
    parser.add_argument("entrada", help="arquivo JSON gerado por analisar_documentos.py")
    return parser.parse_args()

def achados_que_falham(achados: list[dict]) -> list[dict]:
    return [a for a in achados if a.get("severidade") not in SEVERIDADES_SEM_FALHA]

def anotar_no_github(achado: dict) -> None:
    # "::error ...::" é um comando do GitHub Actions: vira uma anotação na página da
    # execução, apontando para o arquivo e a linha. Fora do Actions é só texto no terminal.
    severidade = nome_exibicao(achado.get("severidade"), SEVERIDADES)
    print(f"::error file={achado.get('documento')},line={achado.get('linha')},"
          f"title={achado.get('regra')} ({severidade})::{achado.get('mensagem')}")

def main() -> int:
    args = ler_argumentos()

    try:
        resultado = carregar_resultado(Path(args.entrada))
    except (OSError, ValueError, json.JSONDecodeError) as erro:
        print(f"Erro ao verificar os achados: {erro}", file=sys.stderr)
        return 1
    erros = resultado.get("erros") or []
    for erro in erros:
        print(f"::error file={erro.get('documento')},title=Arquivo não analisado::{erro.get('motivo')}")
    if erros:
        print(f"❌ {len(erros)} arquivo(s) não puderam ser analisados. Veja o relatório.")

    falhas = achados_que_falham(resultado["achados"])
    if not falhas and not erros:
        print("✅ Nenhum achado de severidade média, alta ou crítica.")
        return 0

    for achado in falhas:
        anotar_no_github(achado)
    if falhas:
        print(f"{len(falhas)} achado(s) de severidade média, alta ou crítica. "
              "Corrija os requisitos apontados no relatório.")
    return 1

if __name__ == "__main__":
    sys.exit(main())
