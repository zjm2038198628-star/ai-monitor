# AI Smart Monitoring System

<p align="center">
  <img src="https://img.shields.io/badge/Version-v9.3-brightgreen" alt="Version">
  <img src="https://img.shields.io/badge/Python-3.12-blue?logo=python" alt="Python">
  <img src="https://img.shields.io/badge/CUDA-12.4-green?logo=nvidia" alt="CUDA">
  <img src="https://img.shields.io/badge/InsightFace-0.7.3-red" alt="InsightFace">
  <img src="https://img.shields.io/badge/SCRFD-500m-cyan" alt="SCRFD">
  <img src="https://img.shields.io/badge/Edge-Zero_BoxMOT-brightgreen" alt="Edge">
  <img src="https://img.shields.io/badge/Tests-209/209-brightgreen" alt="Tests">
  <img src="https://img.shields.io/badge/License-LYUN-lightgrey" alt="License">
</p>

<p align="center">
  <b>A production-grade real-time edge AI monitoring system — SCRFD detection, ByteTrack tracking, ArcFace recognition, behavior analysis, GPU-accelerated async inference.</b>
</p>

---

## Introduction

**AI Smart Monitoring System** is a production-grade real-time computer vision pipeline built for edge deployment.

It combines state-of-the-art models — SCRFD for lightweight face detection, ByteTrack for multi-object tracking, InsightFace ArcFace for face recognition, and a full behavior analysis layer — into a single optimized pipeline running entirely on local hardware at real-time speeds.

Designed for scenarios where cloud dependency, latency, or subscription cost is unacceptable:

- **Smart Security** — face-based access control, visitor logging, zone alerts
- **Elderly Care** — behavior monitoring, loitering detection, fall detection
- **Retail Analytics** — customer counting, demographic analysis
- **Smart Home** — family member recognition, automation triggers
- **Edge AI Research** — real-time multi-model pipeline benchmarking

---

## Demo

```
┌──────────────────────────────────────────────────────────────┐
│ FPS: 30.2    Motion: ON    Zone: server_room                 │
│ Persons: 2   Queue: 0 | Pending: 0                           │
│ Detect: normal(2f) | Frame: #1500 | Cool: 300                │
│ cam:2ms | det:10ms | trk:1ms | rec:0 | rnd:1                 │
│                                                              │
│   ┌─────────────┐    ┌─────────────┐                         │
│   │  Byron      │    │  Unknown    │                         │
│   │  MOVING     │    │  STATIONARY │                         │
│   │  (0.87)     │    │             │                         │
│   └─────────────┘    └─────────────┘                         │
│   ID:1               ID:5                                   │
│                                                              │
│   [EVENT] Byron entered server_room                          │
│   Press Q to quit                                            │
└──────────────────────────────────────────────────────────────┘
```

> *GIF demo coming soon. Contributions welcome!*

---

## Features

### Core Pipeline

- [x] **SCRFD Face Detection** — InsightFace det_500m ONNX, CUDA GPU inference, 5-point landmarks
- [x] **Motion Gate** — frame-difference motion detection (threshold 2.0), skips idle frames
- [x] **Adaptive Frame Scheduler** — dynamic detection intervals (fast=1f / normal=2f / slow=5f / force=15f)
- [x] **ByteTrack Multi-Object Tracking** — Kalman filter + Hungarian global matching, stable IDs (desktop)
- [x] **Lightweight IoU Tracker** — pure Python + numpy, zero boxmot dependency, edge-optimized (edge_minimal/balanced)
- [x] **TrackMemory** — long-term trajectory memory with direction penalty, lock mechanism, size weight
- [x] **Track Reassociation** — three-tier lost-track recovery (IoU → spatial proximity → no match)
- [x] **ArcFace Recognition** — 512-dim embeddings via InsightFace 0.7.3 (buffalo_s)
- [x] **Async Recognition Worker** — daemon thread, non-blocking submit + non-blocking collect
- [x] **Smart Scheduler** — priority: new tracks → cooldown-expired → re-verify identified
- [x] **Face Re-ID Cache** — embedding cache (10s TTL) preserves identity across ID switches
- [x] **Hard Dedup** — one registered-name box max; duplicates reset with 600-frame cooldown

### Behavior Analysis Layer

- [x] **Trajectory Analyzer** — per-track speed, direction, stationary frame accumulation
- [x] **Behavior Engine** — state machine: MOVING / STATIONARY / LOITERING / DISAPPEARED
- [x] **Region Manager** — zone system with point-in-polygon entry/leave tracking
- [x] **Event System** — unified event emitter, zone entry/leave events
- [x] **Alert Manager** — cooldown-based alert dedup (30s per alert type)

### Trigger System

- [x] **Out-of-frame trigger** — force re-recognize when track exits frame boundary
- [x] **Overlap trigger** — reset identity immediately when IoU > 0.3
- [x] **Separation trigger** — unlock Hungarian lock + force re-recognize after 0.5s separation
- [x] **Hard dedup trigger** — duplicate registered names reset with 600-frame cooldown

### Recognition Optimization (v9)

- [x] **Face Quality Filter** — 5-rule pre-screening (size/blur/aspect/bounds), rejects ~70% low-quality faces
- [x] **Identity Cooldown** — recognized persons get 600-frame cooldown (vs 300 for unknown)
- [x] **Failed Backoff** — per-track exponential backoff (90f × fail_count), caps at 20 attempts
- [x] **Queue Pressure Gate** — when worker queue ≥3, only new tracks allowed
- [x] **Embedding Cache** — LRU cache (128 entries, 30s TTL) avoids re-recognition after track recovery
- [x] **Vectorized DB Search** — numpy `np.dot(matrix, query)` O(N×512) single-operation cosine similarity

