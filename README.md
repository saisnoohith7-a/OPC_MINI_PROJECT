# 🚀 Hybrid Job Scheduling Optimization

> **An intelligent job scheduling simulator that compares classical scheduling algorithms with an improved hybrid scheduling approach to minimize weighted tardiness in real-world manufacturing and production systems.**

---

## 📖 Overview

Efficient job scheduling is crucial in manufacturing, cloud computing, and production planning. This project evaluates four scheduling algorithms and demonstrates how an **Improved Hybrid Scheduling Algorithm** outperforms traditional methods under complex workloads.

The simulator creates two different scheduling environments:

* 🟢 **Scenario A:** Balanced workloads with similar priorities.
* 🔴 **Scenario B:** Real-world workloads with varying job priorities and tight deadlines.

The algorithms are compared using multiple performance metrics and visualized through informative graphs.

---

## ✨ Features

* 📊 Generate synthetic scheduling datasets
* ⚡ Implement **Shortest Processing Time (SPT)**
* 📅 Implement **Earliest Due Date (EDD)**
* 🔀 Traditional Hybrid Scheduling
* 🧠 Improved Hybrid Scheduling Algorithm
* 🎯 Automatic alpha (α) parameter optimization
* 📈 Performance comparison using multiple metrics
* 📉 Five professional visualizations
* 🖥️ Console summary of scheduling performance

---

## 🛠️ Technologies Used

| Technology    | Purpose                |
| ------------- | ---------------------- |
| 🐍 Python     | Programming Language   |
| 🔢 NumPy      | Numerical Computations |
| 🗂️ Pandas    | Data Processing        |
| 📊 Matplotlib | Data Visualization     |
| 🎨 Seaborn    | Statistical Graphs     |

---

## 🧮 Scheduling Algorithms

### ⚡ Shortest Processing Time (SPT)

Schedules jobs with the smallest processing time first.

### 📅 Earliest Due Date (EDD)

Schedules jobs according to the earliest deadlines.

### 🔀 Traditional Hybrid

Combines processing time and slack time using a weighted parameter (α).

### 🧠 Improved Hybrid

Uses:

* Processing efficiency
* Dynamic slack
* Job urgency
* Job weights

to minimize weighted tardiness more effectively.

---

## 📏 Evaluation Metrics

The following metrics are calculated for every scheduling strategy:

* ⏱️ Flow Time
* ⌛ Tardiness
* ⚖️ Weighted Tardiness
* ✅ On-Time Jobs
* ❌ Late Jobs
* 🎯 Service Level

---

## 📊 Visualizations

The project generates **five analytical graphs**:

### 📈 1. Scenario A Optimization Curve

Compares Traditional Hybrid and Improved Hybrid across different α values.

### 📉 2. Scenario B Optimization Curve

Shows how the improved algorithm performs under real-world conditions.

### 📊 3. Tardiness Distribution

Displays the lateness distribution for each scheduling method.

### 📋 4. Flow Time vs Tardiness

Bar chart comparing average flow time and tardiness.

### 🥧 5. Service Level Analysis

Pie chart showing the percentage of late and on-time jobs.

---

## 📂 Project Structure

```text
Hybrid-Job-Scheduling/
│
├── scheduling.py
├── README.md
└── requirements.txt
```

---

## ⚙️ Installation

Clone the repository:

```bash
git clone <repository-url>
cd Hybrid-Job-Scheduling
```

Install dependencies:

```bash
pip install numpy pandas matplotlib seaborn
```

---

## ▶️ Run the Project

```bash
python scheduling.py
```

---

## 📌 Console Output

The program prints:

* 📌 Mean Slack
* 📌 Mean Weighted Slack
* 📌 Mean Flow Time
* 📌 Mean Tardiness
* 📌 Mean Weighted Tardiness

---

## 📸 Output Preview

The simulation opens **5 visualization windows** containing:

* 📈 Optimization Curves
* 📊 Performance Comparison
* 📉 Tardiness Distribution
* 📋 Flow Time Analysis
* 🥧 Service Level Pie Chart

---

## 🏆 Key Results

✅ Improved Hybrid Scheduling consistently:

* Reduces **Weighted Tardiness**
* Improves scheduling efficiency
* Handles high-priority jobs better
* Performs better than **SPT**, **EDD**, and the Traditional Hybrid approach in high-variance scenarios

---

## 🔮 Future Enhancements

* 🤖 Machine Learning-based Scheduling
* 🧬 Genetic Algorithm Optimization
* ☁️ Cloud Scheduling Support
* 🏭 Multi-Machine Scheduling
* 🌐 Streamlit Dashboard
* 📂 CSV Dataset Support
* 📈 Gantt Chart Visualization
