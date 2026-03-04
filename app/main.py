###########################################
# CLI behavior
# python -m app.main ingest
# python -m app.main ask "..." --top-k 3
# python -m app.main health
###########################################
from __future__ import annotations
import argparse
import json
from app.rag_pipeline import RagPipeline, AppConfig
import sys


def build_parser() -> argparse.ArgumentParser:
    """subcommands: ingest, ask, health"""
    p = argparse.ArgumentParser(description="Mini RAG CLI")
    sub = p.add_subparsers(dest="cmd", required=True)

    ingest = sub.add_parser("ingest", help="Build/load vector DB from ./data")
    ingest.add_argument("--data-dir", default="./data")
    ingest.add_argument("--persist-path", default="./vector_db")

    ask = sub.add_parser("ask", help="Ask a question (Retrival + generation)")
    ask.add_argument("question", help="Your question string")
    ask.add_argument("--top-k", type=int, default=None)
    ask.add_argument("--persist-path", default="./vector_db")

    health = sub.add_parser("health", help="Check readiness")
    health.add_argument("--persist-path", default="./vector_db")

    return p    


def main() -> int:
    """Entry point"""
    
    args = build_parser().parse_args()

    cfg = AppConfig(
        data_dir=getattr(args, "data_dir", "./data"),
        persist_path=getattr(args, "persist_path", "./vector_db")
        )
    
    pipe = RagPipeline(config=cfg)

    if args.cmd == "ingest":
        result = pipe.ingest()
        print(json.dumps(result, indent=2))
        return 0
    
    if args.cmd == "health":
        result = pipe.health()
        print(json.dumps(result, indent=2))

    if args.cmd == "ask":
        result = pipe.ask(args.question, top_k=args.top_k)
        print(json.dumps(result, indent=2))
        return 0
    
    return 1


if __name__ == "__main__":
    raise SystemExit(main())