### VisionTask Plugins (v9)

- [x] **VisionTask Interface** — abstract base class for pluggable vision tasks (should_run + run)
- [x] **VisionEvent** — unified event data structure (event_type, track_id, confidence, payload)
- [x] **Fall Detection Stub** — placeholder task, no YOLOv8-Pose loaded, zero overhead
- [x] **Pipeline Integration** — tasks list with per-task try/except + PerformanceMonitor timing
- [x] **Design Doc** — `docs/fall_detection_integration.md` (13 sections, fusion roadmap)

### Engineering & Testing

- [x] **209/209 Comprehensive Tests** — 20 test modules, zero camera/GPU/model-download dependencies
- [x] **3 Deployment Profiles** — edge_minimal(320px/CPU/IoU) / balanced(416px/CPU) / desktop(640px/CUDA/ByteTrack)
- [x] **Layered Dependencies** — `requirements/{base,edge_cpu,desktop,jetson,dev}.txt`
- [x] **Per-Stage Latency** — SCRFD pre/infer/post timing, rolling average
- [x] **GPU/CPU Dual Mode** — auto-detect CUDAExecutionProvider, seamless CPU fallback
- [x] **YAML Configuration** — all tunable parameters with profile cascade (default → profile → CLI args)
- [x] **CLI Face Manager** — register / list / remove faces via command line
- [x] **Thread-Safe Architecture** — main thread owns PersonManager; worker thread processes recognition
- [x] **Metrics Logger** — counters, gauges, runtime tracking, summary reports

### Coming Soon

- [ ] Fall Detection — activate FallDetectionTask with YOLOv8-Pose model
- [ ] TensorRT acceleration (SCRFD 2-3x faster)
- [ ] Web Dashboard — FastAPI + WebSocket
- [ ] Multi-camera RTSP streaming
- [ ] Edge deployment (Jetson Orin / Raspberry Pi 5)

---

## System Architecture

### Single-Camera Pipeline

```
┌────────────────────── Main Thread ──────────────────────┐
│                                                          │
│  Camera ──▶ MotionGate ──▶ FrameScheduler ──▶ SCRFD     │
│  (cv2)      (frame-diff)   (adaptive interval)  (ONNX)  │
│     │              │              │               │       │
│     ▼              ▼              ▼               ▼       │
│  [Frame]      [skip?]       [detect?]        Detection   │
│                                                          │
│  SCRFD ──▶ Tracker ──▶ TrackMemory ──▶ PersonManager    │
│ (640px)   (ByteTrack/  (Hungarian)     (identity+bbox)  │
│            LightIoU)                                    │
│                │              │               │          │
│                ▼              ▼               ▼          │
│           Track IDs     Global Match    Person State     │
│                                                          │
│  PersonManager ──▶ FaceQualityFilter ──▶ Scheduler       │
│     │                  (5 rules)         (priority+cd)   │
│     ▼                       │               │            │
│  Active Persons         reject ~70%    pick next target  │
│                                                          │
│  Scheduler ──▶ Worker(thread) ──▶ FaceDB ──▶ Renderer   │
│    │             submit(crop)    search(512d)  draw+show │
│    ▼                │               │            │       │
│  [submit]       ArcFace(GPU)   [Byron:0.87]  cv2.imshow │
│                                                          │
│  60f status: fps/det/trk/rec/persons/lost/q/enq/rej     │
└──────────────────────────────────────────────────────────┘
```

**Tech per stage:**

| Stage | Technology | Dependency |
|-------|-----------|------------|
| Capture | OpenCV VideoCapture | `opencv-python-headless` |
| Motion | Frame-difference | `numpy` |
| Schedule | Adaptive FrameScheduler | (stdlib) |
| Detect | SCRFD det_500m (InsightFace) | `insightface` + `onnxruntime` |
| Track | ByteTrack or LightweightIoUTracker | `boxmot` (desktop) or `numpy` (edge) |
| Memory | TrackMemory Hungarian | `numpy` |
| Person | PersonManager + EmbeddingCache | `numpy` |
| Quality | FaceQualityFilter (5 rules) | `numpy` + `cv2` |
| Recognize | ArcFace w600k_mbf | `insightface` |
| Render | OpenCV draw + imshow | `opencv-python-headless` |

### Multi-Camera Pipeline (v9.4)

```
┌─────────────────────────────────────────────────────────────┐
│                   MultiCameraManager                        │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Shared: RecognitionWorker + FaceDatabase            │   │
│  │  GlobalInferenceScheduler (max 2 concurrent detects) │   │
│  └──────────────────────────────────────────────────────┘   │
│                           │                                  │
│          ┌────────────────┼────────────────┐                 │
│          ▼                ▼                ▼                 │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐        │
│  │ CameraPipe   │ │ CameraPipe   │ │ CameraPipe   │        │
│  │ #cam0        │ │ #cam1        │ │ #cam2        │        │
│  │ (thread)     │ │ (thread)     │ │ (thread)     │        │
│  │              │ │              │ │              │        │
│  │ Camera──┐    │ │ Camera──┐    │ │ Camera──┐    │        │
│  │ Motion  │    │ │ Motion  │    │ │ Motion  │    │        │
│  │ Sched   │    │ │ Sched   │    │ │ Sched   │    │        │
│  │ SCRFD───┤    │ │ SCRFD───┤    │ │ SCRFD───┤    │        │
│  │ Tracker │    │ │ Tracker │    │ │ Tracker │    │        │
│  │ Person  │    │ │ Person  │    │ │ Person  │    │        │
│  │ Quality │    │ │ Quality │    │ │ Quality │    │        │
│  │ Recog───┼────┼─┤ Recog───┼────┼─┤ Recog───┤    │        │
│  │ Render  │    │ │ Render  │    │ │ Render  │    │        │
│  │         │    │ │         │    │ │         │    │        │
│  │ OWN:    │    │ │ OWN:    │    │ │ OWN:    │    │        │
│  │ tracker │    │ │ tracker │    │ │ tracker │    │        │
│  │ memory  │    │ │ memory  │    │ │ memory  │    │        │
│  │ person  │    │ │ person  │    │ │ person  │    │        │
│  │ tids    │    │ │ tids    │    │ │ tids    │    │        │
│  │ metrics │    │ │ metrics │    │ │ metrics │    │        │
│  └──────────────┘ └──────────────┘ └──────────────┘        │
│                                                             │
│  Per-camera status (60f):                                   │
│  [cam0] fps=44 det=13ms trk=0.1ms rec=0ms | persons=2      │
│         lost=0 | enq=3 skip=0 rej=45 cache=1 q=1            │
│  [cam1] fps=36 det=14ms trk=0.1ms rec=0ms | persons=1      │
│         lost=0 | enq=2 skip=0 rej=52 cache=0 q=1            │
└─────────────────────────────────────────────────────────────┘
```

