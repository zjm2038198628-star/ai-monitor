"""
FallDetectionTask — 摔倒检测插件 (空实现 / Stub)。

当前阶段不加载 YOLOv8-Pose 模型，仅预留接口。
未来融合时：替换 run() 中的空实现为 YOLOv8-Pose 推理逻辑。
"""

import logging
from typing import List

from core.interfaces import VisionTask, VisionEvent

logger = logging.getLogger(__name__)


class FallDetectionTask(VisionTask):
    """
    摔倒检测任务 (Stub)。

    配置:
        tasks.fall_detection:
          enabled: false        # 默认关闭
          interval: 5           # 每5帧运行一次
          model: null           # 未来: YOLOv8-Pose 模型路径
          device: cpu           # 推理设备
          confidence_threshold: 0.6
          min_duration_frames: 10  # 最少持续帧数才判定跌倒
    """

    def __init__(self, config: dict = None):
        super().__init__()
        self.name = "fall_detection"
        self.enabled = False
        self.interval = 5
        self._debug = False

        if config:
            self.enabled = config.get("enabled", False)
            self.interval = config.get("interval", 5)
            self._model_path = config.get("model", None)
            self._device = config.get("device", "cpu")
            self._conf_threshold = config.get("confidence_threshold", 0.6)
            self._min_duration = config.get("min_duration_frames", 10)

    def should_run(self, frame_id: int, tracks: list, context: dict) -> bool:
        """每隔 interval 帧运行一次，且需要存在 track。"""
        if not self.enabled:
            return False
        if len(tracks) == 0:
            return False
        return frame_id % self.interval == 0

    def run(self, frame, tracks: list, context: dict) -> List[VisionEvent]:
        """
        空实现：不加载 YOLOv8-Pose，不执行推理，返回空事件列表。

        未来实现逻辑:
            1. 为每个 track 裁剪 ROI
            2. YOLOv8-Pose 推理 → 17个关键点
            3. 计算躯干倾斜角 / 头部高度 / 肩臀比
            4. 判断是否跌倒 (confidence > threshold)
            5. 持续 min_duration_frames 后触发事件
            6. 返回 VisionEvent(event_type="fall_detected", ...)
        """
        if self._debug:
            logger.debug(f"[FallDetectionStub] frame={context.get('frame_count')}, "
                         f"tracks={len(tracks)}, model={self._model_path or 'None'}")

        # 不加载 YOLOv8-Pose 模型
        # 不引入 ultralytics / torch
        # 不增加推理开销

        return []
