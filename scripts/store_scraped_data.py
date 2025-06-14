#!/usr/bin/env python3
"""
Script for storing scraped data in the database.
Usage: python -m scripts.manual_ingest <index_name> [--debug] [--max-chunks N]
"""

import argparse
import asyncio
import sys

from src.services.store_data import store_data


async def main():
  parser = argparse.ArgumentParser(description="Ingest scraped data")
  parser.add_argument("index_name", help="Name of the index to ingest")
  parser.add_argument("--debug", action="store_true", help="Run in debug mode")
  parser.add_argument(
    "--max-chunks", type=int, default=20, help="Max chunks in debug mode"
  )

  args = parser.parse_args()

  print(f"Starting ingestion for index: {args.index_name}")
  if args.debug:
    print(f"Running in DEBUG mode (max {args.max_chunks} chunks)")

  result = await store_data(
    args.index_name, debug_mode=args.debug, max_debug_chunks=args.max_chunks
  )

  if result.is_ok():
    stats = result.ok()
    print("Data storage completed successfully")
    print("Statistics:")
    print(stats)
  else:
    print(f"Data storage failed: {result.err()}")
    sys.exit(1)


if __name__ == "__main__":
  asyncio.run(main())
