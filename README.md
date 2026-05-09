# Infield_TEST_DMFB

Reinforcement Learning-Based In-Field Testing for Digital Microfluidic Biochips (DMFBs)

## Overview

Digital microfluidic biochips (DMFBs) are widely used in biomedical applications such as clinical diagnostics, drug discovery, and point-of-care testing. However, defects such as electrode degradation, dielectric breakdown, and manufacturing faults can affect their reliability during operation.

This project presents a Reinforcement Learning (RL)-based approach for efficient in-field testing of DMFBs. The RL agent learns optimal routing paths for test droplets while ensuring that ongoing bioassays are not disrupted.

Compared to traditional SAT-based methods, the proposed RL solution:

- Scales efficiently to larger grids
- Reduces test completion time
- Generates reliable routing paths
- Maintains assay integrity during testing

This repository contains the implementation used in our research work on RL-based in-field testing of DMFBs.

---

# Project Structure

```bash
Infield_TEST_DMFB/
│
├── example/
│   ├── main.py
│   ├── render.py
│   ├── assay_file.py
│   └── ...
│
├── README.md
└── requirements.txt
```

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

You can install all dependencies using:

```bash
pip install -r requirements.txt
```

---

# How to Run

## Step 1: Go to Example Folder

```bash
cd example
```

---

## Step 2: Configure Hyperparameters

Open `main.py` and modify the hyperparameters according to your experiment requirements.

Example parameters include:

- Number of episodes
- Learning rate
- Discount factor
- Epsilon decay
- Grid size
- Reward settings

Also provide the required assay configuration file.

---

## Step 3: Run Training

Execute:

```bash
python main.py
```

The RL agent will start training and generate the best routing path for the test droplets.

After training, you will obtain an action sequence array corresponding to the best episode.

---

## Step 4: Generate Grid Visualization

Copy the generated action sequence string and paste it into the `render.py` file.

Then run:

```bash
python render.py
```

This will generate the grid visualization showing the droplet routing path on the DMFB.

---

# Output

The framework produces:

- Optimal droplet routing paths
- Action sequence arrays
- Grid-based routing visualization
- Reduced test completion time compared to SAT-based approaches

---

# Research Contribution

This work proposes a scalable RL-based framework for concurrent in-field testing of DMFBs. The approach enables efficient defect detection while preserving ongoing bioassay operations, making it suitable for real-world biomedical applications.

---

# Citation

If you use this work in your research, please cite the corresponding paper.

```bibtex
@article{yourpaper,
  title={Reinforcement Learning Based In-Field Testing of Digital Microfluidic Biochips},
  author={Author Name},
  journal={Conference/Journal Name},
  year={2026}
}
```

---

# Authors

- Ritik Kumar Koshta
- IIT Guwahati

---

# License

This project is intended for research and academic purposes.