**Key difference from single-camera:**

| Resource | Single-Camera | Multi-Camera |
|----------|--------------|--------------|
| Tracker | 1 shared | 1 per camera |
| TrackMemory | 1 shared | 1 per camera |
| PersonManager | 1 shared | 1 per camera |
| Track IDs | global namespace | per-camera isolated |
| RecognitionWorker | own | **shared (1 instance)** |
| FaceDatabase | own | **shared (1 instance)** |
| Inference | sequential | **GlobalInferenceScheduler (max 2 concurrent)** |
| Threads | 1 main + 1 worker | 1 per camera + 1 shared worker |

---

## System Architecture

```
┌─────────────────────────────── MAIN THREAD ───────────────────────────────┐
│                                                                            │
│  Camera ──▶ MotionGate ──▶ FrameScheduler ──▶ SCRFD(降频)                  │
│              (diff>2.0?)     (1/2/5/15fr)       InsightFace                │
│                     │              │              │                         │
│                     ▼              ▼              ▼                         │
│              [skip frame]   [skip frame]   ByteTrack + Hungarian           │
│                                                    │                       │
│                          ┌─────────────────────────┤                       │
│                          ▼                         ▼                       │
│                   TrackMemory              PersonManager                   │
│                   ·Hungarian lock          ·Re-ID cache                    │
│                   ·direction penalty       ·identity mgmt                  │
│                          │                         │                       │
│                          ▼                         ▼                       │
│                   TrackReassociation      TrajectoryAnalyzer               │
│                   (IoU→spatial→none)      ·speed/direction                 │
│                                                    │                       │
│                          ┌─────────────────────────┤                       │
│                          ▼                         ▼                       │
│                   RecognitionScheduler      BehaviorEngine                 │
│                   ·new tracks first        ·MOVING/STATIONARY              │
│                   ·300fr cooldown          ·LOITERING/DISAPPEARED          │
│                          │                         │                       │
│                    submit(非阻塞)                   ▼                       │
│                          │                  RegionManager                  │
│                          ▼                  ·zone entry/leave              │
│                  ┌──────────────┐                 │                        │
│                  │ OUTPUT QUEUE │──▶ get_nowait   ▼                        │
│                  └──────────────┘     EventSystem                         │
│                          │            ·unified events                     │
│                          ▼                 │                               │
│                    update PersonMgr         ▼                               │
│                          │          AlertManager                           │
│                          ▼          ·30s cooldown                          │
│                     ┌─────────┐            │                               │
│                     │ Triggers │◀──────────┘                               │
│                     │ ·overlap │                                           │
│                     │ ·out-of- │                                           │
│                     │  frame   │                                           │
│                     │ ·separat │                                           │
│                     └────┬─────┘                                           │
│                          ▼                                                 │
│                    Hard Dedup                                              │
│                    ·1 box per name                                         │
│                          │                                                 │
│                          ▼                                                 │
│                       Renderer                                             │
│                    ·bbox+name+behavior                                     │
│                          │                                                 │
│                          ▼                                                 │
│                  VisionTask Plugins                                         │
│                    ·FallDetection(stub)                                     │
│                    ·per-task try/except                                     │
│                    ·interval scheduling                                     │
│                          │                                                 │
│                          ▼                                                 │
│                     cv2.imshow()                                           │
└────────────────────────────────────────────────────────────────────────────┘
                           │ submit(非阻塞)
                           ▼
┌────────────────── WORKER THREAD (daemon) ──────────────────┐
│                                                             │
│  INPUT QUEUE(max8) ──▶ InsightFace GPU ──▶ DB search       │
│  单任务顺序处理          buffalo_s CUDA     O(N)线性         │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Key Design Decisions

| Decision | Rationale |
|----------|-----------|
| Async recognition in worker thread | ArcFace inference (5-8ms) never blocks video rendering |
| Motion-gated detection | Skips SCRFD on static frames, reduces GPU load significantly |
| Adaptive detection intervals | fast=1f (motion), normal=2f, slow=5f (idle), force=15f (max skip) |
| Hungarian global matching with lock | Locked confirmed matches prevent ID swaps during crossings |
| No velocity prediction | Removed due to variable intervals; rely on center distance + size weight |
| Hard dedup before render | One registered-name box max; duplicates reset with 600fr cooldown |
| Face Re-ID cache (10s TTL) | Lost tracks' embeddings cached; new tracks auto-match to restore identity |
| Separation trigger (0.5s) | Unlock Hungarian locks + force re-recognition after overlapping boxes separate |
| Single-task worker queue | Prevents multi-face GPU memory contention |
| 300-frame recognition cooldown | 10-30x fewer ArcFace calls vs per-frame recognition |
| Thread-safe by design | Main thread owns PersonManager; worker thread only reads DB |

---

## Tech Stack

| Layer | Technology | Version | Role |
|-------|-----------|---------|------|
| Face Detection | SCRFD det_500m (InsightFace) | 0.7.3 | Lightweight face detection + 5-point landmarks |
| Object Tracking (desktop) | ByteTrack (BoxMOT) | 18.x | Multi-object Kalman tracking |
| Object Tracking (edge) | LightweightIoUTracker | — | Greedy IoU, zero deps, edge CPU |
| Long-term Memory | TrackMemory (Hungarian) | — | Global optimal assignment + lock |
| Track Recovery | TrackReassociation | — | IoU → spatial → none matching |
| Face Recognition | ArcFace ONNX (InsightFace) | 0.7.3 | 512-dim embedding extraction |
| Recognition Model | buffalo_s (w600k_mbf) | — | Lightweight mobile-face backbone |
| Face Quality | FaceQualityFilter | — | Size/blur/aspect 5-rule pre-screening |
| Embedding Cache | LRU OrderedDict | — | track_id→embedding, TTL+容量限制 |
| Motion Detection | Motion Gate (frame-diff) | — | Pixel-level motion gating |
| Frame Scheduling | Adaptive Scheduler | — | Dynamic detection intervals |
| Behavior Analysis | TrajectoryAnalyzer + BehaviorEngine | — | MOVING / STATIONARY / LOITERING |
| Zone System | RegionManager (point-in-polygon) | — | Zone entry/leave tracking |
| Event System | EventSystem + AlertManager | — | Unified events + 30s cooldown |
| VisionTask Plugin | VisionTask ABC + VisionEvent | — | Pluggable extension tasks |
| Inference Runtime | ONNX Runtime GPU/CPU | ≥ 1.15 | GPU-accelerated model serving |
| Image Processing | OpenCV | ≥ 4.8 | Capture, display, rendering |
| Config | YAML | ≥ 6.0 | Profiles (edge_minimal/balanced/desktop) |
| Language | Python | 3.12 | Application logic |

---

## Project Structure

```
project/
│
├── main.py                              # Application entry point
├── register_face.py                     # Face registration CLI
├── requirements.txt                     # → requirements/desktop.txt (backward compat)
├── README.md                            # This document
│
├── configs/
│   ├── default.yaml                     # Base config (desktop defaults)
│   ├── edge_minimal.yaml                # 320px / CPU / IoU / no render
│   ├── balanced.yaml                    # 416px / CPU / IoU / render
│   └── desktop.yaml                     # 640px / CUDA / ByteTrack / full
│
├── requirements/
│   ├── base.txt                         # numpy + pyyaml + opencv-python-headless
│   ├── edge_cpu.txt                     # base + insightface + onnxruntime (CPU)
│   ├── desktop.txt                      # base + insightface + onnxruntime-gpu + boxmot
│   ├── jetson.txt                       # base + insightface (TensorRT recommended)
│   └── dev.txt                          # base + pytest + black + ruff
│
├── core/
│   ├── interfaces.py                    # VisionTask ABC + VisionEvent
│   ├── face_quality.py                  # Face quality filter (size/blur/aspect)
│   ├── camera/                          # Camera capture
│   ├── detectors/                       # SCRFD face detector (InsightFace)
│   ├── detection/                       # Legacy YOLOv8-face (deprecated)
│   ├── recognition/                     # InsightFace ArcFace wrapper
│   ├── tracking/                        # ByteTrack multi-object tracker
│   ├── person/                          # Person data model + manager
│   ├── pipeline/                        # Main loop orchestrator (v9)
│   ├── rendering/                       # Frame overlay rendering
│   ├── scheduler/                       # Recognition priority scheduler (v2)
│   ├── workers/                         # Async GPU worker thread (v2)
│   ├── track_memory.py                  # Long-term trajectory memory (Hungarian)
│   ├── track_reassociation.py           # Lost-track recovery (IoU/spatial)
│   ├── frame_scheduler.py               # Adaptive detection interval scheduler
│   ├── trajectory_analyzer.py           # Per-track speed/direction analysis
│   ├── behavior_engine.py               # Behavior state machine
│   ├── region_manager.py                # Zone system (point-in-polygon)
│   ├── event_system.py                  # Unified event emitter
│   ├── alert_manager.py                 # Cooldown-based alert dedup
│   └── metrics_logger.py                # Unified metrics (counters/gauges)
│
├── plugins/
│   ├── __init__.py                      # Plugin package
│   └── fall_detection_stub.py           # Fall detection placeholder (no YOLO)
│
├── docs/
│   └── fall_detection_integration.md    # 13-section fusion design document
│
├── database/
│   └── face_db.py                       # Pickle-based identity database (vectorized search)
│
├── registry/
│   └── register_face.py                 # Registration logic (3 modes)
│
├── utils/
│   ├── motion_gate.py                   # Frame-difference motion detection
│   ├── fps.py                           # FPS counter
│   ├── config_loader.py                 # YAML config loader
│   └── performance_monitor.py           # Per-stage latency + recognition counters
│
├── tests/
│   ├── run_all_tests.py                 # Full test runner (188 checks / 18 modules)
│   ├── run_core_tests.py                # Core-only runner (170 checks / 16 modules)
│   ├── core/                            # Unit tests (no camera/GPU/model)
│   │   ├── test_motion_gate.py          # 4 tests
│   │   ├── test_tracking_system.py      # 4 tests
│   │   ├── test_behavior_system.py      # 4 tests
│   │   ├── test_region_events.py        # 5 tests
│   │   ├── test_performance_metrics.py  # 5 tests
│   │   ├── test_failure_recovery.py     # 5 tests
│   │   ├── test_recognition_scheduler.py # 17 tests
│   │   ├── test_person_manager.py       # 26 tests
│   │   ├── test_track_reassociation.py  # 13 tests
│   │   ├── test_recognition_worker.py   # 14 tests
│   │   ├── test_metrics_logger.py       # 15 tests
│   │   ├── test_face_db.py              # 19 tests
│   │   ├── test_face_quality.py         # 10 tests
│   │   ├── test_recognition_worker_queue.py # 8 tests
│   │   ├── test_embedding_cache.py      # 6 tests
│   │   ├── test_gallery_search.py       # 7 tests
│   │   ├── test_vision_task_interface.py # 13 tests
│   │   └── test_fall_detection_stub.py  # 13 tests
│   ├── integration/                     # Integration tests (model/camera needed)
│   └── manual/                          # Manual tests (human observation)
│
├── models/
│   ├── yolov8n-face.pt                  # Legacy YOLO weights (deprecated)
│   └── scrfd_500m_bnkps.onnx            # SCRFD face detection model
│
├── face_db/
│   └── identities.pkl                   # Registered face embeddings
│
└── insightface-0.7.3/                   # InsightFace source (for compilation)
```

---

## Installation

### Prerequisites

| Software | Version | Check | Required For |
|----------|---------|-------|-------------|
| Python | 3.10+ | `python --version` | All profiles |
| VS C++ Build Tools | 2022 | Windows only | InsightFace compilation |
| NVIDIA GPU | GTX 1060 6GB+ | `nvidia-smi` | desktop profile only |
| CUDA Toolkit | 11.8+ | `nvcc --version` | desktop profile only |

> **edge_minimal / balanced 模式不需要 GPU**，仅需 Python + VS Build Tools。

### Step-by-Step

**1. Download VS Build Tools (Windows)**

```
https://visualstudio.microsoft.com/visual-cpp-build-tools/
```
Select **"Desktop development with C++"** → Install.

**2. Install dependencies**

```bash
# Desktop GPU (推荐)
pip install -r requirements/desktop.txt

