# Infield_TEST_DMFB

Reinforcement Learning-Based In-Field Testing for Digital Microfluidic Biochips (DMFBs)

---

# Overview

Digital Microfluidic Biochips (DMFBs) are emerging as an important technology for biomedical applications such as:

- Clinical diagnostics
- Drug discovery
- DNA analysis
- Point-of-care testing
- Sample preparation

DMFBs manipulate droplets dynamically over a 2D electrode array to perform biochemical operations. However, during long-term operation, defects such as:

- Electrode degradation
- Dielectric breakdown
- Manufacturing faults
- Actuation failures

can occur and affect the reliability of the chip.

To address this problem, this project proposes a Reinforcement Learning (RL)-based in-field testing framework that intelligently routes a test droplet during ongoing assay execution without interrupting the bioassay operations.

---

# Example Bioassay Included

This repository includes an example multiple target mixture preparation assay for demonstration and testing purposes.

Example assay used in the provided implementation:

```text
A : B : C = 1 : 2 : 1

A : C : D = 1 : 2 : 1
```

This assay is provided only as a sample workload so that users can directly run and understand the framework.

The framework itself is not limited to this particular bioassay. Users can define and test different assay configurations by modifying the assay files inside:

```bash
Example/assay/
```

During assay execution:

- Functional assay droplets move dynamically across the grid
- The RL-based test droplet avoids interfering with assay operations
- The testing agent attempts to maximize footprint coverage efficiently

This creates a challenging routing problem where both:

- Bioassay integrity
- Testing efficiency

must be maintained simultaneously.

---

# Key Features

Compared to traditional SAT-based approaches, the proposed RL framework:

- Scales efficiently to larger grids
- Reduces total test completion time
- Learns intelligent routing paths
- Avoids collision with assay droplets
- Preserves assay integrity during testing
- Generates reliable and reusable routing policies

---

# Routing Strategy

The framework primarily uses Reinforcement Learning (RL) for routing the test droplet during ongoing assay execution.

Running `main.py` generates:

- Action sequence array
- Visited footprint information

These generated outputs can later be used inside `render.py` to create grid visualizations and GIF animations of droplet movement on the DMFB.

After the assay execution time is completed, a greedy algorithm is used to:

- Cover remaining uncovered footprints
- Route the test droplet safely to the sink position

During execution, assay droplets move dynamically at different timestamps. The positions occupied by assay droplets at a particular timestamp act as temporary obstacles for the RL-based test droplet.

This ensures that:

- Assay operations are not disturbed
- Collision between droplets is avoided
- Safe concurrent testing is maintained

---

# Project Structure

```bash
Infield_TEST_DMFB/
│
├── Example/
│   ├── main.py
│   ├── render.py
│   ├── assay/
│   │   ├── assay_1.py
│   │   └── ...
│   │
│   └── ...
│
├── README.md
└── requirements.txt
```

---

# Input Description

The input assay configuration is provided inside:

```bash
Example/assay/assay_1.py
```

The assay file contains all necessary information required for simulation and training.

## The input includes:

### 1. Grid Dimension

Defines the size of the DMFB grid.

Example:

```python
WIDTH = 12
HEIGHT = 12
```

### 2. Assay Droplet Information

Contains the positions of assay droplets at different timestamps during assay execution.

Example:

```python
droplets = {
    0: [(1,2), (3,4)],
    1: [(1,3), (3,5)],
}
```

This represents dynamic movement of bioassay droplets over time.

The positions occupied by assay droplets at a particular timestamp are treated as temporary obstacles by the RL-based test droplet.

### 3. Obstacles / Restricted Cells

Defines cells that cannot be used for routing.

Example:

```python
obstacles = [(4,5), (5,5)]
```

### 4. Footprint Information

Contains footprint locations that must be covered by the test droplet for testing purposes.

### 5. Test Droplet Starting Position

Defines the initial location of the RL-based test droplet.

Example:

```python
start = (0,1)
```

### 6. Sink Position

Defines the final destination where the test droplet must be routed after testing completion.

Example:

```python
sink = (11,11)
```

---

# Output Description

The framework generates the following outputs:

## 1. Optimal Routing Path

The best routing path learned by the RL agent.

## 2. Action Sequence Array

Sequence of actions corresponding to the best episode.

Example:

```python
[0,0,1,2,3,0,1]
```

where actions correspond to droplet movements such as:

- Up
- Down
- Left
- Right
- Stay

## 3. Visited Footprint Information

Stores the footprints covered by the test droplet during execution.

## 4. Grid Visualization and GIF Generation

Visual representation of:

- Assay droplets
- Test droplet movement
- Covered footprints
- Obstacles
- Sink routing

Generated using:

```bash
python render.py
```

The render file uses the generated action sequence and visited footprint information to create visualization outputs and GIF animations.

## 5. Complete Footprint Coverage

Ensures all reachable footprints are covered using:

- RL routing
- Greedy completion strategy

## 6. Sink Routing

After testing completion, the droplet is routed safely to the sink position.

---

# Dependencies

Install the following dependencies before running the project:

```bash
contourpy==1.3.3
cycler==0.12.1
fonttools==4.61.1
ImageIO==2.37.2
kiwisolver==1.4.9
matplotlib==3.10.8
numpy==2.4.2
packaging==26.0
pillow==12.1.1
pip==24.0
pyparsing==3.3.2
python-dateutil==2.9.0.post0
six==1.17.0
```

Install all dependencies using:

```bash
pip install -r requirements.txt
```

---

# How to Run

## Step 1: Go to Example Folder

```bash
cd Example
```

## Step 2: Configure Hyperparameters

Open `main.py` and modify hyperparameters according to your experiment requirements.

Parameters include:

- Number of episodes
- Learning rate
- Discount factor
- Epsilon decay
- Reward values
- Grid size
- Assay configuration file

Users can also replace the provided example assay with their own custom assay configuration.

## Step 3: Run Training

Execute:

```bash
python main.py
```

The RL agent will start training and learn routing paths for the test droplet.

Running `main.py` generates:

- Best routing path
- Action sequence array
- Visited footprint information

After the assay execution time is completed, the greedy algorithm handles:

- Remaining footprint coverage
- Sink routing

## Step 4: Generate Visualization

Copy the generated action sequence array and visited footprint information into:

```bash
render.py
```

Then execute:

```bash
python render.py
```

This generates the complete DMFB routing visualization and GIF animation.

---

# Output

The framework produces:

- Optimal droplet routing paths
- Action sequence arrays
- Visited footprint information
- Grid-based routing visualization
- GIF animation of droplet movement
- Complete footprint coverage
- Sink routing after assay completion
- Reduced test completion time compared to SAT-based approaches

---

# Research Contribution

This work proposes a scalable RL-based framework for concurrent in-field testing of DMFBs.

The framework:

- Enables intelligent defect testing during assay execution
- Preserves ongoing biochemical operations
- Reduces testing time compared to SAT-based methods
- Improves scalability for larger DMFB grids

The integration of Reinforcement Learning with greedy post-processing improves:

- Routing efficiency
- Coverage performance
- Real-world applicability of DMFB testing

---

# Citation

If you use this work in your research, please cite the corresponding paper.

```bibtex
@article{Link_of_paper,
  title={Intelligent In-Field Testing of Digital Microfluidic Biochips using Reinforcement Learning},
  author={Author Name},
  journal={Conference/Journal Name},
  year={2026}
}
```

---

# Authors

- Ritik Kumar Koshta
- Indian Institute of Technology Guwahati (IIT Guwahati)

---

# License

This project is intended for research and academic purposes.
