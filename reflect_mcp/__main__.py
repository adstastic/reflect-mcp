#!/usr/bin/env python3
"""Entry point for the Reflect MCP server."""

import asyncio
import sys
from .server import main as server_main


def main():
    """Run the MCP server."""
    try:
        asyncio.run(server_main())
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()