# Edge CPU (树莓派等)
pip install -r requirements/edge_cpu.txt
```

**3. Compile insightface 0.7.3**

```bash
pip install insightface-0.7.3\insightface-0.7.3
```

**4. Download buffalo_s model (optional)**

If auto-download fails, manually get:

```
https://github.com/deepinsight/insightface/releases/download/v0.7/buffalo_s.zip
```

Extract to: `C:\Users\<name>\.insightface\models\buffalo_s\`

**5. Register your face**

```bash
python register_face.py --name YourName --simple
```

**6. Run tests (recommended)**

```bash
python tests/run_all_tests.py
```

Expected: `Overall: EDGE AI READY — 209 pass, 0 fail`

**7. Run**

```bash
python main.py
```

---

## Usage

### Start

```bash
python main.py --profile desktop               # GPU 全功能
python main.py --profile edge_minimal          # 边缘最低功耗 (无显示)
python main.py --profile balanced              # CPU 平衡模式
python main.py --camera 0                      # 内置摄像头
python main.py --camera 1                      # 手机/USB摄像头
python main.py --device cpu                    # 强制CPU
python main.py --benchmark                     # 自动无渲染 + 300帧测试
```

### Manage Faces

```bash
python register_face.py --name Alice --simple     # Register (SPACE capture)
python register_face.py --name Alice --image a.jpg # From photo
python register_face.py --list                     # List all
python register_face.py --remove --name Alice      # Delete
```

### Run Tests

```bash
python tests/run_all_tests.py           # 全量 (188 checks / 18 modules)
python tests/run_core_tests.py          # 仅核心 (170 checks / 16 modules)
```

### Key Controls

| Key | Action |
|-----|--------|
| `q` | Quit |
| `ESC` | Cancel registration |

### Display Overlay

| Line | Meaning |
|------|---------|
| `FPS: 30.2` | Real-time frames per second |
| `Motion: ON` | Motion gate status (ON/OFF) |
| `Zone: server_room` | Active zone monitoring |
| `Persons: 2` | Stable tracked persons |
| `Queue: 0 \| Pending: 0` | Recognition queue status |
| `Detect: normal(2f)` | Detection interval mode |
| `cam:2ms \| det:10ms \| trk:1ms \| rec:0 \| rnd:1` | Per-stage latency |
| `MOVING / STATIONARY / LOITERING` | Per-person behavior state |

---

## Configuration

### Profiles (v9)

Three pre-configured profiles for different hardware tiers:

| Profile | Input Size | Detection | Tracking | GPU | Render |
|---------|-----------|-----------|----------|-----|--------|
| `edge_minimal` | 320px | every 4f | IoU | CPU (onnxruntime) | no |
| `balanced` | 416px | every 3f | IoU | CPU (onnxruntime) | yes |
| `desktop` | 640px | every 2f | ByteTrack | CUDA (onnxruntime-gpu) | yes |

**Priority: CLI args > profile config > default.yaml**

```bash
python main.py --profile edge_minimal              # 边缘最低功耗
python main.py --profile balanced                  # 平衡模式
python main.py --profile desktop                   # 桌面GPU全功能
python main.py --profile edge_minimal --device cuda # profile + CLI覆盖
python main.py --config configs/edge_minimal.yaml   # 直接指定配置文件
```

Profile files: `configs/edge_minimal.yaml`, `configs/balanced.yaml`, `configs/desktop.yaml`

### Why edge_minimal defaults

- **no onnxruntime-gpu**: 边缘设备无 NVIDIA GPU 或显存不足
- **no boxmot (ByteTrack)**: 减少第三方依赖，IoU 跟踪对人脸场景足够
- **render=false**: 减少 SDL/OpenCV 显示开销，仅 benchmark
- **input_size=320**: SCRFD 320px 精度损失 <5%，速度提升 ~3x
- **behavior modules OFF**: 减少每帧 100+ 次规则计算

### Parameters

All settings in `configs/default.yaml`:

```yaml
camera:
  index: 0
  width: 640
  height: 480

