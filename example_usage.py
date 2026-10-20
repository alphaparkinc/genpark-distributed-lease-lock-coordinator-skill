"""Example usage for Distributed Lease Lock Coordinator."""
from client import DistributedLeaseLockCoordinator
import json

coord = DistributedLeaseLockCoordinator()

# Agent Alpha acquires lock
res_alpha = coord.acquire_lock("customer_update_job", "agent_alpha", ttl_seconds=60.0)
print("Alpha acquire:", json.dumps(res_alpha))

# Agent Beta attempts to acquire same resource
res_beta = coord.acquire_lock("customer_update_job", "agent_beta", ttl_seconds=60.0)
print("Beta acquire (blocked):", json.dumps(res_beta))

# Alpha releases
coord.release_lock("customer_update_job", "agent_alpha")

# Beta retries and succeeds
res_beta_retry = coord.acquire_lock("customer_update_job", "agent_beta", ttl_seconds=60.0)
print("Beta retry (acquired):", json.dumps(res_beta_retry))
