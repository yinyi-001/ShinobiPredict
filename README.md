
# 忍者预测 ([ShinobiPredict](D:\Code\ShinobiPredict)) - 火影忍者格斗数据采集与轨迹预测
这是一个基于计算机视觉（YOLOv5）与时序神经网络（LSTM）的对战视频分析项目。本项目旨在通过解析格斗游戏视频，提取角色的实时坐标，并利用深度学习模型预测角色的下一步走位，为后续的动作识别与博弈分析打下基础。
## 🚀 项目已实现功能 (Current Progress)
1. **视频自动拆帧 (Data Extraction)**：通过 OpenCV 智能提取视频帧，并支持拖拽式批处理。
2. **目标检测 (Object Detection)**：利用 YOLOv5 训练了专属的“鸣人”检测模型，mAP@0.5 达到 0.9 以上。
3. **数据清洗与结构化 (Data Processing)**：将 YOLO 输出的散装 txt 坐标日志，按时间序列清洗并转化为标准的 Excel/CSV 格式。
4. **走位轨迹预测 (Trajectory Prediction)**：构建 LSTM 神经网络，通过前 10 帧的坐标序列，精准预测下一帧的角色落点。
## 📊 模型效果展示
以下是 LSTM 模型预测的走位轨迹（红线为 AI 预测，蓝线为真实走位），可见模型极其精准地捕捉了角色的移动趋势，并有效过滤了游戏画面的抖动噪音：
![Trajectory Prediction](assets/trajectory_plot.png)
## 🛠️ 环境配置 (Setup)
1. 克隆本仓库（注：数据集与模型权重过大，未上传至仓库，需自行训练）。
2. 安装依赖：
   ```bash
   pip install -r requirements.txt

_(注：确保安装了带 CUDA 支持的 PyTorch)_

## 📂 目录结构 (Project Structure)

- `01_datasets/`：存放视频、截图、标签以及清洗后的 Excel 数据（已在 `.gitignore` 中忽略）。
    
- `02_scripts/`：核心代码库。
    
    - `video_extract.py`：视频拆帧脚本。
        
    - `txt_to_csv.py`：把 YOLO 的 txt 坐标洗成 CSV 时间线数据。
        
    - `predict_trajectory.py`：LSTM 轨迹预测模型训练与可视化脚本。
        
- `assets/`：存放 README 展示图片。
    
- `yolov5/`：YOLOv5 官方源码（用于训练与推理）。
    

---

## 🗺️ 未来规划与期望 (Roadmap & Expectations)

当前项目仅完成了“角色在哪”的空间坐标预测。为了构建一个真正的“格斗游戏 AI 教练”，接下来的开发路线规划如下：

### 阶段一：细粒度动作识别 (Action Recognition)
- **多类别目标检测**：除了识别角色本体（`naruto`），增加对“具体的平A（区分第几A）”、“技能特效（如螺旋丸，以及飞行物类型的脱手技能）”、“打击命中光效（Hit Effect）”、“密卷”、“通灵”等标签的识别。
- **状态逻辑判定**：结合 YOLO 的检测结果与 LSTM 时序逻辑，利用状态机（State Machine）判断角色当前处于“移动”、“平A（1A/2A/3A）”、“释放技能的硬体”、“顶通灵密卷的金刚体”、“前后摇”还是“受击硬直”状态。
- **连续动作预测**：解决二技能（影分身）等多段、多动作复合技能的精准时序切分。

### 阶段二：双人博弈与态势感知 (Game State Awareness)
- **双角色特征提取**：将敌方角色的坐标、血量、查克拉量纳入输入特征。
- **距离与威胁评估**：计算敌我相对距离，预测敌方下一步的攻击意图（如起跳、突进）。

### 阶段三：最优解推荐 (Optimal Action Recommendation)
- **行为克隆 (Behavior Cloning)**：收集高段位玩家对局视频，让 AI 模仿高手的应对策略。
- **强化学习 (Reinforcement Learning)**：结合游戏机制建立奖励函数，让 AI 在模拟环境中探索“最佳走位”与“反打时机”。

---

_Created with ❤️ by yinyi-001_