detector:
  model_name: "buffalo_s"
  input_size: 640
  conf_threshold: 0.5
  detection_interval: 2
  device: cuda

recognition:
  model_name: "buffalo_s"
  recognition_threshold: 0.70
  recognition_cooldown: 300
  min_face_size: 48
  blur_threshold: 80
  max_queue_size: 4

runtime:
  mode: edge_minimal
  use_gpu: true
  enable_behavior: false
  enable_event_system: false
  enable_alert: false
```
motion:
  enabled: true
  method: "frame_diff"
  threshold: 2.0
  min_area: 500

behavior:
  stationary_threshold: 60
  loitering_threshold: 300

pipeline:
  window_name: "Vision AI"
  quit_key: "q"
  worker_queue_size: 8
```

### Quick Tuning

```
Goal                │ Settings
────────────────────┼─────────────────────────────────────────────────
Maximum FPS         │ motion enabled, detection interval: slow(5f)
Best Accuracy       │ conf_threshold: 0.3, recognition_threshold: 0.8
Low VRAM GPU        │ motion enabled, detection interval: normal(2f)
CPU Only            │ --device cpu, motion enabled, detect slow
More Alerts         │ decrease alert cooldown, add more zones
```

---

## Performance

**RTX 4060 Laptop GPU (8GB VRAM) — v8 with SCRFD + motion gate + adaptive scheduling**

