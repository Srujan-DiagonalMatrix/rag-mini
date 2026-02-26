###########################################
# CLI behavior
# python -m app.main ingest
# python -m app.main ask "..." --top-k 3
# python -m app.main health
###########################################

import argparse
from rag_pipeline import RagPipeline

def build_parser() -> argparse.ArgumentParser:
    """subcommands: ingest, ask, health"""
    pass

def cmd_ingest(args) -> int:
    RagPipeline.ingest()

def cmd_ask(args) -> int:
    RagPipeline.ask(args.question)

def cmd_health(args) -> int:
    RagPipeline.health()

def main() -> int:
    """Entry point"""
    pass
