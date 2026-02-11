# TinyML-Based Motor Fault Diagnosis System

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![STM32](https://img.shields.io/badge/STM32-F303RE-03234B?logo=stmicroelectronics)](https://www.st.com/en/microcontrollers-microprocessors/stm32f303re.html)
[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-Lite-FF6F00?logo=tensorflow)](https://www.tensorflow.org/lite)

> **Final Year Project (FYP)** - Universiti Teknologi Malaysia  
> **Author:** Muhammad Luqman Hakim bin Mohd Zawahil  
> **Supervisor:** Dr. Noorhazirah Sunar  
> **Duration:** October 2025 - July 2026  
> **Status:** 🔄 Active Development (FYP Part 2)

---

## 📋 Table of Contents
- [Overview](#overview)
- [Problem Statement](#problem-statement)
- [System Architecture](#system-architecture)
- [Hardware Setup](#hardware-setup)
- [Software Components](#software-components)
- [Current Progress](#current-progress)
- [Installation & Usage](#installation--usage)
- [Results](#results)
- [Challenges & Solutions](#challenges--solutions)
- [Future Work](#future-work)
- [Publications](#publications)
- [Acknowledgments](#acknowledgments)

---

## 🎯 Overview

This project develops an **embedded machine learning system** for real-time vibration-based fault diagnosis in DC motors using **STM32F3 microcontroller**. The system explores optimal preprocessing strategies (FFT, time-domain features) and model architectures (SVM, 1D-CNN) for deployment on resource-constrained embedded devices.

### Key Features
- ⚡ Real-time vibration data acquisition at 3200 Hz target sampling rate
- 🧠 On-device machine learning inference using TinyML
- 📊 Automated data collection and labeling pipeline
- 🔧 Multiple preprocessing strategies for model optimization
- 📈 Comparative analysis of SVM vs 1D-CNN on embedded hardware

### Research Gap
Investigating the trade-offs between different signal preprocessing techniques and their impact on model performance when deployed on resource-constrained microcontrollers.

---

## ❓ Problem Statement

Predictive maintenance in industrial motors requires expensive and complex monitoring systems. This project aims to develop a **low-cost, embedded solution** that can:

1. Detect bearing faults in DC motors through vibration analysis
2. Operate in real-time on a microcontroller (< $10 hardware cost)
3. Achieve >85% classification accuracy with <100ms inference time
4. Minimize power consumption for edge deployment

**Traditional Approach:** Cloud-based ML (requires connectivity, latency issues)  
**Our Approach:** Edge ML (on-device inference, low latency, privacy-preserving)

---

## 🏗️ System Architecture
```
┌─────────────────────────────────────────────────────────────────┐
│                     DATA ACQUISITION PHASE                       │
│                                                                   │
│  775 DC Motor → Side-Loaded → ADXL345 → STM32F3 → UART → PC    │
│  with Bearing    Bearing      (SPI)     (DMA)           ↓        │
│                                                    Python Script  │
│                                                    (.csv output)  │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                   PREPROCESSING & TRAINING                       │
│                                                                   │
│  Raw Data → Cleaning → Feature Extraction → Model Training      │
│                         (FFT, Time-domain)   (SVM, 1D-CNN)      │
│                                                    ↓              │
│                                            TensorFlow Lite       │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                    DEPLOYMENT ON STM32                           │
│                                                                   │
│  ADXL345 → STM32F3 → Preprocessing → ML Inference → Result     │
│            (DMA)     (On-device)      (STM32Cube.AI)             │
└─────────────────────────────────────────────────────────────────┘

## 🔧 Hardware Setup

### Components

| Component | Model | Purpose | Interface |
|-----------|-------|---------|-----------|
| Microcontroller | STM32F303 (Discovery Board) | Main processing unit | - |
| Accelerometer | ADXL345 | Vibration sensing | SPI (3-wire) |
| Motor | 775 DC Motor | Test subject | - |
| Bearing | Side-loaded bearing | Fault simulation | Rotating Unbalance, Bearing Contamination |
| Data Bridge | Arduino Nano | UART-USB converter | UART |
| Power Supply | 12V DC adapter | Motor power | - |

```
ADXL345 Pin  →  STM32F3 Pin
VCC          →  3.3V
GND          →  GND
CS           →  PA4 (GPIO)
SDO          →  PA6 (SPI1_MISO)
SDA          →  PA7 (SPI1_MOSI)
SCL          →  PA5 (SPI1_SCK)
```

**STM32F3 to Arduino Nano (UART):**
```
STM32 TX (PA2)  →  Arduino RX
STM32 RX (PA3)  →  Arduino TX
GND             →  GND
```
---

## 💻 Software Components

### 1. Firmware (STM32F3)
- **Language:** C (STM32 HAL)
- **IDE:** STM32CubeIDE
- **Key Features:**
  - ADXL345 SPI driver (polling/interrupt/DMA modes)
  - UART data transmission to PC
  - Real-time data buffering
  - Low-power modes (future)

### 2. Data Processing (Python)
- **Version:** Python 3.8+
- **Key Libraries:**
  - `numpy`, `pandas` - Data manipulation
  - `matplotlib`, `seaborn` - Visualization
  - `scipy` - Signal processing (FFT)
  - `pyserial` - UART communication

### 3. Model Training (Python)
- **Frameworks:**
  - `scikit-learn` - SVM implementation
  - `tensorflow` - 1D-CNN implementation
- **Optimization:**
  - TensorFlow Lite conversion
  - Quantization (int8, float16)
  - Model pruning

### 4. Deployment (STM32Cube.AI)
- Converts TFLite models to C code
- Optimizes for STM32 hardware
- Generates inference runtime

---

## ✅ Current Progress

### Completed (FYP Part 1 - Aug-Dec 2025)
- [x] Literature review on TinyML and vibration analysis
- [x] Hardware assembly and initial testing
- [x] ADXL345 SPI driver development (polling mode)
- [x] UART communication pipeline to PC
- [x] Python data collection script with automated labeling
- [x] Data visualization and exploratory analysis
- [x] Signal preprocessing implementation (FFT, time-domain)

### In Progress (FYP Part 2 - Jan-Jul 2026)
- [x] Investigating DMA-based data acquisition (addressing timing issues)
- [ ] SVM model training and optimization
- [ ] 1D-CNN model training and optimization
- [ ] TensorFlow Lite model conversion
- [ ] STM32Cube.AI deployment and testing
- [ ] Comparative analysis of preprocessing strategies
- [ ] Performance benchmarking (accuracy, latency, memory)
- [ ] Journal paper writing

**Current Challenge:** Data corruption during extended operation at 3200 Hz sampling rate.
- **Hypothesis:** ISR latency exceeding 312.5 μs sample period
- **Proposed Solution:** DMA-based circular buffering
- **Status:** Under investigation (oscilloscope testing scheduled Apr 2026)

---

## 🚀 Installation & Usage

### Prerequisites
- STM32CubeIDE (firmware development)
- Python 3.8+ (data processing)
- STM32CubeMX (configuration)
- STM32Cube.AI (deployment, optional)

### Quick Start

#### 1. Firmware Setup
```bash
# Clone repository
git clone https://github.com/yourusername/motor-fault-diagnosis-tinyml.git
cd motor-fault-diagnosis-tinyml/firmware

# Open project in STM32CubeIDE
# File → Open Projects from File System → Select firmware/

# Build and flash to STM32F3
# Project → Build Project
# Run → Debug (or use ST-Link)
```

#### 2. Data Collection
```bash
cd data_processing

# Install dependencies
pip install -r requirements.txt

# Collect vibration data
python collect_data.py --port COM3 --duration 60 --label healthy

# Options:
#   --port: Serial port (e.g., COM3, /dev/ttyUSB0)
#   --duration: Recording duration in seconds
#   --label: Fault condition (healthy, inner_race, outer_race, ball)
```

#### 3. Data Preprocessing
```bash
# Preprocess collected data
python preprocess.py --input data/raw/ --output data/processed/

# Visualize data
python visualize.py --file data/processed/healthy_001.csv
```

#### 4. Model Training
```bash
cd model_training

# Train SVM
python train_svm.py --data ../data/processed/ --output models/svm_model.pkl

# Train 1D-CNN
python train_cnn.py --data ../data/processed/ --output models/cnn_model.h5

# Convert to TFLite
python convert_to_tflite.py --model models/cnn_model.h5 --output deployment/model_files/
```

For detailed instructions, see READMEs in respective folders.

---

## 📊 Results

> **Note:** Results will be updated as FYP Part 2 progresses (Mac-Jul 2026)

### Preliminary Findings (FYP Part 1)

**Data Collection:**
- Successfully collected 2,000+ samples across 2 fault conditions
- Sampling rate: 1600 Hz (stable), 3200 Hz (intermittent issues)
- Data quality: >95% valid samples at 1600 Hz

**Signal Analysis:**
- Clear frequency peaks observed for different fault types
- FFT features show >80% separability (preliminary)
- Time-domain features (RMS, kurtosis) also promising

### Expected Final Results (July 2026)

| Metric | Target | Current |
|--------|--------|---------|
| Classification Accuracy | >85% | TBD |
| Inference Time | <100 ms | TBD |
| Model Size | <50 KB | TBD |
| Power Consumption | <100 mW | TBD |
| Sampling Rate | 3200 Hz | 1600 Hz* |

*\*Currently investigating timing optimization*

---

## 🐛 Challenges & Solutions

### Challenge 1: High-Speed Data Acquisition
**Problem:** Data corruption at 3200 Hz sampling rate during extended operation

**Root Cause Analysis (Hypothesis):**
- Interrupt-driven SPI reads exceed available CPU cycles
- ISR execution time: ~400 μs (estimated)
- Required budget: 312.5 μs (1/3200 Hz)
- Result: Missed interrupts and data loss

**Proposed Solution:**
1. Implement DMA-based SPI transfer (hardware-handled, no CPU overhead)
2. Use circular buffering with double-buffer technique
3. DMA completion interrupt only sets flag (minimal ISR time)
4. Main loop processes complete buffers asynchronously

**Implementation Status:** Researching (Ref: Mastering STM32 Ch.12-13)

**Verification Plan:**
- Measure actual ISR timing with oscilloscope (April 2026)
- Compare DMA vs interrupt latency
- Stress test at 5000 Hz to validate robustness

### Challenge 2: Model Size Constraints
**Problem:** TensorFlow models too large for STM32F3 flash (256 KB)

**Solutions Being Explored:**
- Quantization (float32 → int8)
- Model pruning
- Knowledge distillation
- Simpler architectures (SVM may outperform CNN on this constraint)

---

## 🔮 Future Work

### Short-term (FYP Completion - Jul 2026)
- [ ] Complete DMA implementation and validation
- [ ] Deploy and benchmark both SVM and 1D-CNN models
- [ ] Publish comparative analysis in UTM Jurnal Teknologi
- [ ] Create demonstration video for FYP presentation

### Long-term (Post-Graduation)
- [ ] Expand to multi-class fault classification (4+ fault types)
- [ ] Implement adaptive learning (online model updates)
- [ ] Develop wireless sensor node (BLE/LoRa)
- [ ] Create commercial prototype with enclosure
- [ ] Explore federated learning for distributed motors

---

## 📝 Publications

### In Preparation
**"Optimizing TinyML Models for Vibration-Based Motor Fault Diagnosis Through Signal Preprocessing on STM32 Microcontrollers"**
- **Authors:** M. L. Hakim, Dr Noorhazirah Sunar
- **Target Journal:** UTM Jurnal Teknologi
- **Status:** Manuscript in progress
- **Expected Submission:** Q2 2026

### Conference Presentations
- FYP Presentation, UTM (Expected: July 2026)

---

## 🙏 Acknowledgments

This project would not be possible without:

- **Supervisor:** Dr Noorhazirah Sunar - For invaluable guidance and support
- **UTM Faculty of Engineering** - Lab facilities and equipment
- **Carmine Noviello** - Author of "Mastering STM32" (excellent reference)
- **Online Communities:** STM32 forums, r/embedded, Stack Overflow

### References & Resources
- Carmine Noviello, *Mastering STM32* (2nd Edition)
- STM32 HAL Documentation
- TensorFlow Lite for Microcontrollers
- Edge Impulse Documentation

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

**Note:** If publishing research, please cite appropriately.

---

## 📧 Contact

**Muhammad Luqman Hakim bin Mohd Zawahil**  
📧 Email: luqmanmuhammad652@gmail.com
💼 LinkedIn: www.linkedin.com/in/luqmanhakim24 

---

## 🗂️ Repository Structure
```
motor-fault-diagnosis-tinyml/
├── README.md                 ← You are here
├── docs/                     ← Additional documentation
├── firmware/                 ← STM32 embedded code
├── data_processing/          ← Python scripts for data handling
├── model_training/           ← ML model development
├── deployment/               ← STM32Cube.AI deployment files
├── results/                  ← Experimental results
└── hardware/                 ← Hardware documentation
```

---

## 🔄 Project Timeline
```
Aug 2025  ███████░░░░░░░  Hardware setup, initial testing
Sep 2025  ████████░░░░░░  Data collection pipeline
Oct 2025  █████████░░░░░  Data preprocessing
Nov 2025  ██████████░░░░  Exploratory analysis
Dec 2025  ███████████░░░  FYP Part 1 completion
─────────────────────────────────────────────
Jan 2026  ████████████░░  DMA optimization (current)
Feb 2026  ████████████░░  Model training
Mar 2026  ████████████░░  TFLite conversion
Apr 2026  ████████████░░  STM32 deployment
May 2026  ████████████░░  Testing & benchmarking
Jun 2026  ████████████░░  Paper writing
Jul 2026  ██████████████  Final presentation
```

---

## ⭐ Star History

If you find this project useful, please consider giving it a star!

[![Star History Chart](https://api.star-history.com/svg?repos=yourusername/motor-fault-diagnosis-tinyml&type=Date)](https://star-history.com/#yourusername/motor-fault-diagnosis-tinyml&Date)

---

**Last Updated:** January 2026  
**Project Status:** 🟡 Active Development (40% Complete)