| Stage | Latency | Frequency |
|-------|---------|-----------|
| Camera | 2ms | Every frame |
| Motion Gate | <1ms | Every frame |
| SCRFD Detection (640px) | ~15ms | Adaptive (1-15 frames) |
| ByteTrack + Hungarian | ~1ms | Every detect frame |
| Recognition (buffalo_s) | 5ms | On-demand (300fr cooldown) |
| Behavior Analysis | <1ms | Every frame |
| Render | 1ms | Every frame |
| **Total (avg)** | **~6-10ms** | **~100-160 FPS*** |

*\*FPS limited by camera frame rate (typically 30 FPS). Motion gate skips detection on ~70% of frames.*

### Detection Frequency Impact

| Mode | Interval | GPU Load | Latency (avg) |
|------|----------|----------|---------------|
| fast | Every frame | 100% | ~20ms |
| normal | Every 2 frames | 50% | ~12ms |
| slow | Every 5 frames | 20% | ~8ms |
| motion-gated | Adaptive | ~30% | ~6-10ms |

### Multi-Person Scaling

| People | Recognition | Behavior | FPS |
|--------|-------------|----------|-----|
| 1 | Light | Fast | ≈ camera max |
| 2-3 | Light (queued) | Fast | ≈ camera max |
| 4-6 | Moderate | Fast | slight drop |
| 7+ | Queue fill | Fast | increase cooldown |

---

## Test Suite

```
$ python tests/run_all_tests.py

============================================================
 SYSTEM VALIDATION REPORT
============================================================
  Motion Gate:            PASS (4 pass, 0 fail)
  Tracking System:        PASS (4 pass, 0 fail)
  Behavior Engine:        PASS (4 pass, 0 fail)
  Region Events:          PASS (5 pass, 0 fail)
  Performance:            PASS (5 pass, 0 fail)
  Failure Recovery:       PASS (5 pass, 0 fail)
  Recognition Scheduler:  PASS (17 pass, 0 fail)
  Person Manager:         PASS (26 pass, 0 fail)
  Track Reassociation:    PASS (13 pass, 0 fail)
  Recognition Worker:     PASS (14 pass, 0 fail)
  Metrics Logger:         PASS (15 pass, 0 fail)
  Face Database:          PASS (19 pass, 0 fail)
  Face Quality:           PASS (10 pass, 0 fail)
  Worker Queue:           PASS (8 pass, 0 fail)
  Embedding Cache:        PASS (6 pass, 0 fail)
  Gallery Search:         PASS (7 pass, 0 fail)
  VisionTask Interface:   PASS (13 pass, 0 fail)
  FallDetection Stub:     PASS (13 pass, 0 fail)

  Overall: EDGE AI READY
  Total: 188 pass, 0 fail in 4.6s
============================================================
```

---

## Deployment Guide

### Raspberry Pi 5 / Orange Pi

```bash
# 安装边缘依赖 (无GPU包)
pip install -r requirements/edge_cpu.txt

# 下载模型
python -c "import insightface; insightface.app.FaceAnalysis(name='buffalo_s').prepare(ctx_id=-1)"

# 注册人脸
python register_face.py --name YourName --simple

# 运行 (无显示)
python main.py --profile edge_minimal --max-frames 100
```

### Jetson Nano / Orin

```bash
# Jetson 推荐 TensorRT，当前使用 onnxruntime 过渡
pip install -r requirements/jetson.txt

# 如果 onnxruntime-gpu 有预编译 wheel:
# pip install onnxruntime_gpu-*-cp38-cp38-linux_aarch64.whl

# 运行
python main.py --profile edge_minimal --device cpu
```

### RK3588 / 其他 ARM Edge

```bash
pip install -r requirements/edge_cpu.txt
python main.py --profile edge_minimal --camera 1
```

### Desktop GPU (RTX / GTX)

```bash
pip install -r requirements/desktop.txt
python main.py --profile desktop
```

