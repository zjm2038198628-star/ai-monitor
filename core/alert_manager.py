"""
AlertManager — 告警管理器。

功能:
  - 处理 EventSystem 的事件
  - 同事件+同track 冷却期内不重复报警
  - 日志输出

用法:
    am = AlertManager(cooldown_seconds=30)
    am.process(events)
"""

import logging
import time
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


class AlertManager:
    def __init__(self, cooldown_seconds: float = 30.0):
        self.cooldown = cooldown_seconds
        self._last_alert: Dict[str, float] = {}

    def process(self, events: List[Dict[str, Any]]) -> None:
        for event in events:
            self._handle(event)

    def _handle(self, event: Dict[str, Any]) -> None:
        etype = event["event_type"]
        tid = event["track_id"]
        key = f"{etype}_{tid}"

        now = time.time()
        if key in self._last_alert:
            if now - self._last_alert[key] < self.cooldown:
                return

        self._last_alert[key] = now
        logger.info(f"[ALERT] {etype} track={tid} {event.get('timestamp','')}")
