"""Distributed Lease Lock Coordinator.
100% Python Standard Library.
"""
import time

class DistributedLeaseLockCoordinator:
    """In-memory distributed lease lock with monotonically increasing fencing tokens."""

    def __init__(self):
        self.locks = {}
        self.fencing_counter = 0

    def acquire_lock(self, resource: str, holder_id: str, ttl_seconds: float = 30.0, current_time: float = None) -> dict:
        now = current_time or time.time()
        curr = self.locks.get(resource)

        if curr and now < curr["expires_at"] and curr["holder"] != holder_id:
            return {
                "acquired": False,
                "resource": resource,
                "current_holder": curr["holder"],
                "remaining_ttl": round(curr["expires_at"] - now, 2)
            }

        self.fencing_counter += 1
        expires_at = now + ttl_seconds
        self.locks[resource] = {
            "holder": holder_id,
            "expires_at": expires_at,
            "fencing_token": self.fencing_counter
        }
        return {
            "acquired": True,
            "resource": resource,
            "holder_id": holder_id,
            "fencing_token": self.fencing_counter,
            "expires_at": expires_at
        }

    def release_lock(self, resource: str, holder_id: str) -> dict:
        curr = self.locks.get(resource)
        if not curr:
            return {"released": False, "error": "No lock on resource"}
        if curr["holder"] != holder_id:
            return {"released": False, "error": "Cannot release lock held by another entity"}

        del self.locks[resource]
        return {"released": True, "resource": resource}