### Benchmark

```bash
# 自动 --no-render --max-frames 300
python main.py --profile edge_minimal --benchmark

# 自定义帧数
python main.py --profile balanced --benchmark --max-frames 1000

# 输出示例:
# [PERF] fps=22.4 detect=18.2ms track=1.1ms recog_queue=2 skipped=38
# [RECOG] enqueue=3 skip=42 reject=18 cache_hit=21 queue=1 worker=23.5ms
```

### Dependency Layering

```
requirements/
├── base.txt          # numpy, pyyaml, opencv-python-headless
├── edge_cpu.txt      # base + insightface + onnxruntime (CPU)
├── desktop.txt       # base + insightface + onnxruntime-gpu + boxmot
├── jetson.txt        # base + insightface (推荐TensorRT)
└── dev.txt           # base + pytest + black + ruff
```

**Why edge_cpu does NOT install onnxruntime-gpu:**
- 树莓派/RK3588 无 NVIDIA GPU
- onnxruntime-gpu wheel 在 ARM 上无预编译版本
- CPU 推理在 320px + 4f interval 下可达 8-15 FPS

**Why edge_minimal disables behavior modules:**
- BehaviorEngine + EventSystem + AlertManager 每帧 ~100 次规则计算
- 对边缘 CPU 是显著开销
- 保留在代码中，可通过 `runtime.enable_behavior: true` 重新启用

---

## Multi-Camera (v9.4)

### Architecture

```
MultiCameraManager
  ├── shared RecognitionWorker     (global, 1 instance)
  ├── shared FaceDatabase          (global, 1 instance)
  ├── GlobalInferenceScheduler     (max 2 concurrent detects)
  ├── CameraPipeline #cam0         (independent thread)
  │     ├── own Tracker + TrackMemory
  │     ├── own PersonManager + FrameScheduler
  │     └── own FrameCounter + CameraMetrics
  ├── CameraPipeline #cam1
  └── CameraPipeline #cam2
```

Each camera has independent tracker/TrackMemory/PersonManager/frame count. Track IDs are isolated between cameras.

### CLI

```bash
python main.py --profile edge_minimal --camera 0 1 --benchmark --max-frames 100
python main.py --multi-camera configs/cameras.yaml
```

### YAML Config

```yaml
# configs/cameras.yaml
cameras:
  - id: cam0
    source: 0
    profile: edge_minimal
  - id: cam1
    source: 1
    profile: edge_minimal

scheduler:
  max_concurrent_detect: 2
```

### Edge Recommendations

| Device | Cameras | Profile |
|--------|---------|---------|
| RK3588 | 2-4 | edge_minimal |
| Raspberry Pi 5 | 1-2 | edge_minimal |
| Jetson Orin | 4+ | edge_minimal |
| Desktop GPU | 6+ | desktop |

`GlobalInferenceScheduler` limits simultaneous SCRFD detections (default 2), preventing CPU overload.

### Benchmark

```bash
python main.py --profile edge_minimal --camera 0 1 --benchmark --max-frames 200

# Output:
#  MULTI-CAMERA REPORT
#   Cameras: 2 | Total FPS: 15.2 | Runtime: 30s
#   [cam0] fps=8.1 det=42ms frames=100 dropped=2
#   [cam1] fps=7.1 det=48ms frames=100 dropped=3
```

---

## Changelog

### v9.4 — 多摄像头架构 (2026-05-15)

- **新增** `core/camera_pipeline.py` — 单摄像头独立处理线程（own tracker/memory/state/reconnect）
- **新增** `core/multi_camera_manager.py` — 管理多 CameraPipeline，shared Worker + GlobalMetrics
- **新增** `core/scheduler/global_inference_scheduler.py` — 令牌桶限制同时 detect（max_concurrent=2）
- **新增** `core/metrics/camera_metrics.py` + `global_metrics.py` — per-camera + 全局统计
- **新增** `configs/cameras.yaml` — 多摄像头 YAML 配置
- **修改** `main.py` — `--multi-camera` + `--camera 0 1` 多源支持
- **结果**：摄像头间 track_id 隔离，per-camera 独立 tracker，全局共享 RecognitionWorker

### v9.3 — 真正边缘化 (2026-05-14)

- **新增** `core/tracking/iou_tracker.py` — 轻量 IoU 跟踪器（纯 Python + numpy，零 boxmot 依赖，贪心匹配）
- **修复** `core/tracking/__init__.py` — MultiObjectTracker 安全导入（boxmot 缺失时降级为 None 不崩溃）
- **修复** `main.py` — `build_tracker()` 根据 `tracking.type` 选择跟踪器（iou→LightweightIoUTracker / bytetrack→MultiObjectTracker）
- **修复** `core/pipeline/pipeline.py` — 移除 MultiObjectTracker 类型强耦合
- **清理** 4 个配置文件跟踪段 — edge_minimal/balanced 仅保留 iou 参数，desktop 保留 ByteTrack
- **新增** 测试：`test_iou_tracker.py` (16) + `test_tracker_factory.py` (6)
- **结果**：`pip install -r requirements/edge_cpu.txt` → `python main.py --profile edge_minimal` 不报错，209/209 测试通过

### v9.2 — 边缘部署配置 + 依赖分层 (2026-05-14)

- **新增** 3 个 profile 配置文件：`edge_minimal.yaml` (320px/CPU/IoU) / `balanced.yaml` (416px/CPU) / `desktop.yaml` (640px/CUDA/ByteTrack)
- **新增** `main.py` — `_deep_merge()` 配置级联：default → profile → --config → CLI args
- **新增** 5 层依赖文件：`requirements/{base,edge_cpu,desktop,jetson,dev}.txt`
- **新增** `--benchmark` 参数（自动 --no-render --max-frames 300）
- **新增** README 部署指南（树莓派、Jetson、RK3588、桌面、Benchmark）

