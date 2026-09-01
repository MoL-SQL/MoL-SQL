"""Durable experiment progress snapshots and human-readable logs."""

from __future__ import annotations

import json
import time
import threading
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _rounded(value: float | None) -> float | None:
    return round(value, 2) if value is not None else None


class ProgressTracker:
    def __init__(
        self,
        *,
        run_root: Path,
        run_id: str,
        model: str,
        stage_totals: dict[str, int],
        initial_completed: dict[str, int] | None = None,
        initial_correct: int = 0,
        initial_rates_per_second: dict[str, float] | None = None,
    ) -> None:
        self.run_root = run_root
        self.snapshot_path = run_root / "progress.json"
        self.log_path = run_root / "progress.log"
        self.run_id = run_id
        self.model = model
        self.started_at = _now()
        self.started_monotonic = time.monotonic()
        initial = initial_completed or {}
        initial_rates = initial_rates_per_second or {}
        self.stages = {
            stage: {
                "total": total,
                "completed": min(initial.get(stage, 0), total),
                "initial_completed": min(initial.get(stage, 0), total),
                "run_completed": 0,
                "successful": min(initial.get(stage, 0), total)
                if stage == "infer"
                else None,
                "failed": 0 if stage == "infer" else None,
                "correct": min(initial_correct, total) if stage == "eval" else None,
                "started_monotonic": None,
                "initial_rate_per_second": initial_rates.get(stage),
            }
            for stage, total in stage_totals.items()
        }
        self.current: dict[str, str | None] = {
            "stage": None,
            "source": None,
            "cell": None,
        }
        self.status = "running"
        self.error: str | None = None
        self._last_log_key: tuple[Any, ...] | None = None
        self._last_log_monotonic = 0.0
        self._lock = threading.RLock()
        self._stop_heartbeat = threading.Event()
        self.run_root.mkdir(parents=True, exist_ok=True)
        self._publish(force_log=True)
        self._heartbeat = threading.Thread(
            target=self._heartbeat_loop,
            name=f"progress-{run_id}",
            daemon=True,
        )
        self._heartbeat.start()

    def begin(self, stage: str, source: str, cell: str) -> None:
        with self._lock:
            self.current = {"stage": stage, "source": source, "cell": cell}
            state = self.stages.get(stage)
            if state is not None and state["started_monotonic"] is None:
                state["started_monotonic"] = time.monotonic()
            self._publish(force_log=True)

    def advance(
        self,
        stage: str,
        amount: int,
        *,
        successful: int = 0,
        failed: int = 0,
        correct: int = 0,
    ) -> None:
        with self._lock:
            state = self.stages[stage]
            state["run_completed"] += amount
            state["completed"] = min(
                state["total"], state["initial_completed"] + state["run_completed"]
            )
            if state["successful"] is not None:
                state["successful"] += successful
            if state["failed"] is not None:
                state["failed"] += failed
            if state["correct"] is not None:
                state["correct"] += correct
            self._publish()

    def finish(self, status: str, error: str | None = None) -> None:
        with self._lock:
            self.status = status
            self.error = error
            self._stop_heartbeat.set()
            self._publish(force_log=True)

    def _heartbeat_loop(self) -> None:
        while not self._stop_heartbeat.wait(10.0):
            self._publish()

    def _stage_payload(self, name: str, state: dict[str, Any]) -> dict[str, Any]:
        total = state["total"]
        completed = state["completed"]
        percentage = 100.0 if total == 0 else completed * 100.0 / total
        stage_started = state["started_monotonic"]
        elapsed = time.monotonic() - stage_started if stage_started is not None else 0.0
        run_completed = state["run_completed"]
        live_rate = run_completed / elapsed if elapsed > 0 and run_completed > 0 else None
        rate = live_rate or state["initial_rate_per_second"]
        eta_basis = (
            "current_run_throughput"
            if live_rate is not None
            else "historical_latency_seed"
            if rate is not None
            else None
        )
        remaining = max(0, total - completed)
        eta = remaining / rate if rate and remaining else 0.0 if remaining == 0 else None
        estimated_finish = _now() + timedelta(seconds=eta) if eta is not None else None
        payload = {
            "total": total,
            "completed": completed,
            "remaining": remaining,
            "percentage": round(percentage, 2),
            "elapsed_seconds": _rounded(elapsed),
            "rate_per_minute": _rounded(rate * 60 if rate else None),
            "eta_seconds": _rounded(eta),
            "estimated_finish_at": estimated_finish.isoformat()
            if estimated_finish is not None
            else None,
            "eta_basis": eta_basis,
        }
        for key in ("successful", "failed", "correct"):
            if state[key] is not None:
                payload[key] = state[key]
        return payload

    def _payload(self) -> dict[str, Any]:
        stages = {
            name: self._stage_payload(name, state) for name, state in self.stages.items()
        }
        total = sum(stage["total"] for stage in stages.values())
        completed = sum(stage["completed"] for stage in stages.values())
        return {
            "run_id": self.run_id,
            "model": self.model,
            "status": self.status,
            "started_at": self.started_at.isoformat(),
            "updated_at": _now().isoformat(),
            "elapsed_seconds": _rounded(time.monotonic() - self.started_monotonic),
            "overall_percentage": round(completed * 100.0 / total, 2) if total else 100.0,
            "current": self.current,
            "stages": stages,
            "error": self.error,
        }

    def _publish(self, force_log: bool = False) -> None:
        with self._lock:
            payload = self._payload()
            temporary = self.snapshot_path.with_suffix(".json.tmp")
            temporary.write_text(
                json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
                encoding="utf-8",
            )
            temporary.replace(self.snapshot_path)
            current_stage = payload["current"]["stage"]
            stage = payload["stages"].get(current_stage) if current_stage else None
            percentage_bucket = int(stage["percentage"]) if stage else -1
            log_key = (
                self.status,
                current_stage,
                payload["current"]["source"],
                payload["current"]["cell"],
                percentage_bucket,
            )
            now_monotonic = time.monotonic()
            should_log = (
                force_log
                or log_key != self._last_log_key
                or now_monotonic - self._last_log_monotonic >= 30.0
            )
            if not should_log:
                return
            if stage:
                eta_text = (
                    f"{stage['eta_seconds']}s"
                    if stage["eta_seconds"] is not None
                    else "unknown"
                )
                rate_text = (
                    f"{stage['rate_per_minute']}/min"
                    if stage["rate_per_minute"] is not None
                    else "unknown"
                )
                line = (
                    f"{payload['updated_at']} status={self.status} stage={current_stage} "
                    f"source={payload['current']['source']} cell={payload['current']['cell']} "
                    f"progress={stage['completed']}/{stage['total']} "
                    f"percent={stage['percentage']:.2f}% elapsed={payload['elapsed_seconds']:.2f}s "
                    f"eta={eta_text} rate={rate_text}"
                )
            else:
                line = (
                    f"{payload['updated_at']} status={self.status} stage=None "
                    f"overall={payload['overall_percentage']:.2f}% "
                    f"elapsed={payload['elapsed_seconds']:.2f}s"
                )
            if self.error:
                line += f" error={self.error}"
            with self.log_path.open("a", encoding="utf-8") as file:
                file.write(line + "\n")
            self._last_log_key = log_key
            self._last_log_monotonic = now_monotonic
