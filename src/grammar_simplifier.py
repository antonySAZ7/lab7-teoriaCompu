import argparse
import re
import sys
from itertools import product
from pathlib import Path


EPSILON_SYMBOLS = {"epsilon", "eps", "ε"}
EPSILON_OUTPUT = "epsilon"
PRODUCTION_PATTERN = re.compile(
    r"^\s*([A-Z])\s*(?:->|→)\s*(.+?)\s*$"
)
BODY_PATTERN = re.compile(r"^(?:[A-Za-z0-9]+|epsilon|eps|e|ε)$")

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


class GrammarError(ValueError):
    pass


def normalize_body(body):
    body = body.strip()
    return "ε" if body in EPSILON_SYMBOLS else body


def validate_body(body, line_number):
    normalized = normalize_body(body)
    if not normalized:
        raise GrammarError(
            f"Linea {line_number}: hay una produccion vacia. Use epsilon."
        )
    if not BODY_PATTERN.fullmatch(body.strip()):
        raise GrammarError(
            f"Linea {line_number}: cuerpo invalido '{body.strip()}'. "
            "Use simbolos alfanumericos o epsilon."
        )
    return normalized


def parse_grammar(path):
    productions = {}
    start_symbol = None

    for line_number, raw_line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        raw_line = raw_line.lstrip("\ufeff")
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue

        match = PRODUCTION_PATTERN.fullmatch(line)
        if not match:
            raise GrammarError(
                f"Linea {line_number}: produccion mal escrita: '{raw_line}'. "
                "Formato esperado: A -> aB | epsilon"
            )

        head, body_text = match.groups()
        if start_symbol is None:
            start_symbol = head

        alternatives = [validate_body(part, line_number) for part in body_text.split("|")]
        productions.setdefault(head, set()).update(alternatives)

    if not productions:
        raise GrammarError("El archivo no contiene producciones validas.")

    return start_symbol, productions


def nullable_symbols(productions):
    nullable = set()
    changed = True

    while changed:
        changed = False
        for head, bodies in productions.items():
            if head in nullable:
                continue

            for body in bodies:
                if body == "ε" or all(symbol in nullable for symbol in body):
                    nullable.add(head)
                    changed = True
                    break

    return nullable


def epsilon_free_variants(body, nullable):
    if body == "ε":
        return set()

    nullable_positions = [
        index for index, symbol in enumerate(body) if symbol in nullable
    ]
    variants = set()

    for mask in product([False, True], repeat=len(nullable_positions)):
        removed = set(
            position
            for position, should_remove in zip(nullable_positions, mask)
            if should_remove
        )
        candidate = "".join(
            symbol for index, symbol in enumerate(body) if index not in removed
        )
        if candidate:
            variants.add(candidate)

    return variants


def remove_epsilon_productions(start_symbol, productions):
    nullable = nullable_symbols(productions)
    simplified = {head: set() for head in productions}
    steps = []

    for head, bodies in productions.items():
        for body in sorted(bodies):
            if body == "ε":
                steps.append((head, body, []))
                continue

            variants = epsilon_free_variants(body, nullable)
            simplified[head].update(variants)
            steps.append((head, body, sorted(variants)))

    if start_symbol in nullable:
        new_start = "S0"
        while new_start in simplified:
            new_start += "0"
        simplified = {new_start: {start_symbol, "ε"}, **simplified}
        start_symbol = new_start

    return start_symbol, simplified, nullable, steps


def format_productions(productions):
    lines = []
    for head in sorted(productions):
        bodies = sorted(productions[head], key=lambda value: (value == "ε", value))
        printable = [EPSILON_OUTPUT if body == "ε" else body for body in bodies]
        lines.append(f"{head} -> {' | '.join(printable)}")
    return "\n".join(lines)


def print_analysis(path, start_symbol, productions, simplified_start, simplified, nullable, steps):
    print(f"\nArchivo: {path}")
    print("\nGramatica original:")
    print(format_productions(productions))

    print("\n1. Simbolos anulables encontrados:")
    if nullable:
        print(", ".join(sorted(nullable)))
    else:
        print("No hay simbolos anulables.")

    print("\n2. Construccion de nuevas producciones:")
    for head, body, variants in steps:
        if body == "ε":
            print(f"   {head} -> {EPSILON_OUTPUT} se elimina directamente.")
            continue

        nullable_count = sum(1 for symbol in body if symbol in nullable)
        total_cases = 2 ** nullable_count
        generated = " | ".join(variants) if variants else "ninguna"
        print(
            f"   {head} -> {body}: {nullable_count} anulables, "
            f"{total_cases} casos posibles => {generated}"
        )

    if simplified_start != start_symbol:
        print(
            "\n3. El simbolo inicial era anulable, por eso se agrego "
            f"{simplified_start} -> {start_symbol} | {EPSILON_OUTPUT}."
        )
    else:
        print("\n3. No fue necesario agregar un nuevo simbolo inicial.")

    print("\nGramatica sin producciones epsilon:")
    print(format_productions(simplified))


def main():
    parser = argparse.ArgumentParser(
        description="Elimina producciones epsilon de una gramatica libre de contexto."
    )
    parser.add_argument(
        "files",
        nargs="+",
        type=Path,
        help="Archivos de texto con producciones, por ejemplo grammars/gramatica1.txt",
    )
    args = parser.parse_args()

    for grammar_file in args.files:
        if not grammar_file.exists():
            raise GrammarError(f"No existe el archivo: {grammar_file}")

        start_symbol, productions = parse_grammar(grammar_file)
        simplified_start, simplified, nullable, steps = remove_epsilon_productions(
            start_symbol, productions
        )
        print_analysis(
            grammar_file,
            start_symbol,
            productions,
            simplified_start,
            simplified,
            nullable,
            steps,
        )


if __name__ == "__main__":
    try:
        main()
    except GrammarError as error:
        print(f"\nERROR: {error}")
        raise SystemExit(1)