### v9.1 — VisionTask 插件接口 (2026-05-14)

- **新增** `core/interfaces.py` — VisionTask ABC + VisionEvent 数据结构
- **新增** `plugins/fall_detection_stub.py` — 摔倒检测空实现（不加载 YOLOv8-Pose）
- **新增** `docs/fall_detection_integration.md` — 13 节融合设计文档
- **修改** `core/pipeline.py` — `_run_tasks()` 插件循环，每 task 独立 try/except + 计时
- **结果**：默认零开销，未来只需 `tasks.fall_detection.enabled=true` + 加载模型即可激活

### v9.0 — 识别性能优化 (2026-05-14)

- **新增** `core/face_quality.py` — FaceQualityFilter（尺寸/模糊/长宽比 5 规则过滤）
- **重写** `core/scheduler/recognition_scheduler.py` — v2：identity cooldown (600f) + failed backoff (90f×N) + queue_pressure_skip
- **重写** `core/workers/recognition_worker.py` — v2：bounded queue + result cache + quality-aware submit
- **强化** `core/person/person_manager.py` — EmbeddingCache（LRU 128 条目，30s TTL）
- **优化** `database/face_db.py` — numpy 向量化 `np.dot` 一次矩阵运算
- **扩展** `utils/performance_monitor.py` — 识别计数器（enqueue/skip/reject/cache_hit）+ 每 60 帧 [RECOG] 报告
- **更新** `configs/default.yaml` — 12 项 recognition 配置

### v8.0 — 减法重构 + 行为层 (2026-05-14)

- **重构** `main.py` — 拆分为 9 个 `build_*` 函数 + `build_optional_modules()` 按配置加载
- **新增** `configs/default.yaml` — `runtime` 段 6 个 enable 开关（behavior/event/alert/reassociation/region）
- **修改** `core/pipeline/pipeline.py` — 可选模块支持 None + `_behavior_enabled` 初始化开关 + 身份触发器独立于行为块 + no_render 模式
- **测试**：重组为 `core/` / `integration/` / `manual/` 三层 + `run_core_tests.py`

### v7.x — SCRFD 检测 + ByteTrack + 行为层 (2026-05-13)

- SCRFD 探测器稳定化（InsightFace FaceAnalysis，CUDA backend）
- Motion Gate（帧差分 motion detection）
- Frame Scheduler（自适应检测间隔）
- TrackMemory（匈牙利全局匹配 + 锁机制）
- PersonManager（Re-ID embedding 缓存）
- TrajectoryAnalyzer + BehaviorEngine（MOVING/STATIONARY/LOITERING）
- RegionManager + EventSystem + AlertManager（区域告警，30s cooldown）
- 识别调度器（300 帧 cooldown + pending guard）
- 硬去重（注册用户 1 框上限，600 帧冷却）
- 重叠 / 分离触发器（0.5s 解锁 + 强制重识别）

---

## Roadmap

```
v9  ✅  Recognition optimization, FaceQualityFilter, embedding cache (current)
v8  ✅  Behavior layer, triggers, hard dedup, 131-pass test suite
v7  ✅  TrackMemory Hungarian + lock, PersonManager Re-ID cache
v6  ✅  SCRFD detector, 5-point landmarks, InsightFace detection
v5  ✅  Detection降频, PersonManager rendering, tracker optimization
v4  ✅  Async recognition, buffalo_s, smart scheduler
v9.1 ✅  VisionTask plugin interface, fall detection stub, 188-pass suite
v9.3 ✅  LightweightIoUTracker, true edge (zero boxmot), 209-pass suite (current)
v9.2 ✅  Edge deployment profiles, dependency layering, benchmark mode
v10 🔜  Fall Detection — activate FallDetectionTask with YOLOv8-Pose
v11 🔜  TensorRT acceleration (SCRFD 2-3x speedup)
v12 🔜  Web dashboard (FastAPI + WebSocket)
v13 🔜  Multi-camera RTSP streaming
```

---

## FAQ

<details>
<summary><b>FPS is too low / video is choppy</b></summary>

Enable motion gate in config (default ON). Set `detector.input_size: 320` for faster detection. Use `buffalo_s` model.
</details>

<details>
<summary><b>Two people show the same name</b></summary>

Increase `recognition_threshold` to 0.75-0.8. Hard dedup ensures only one box per registered name. System auto-reverifies every 300 frames.
</details>

<details>
<summary><b>Identity switches when people cross paths</b></summary>

Hungarian lock prevents ID swaps during close interaction. Re-ID cache (10s TTL) preserves identity across lost/recovered tracks. Separation trigger (0.5s) forces re-recognition after overlap ends.
</details>

<details>
<summary><b>Changed model, faces not recognized</b></summary>

buffalo_l and buffalo_s embeddings are incompatible. Re-register all faces via `register_face.py`.
</details>

<details>
<summary><b>Camera won't open</b></summary>

Try `python main.py --camera 0` for built-in, or `--camera 1` for phone. Default is 1 (DroidCam). Windows: Settings → Privacy → Camera → Allow apps.
</details>

<details>
<summary><b>How do I run tests?</b></summary>

```bash
python tests/run_all_tests.py
```

No dependencies needed beyond Python + NumPy. Tests run in ~4 seconds.
</details>

<details>
<summary><b>InsightFace compile error</b></summary>

Install VS C++ Build Tools first. Then run:
```bash
pip install insightface-0.7.3\insightface-0.7.3
```
</details>

---

## License

LYUN License

---

<p align="center">
  <sub>Built for edge AI and real-time vision.</sub>
</p>
