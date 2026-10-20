"""MCP Server for Distributed Lease Lock Coordinator.
100% Python Standard Library JSON-RPC.
"""
import sys
import json
from client import DistributedLeaseLockCoordinator

coordinator = DistributedLeaseLockCoordinator()

def main():
    while True:
        line = sys.stdin.readline()
        if not line:
            break
        try:
            req = json.loads(line)
            method = req.get("method")
            msg_id = req.get("id")

            if method == "tools/list":
                resp = {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {
                        "tools": [
                            {
                                "name": "acquire_lock",
                                "description": "Acquire lease lock with monotonic fencing token",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "resource": {"type": "string"},
                                        "holder_id": {"type": "string"},
                                        "ttl_seconds": {"type": "number", "default": 30.0}
                                    },
                                    "required": ["resource", "holder_id"]
                                }
                            },
                            {
                                "name": "release_lock",
                                "description": "Release held lease lock on resource",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "resource": {"type": "string"},
                                        "holder_id": {"type": "string"}
                                    },
                                    "required": ["resource", "holder_id"]
                                }
                            }
                        ]
                    }
                }
            elif method == "tools/call":
                call_name = req.get("params", {}).get("name")
                args = req.get("params", {}).get("arguments", {})
                if call_name == "acquire_lock":
                    res = coordinator.acquire_lock(
                        resource=args.get("resource", ""),
                        holder_id=args.get("holder_id", ""),
                        ttl_seconds=args.get("ttl_seconds", 30.0)
                    )
                elif call_name == "release_lock":
                    res = coordinator.release_lock(
                        resource=args.get("resource", ""),
                        holder_id=args.get("holder_id", "")
                    )
                else:
                    res = {"error": "Unknown tool"}
                resp = {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}
                }
            else:
                resp = {"jsonrpc": "2.0", "id": msg_id, "error": {"code": -32601, "message": "Method not found"}}
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            sys.stdout.write(json.dumps({"jsonrpc": "2.0", "error": {"code": -32000, "message": str(e)}}) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
