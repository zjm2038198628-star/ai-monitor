"""
渲染模块 — 统一管理画面叠加逻辑。

将绘制逻辑从 Pipeline 中剥离，遵循单一职责原则。
所有绘制方法原地修改 frame，不返回复制。
"""

import cv2
import numpy as np


# 默认配色方案（B, G, R）
COLOR_IDENTIFIED = (0, 255, 0)    # 绿色 — 已识别
COLOR_UNKNOWN = (128, 128, 128)    # 灰色 — 未识别
COLOR_FPS = (0, 255, 255)          # 黄色 — FPS
COLOR_CONFIDENCE = (0, 255, 0)     # 绿色 — 置信度

FONT = cv2.FONT_HERSHEY_SIMPLEX


class Renderer:
    """
    画面渲染器。

    职责：
      1. 绘制人脸检测框 + 身份标签
      2. 绘制 FPS 叠加
      3. 统一配色方案与字体

    设计原则：
      - 所有方法原地修改 frame
      - 配色集中管理，方便后续做主题切换
      - 与检测/识别逻辑完全解耦

    使用示例：
      renderer = Renderer(font_scale=0.6, thickness=2)
      renderer.draw_face(frame, bbox, name="Byron", similarity=0.85, confidence=0.94)
      renderer.draw_fps(frame, 29.8)
    """

    def __init__(
        self,
        font_scale: float = 0.6,
        thickness: int = 2,
        fps_font_scale: float = 0.8,
    ) -> None:
        """
        初始化渲染器。

        Args:
            font_scale:      人脸标签字体缩放。
            thickness:       框线粗细。
            fps_font_scale:  FPS 文字字体缩放（稍大以保证可读性）。
        """
        self.font_scale = font_scale
        self.thickness = thickness
        self.fps_font_scale = fps_font_scale

    # ------------------------------------------------------------------
    # 公共绘制方法
    # ------------------------------------------------------------------

    def draw_face_identity(
        self,
        frame: np.ndarray,
        bbox: tuple,
        name: str = "Unknown",
        similarity: float = 0.0,
        confidence: float = 0.0,
    ) -> None:
        """
        绘制人脸框 + 身份标签。

        配色策略：
          - 已识别: 绿色框 + "Name (sim: 0.85)"
          - 未识别: 灰色框 + "Unknown"

        Args:
            frame:      BGR 图像帧 (原地修改)。
            bbox:       检测框 (x1, y1, x2, y2)。
            name:       人名，默认 "Unknown"。
            similarity: 余弦相似度（已识别时有值）。
            confidence: YOLO 检测置信度。
        """
        x1, y1, x2, y2 = bbox

        is_identified = (name != "Unknown")
        color = COLOR_IDENTIFIED if is_identified else COLOR_UNKNOWN

        # 矩形框
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, self.thickness)

        # 标签文字
        if is_identified:
            label = f"{name} ({similarity:.2f})"
        else:
            label = name

        # 文字背景（半透明效果不好做，用实心矩形兜底确保可读性）
        (tw, th), baseline = cv2.getTextSize(label, FONT, self.font_scale, self.thickness)
        cv2.rectangle(frame, (x1, y1 - th - 10), (x1 + tw + 6, y1), color, -1)

        # 文字（白字）
        cv2.putText(
            frame, label, (x1 + 3, y1 - 6),
            FONT, self.font_scale, (255, 255, 255), self.thickness,
        )

    def draw_fps(self, frame: np.ndarray, fps: float) -> None:
        """
        在左上角叠加 FPS 信息。

        Args:
            frame: BGR 图像帧 (原地修改)。
            fps:   当前帧率数值。
        """
        fps_str = f"FPS: {fps:.1f}"
        cv2.putText(
            frame, fps_str, (10, 30),
            FONT, self.fps_font_scale, COLOR_FPS, self.thickness + 1,
        )

    def draw_system_info(
        self,
        frame: np.ndarray,
        lines: list,
        start_y: int = 60,
        line_spacing: int = 30,
    ) -> None:
        """
        在画面左上角（FPS 下方）绘制多行系统信息。

        Args:
            frame:        BGR 图像帧 (原地修改)。
            lines:        要显示的文本行列表，如 ["Faces: 2", "DB: 5 users"]。
            start_y:      起始 Y 坐标。
            line_spacing: 行间距。
        """
        for i, line in enumerate(lines):
            y = start_y + i * line_spacing
            cv2.putText(
                frame, line, (10, y),
                FONT, self.font_scale, (255, 255, 255), self.thickness,
            )
