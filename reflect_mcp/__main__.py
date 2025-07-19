#!/usr/bin/env python3
"""Entry point for the Reflect MCP server."""

import sys
import os
import traceback

# Only show debug output if MCP_DEBUG is set
if os.getenv("MCP_DEBUG"):
    print(f"Reflect MCP starting...", file=sys.stderr)
    print(f"Python: {sys.executable}", file=sys.stderr)
    print(f"CWD: {os.getcwd()}", file=sys.stderr)
    print(f"Args: {sys.argv}", file=sys.stderr)

from .server import main as server_main


def main():
    """Run the MCP server."""
    try:
        server_main()
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()