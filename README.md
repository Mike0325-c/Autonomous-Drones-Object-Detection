# Autonomous Drone Object Detection
## Overview
This project focuses on building an object detection system for autonomous drones. Drones face unique challenges, such as changing altitudes, varying speeds, and environmental factors. The goal is to develop a system using deep learning to detect objects in real-time from drone images, even under difficult conditions.

## Motivation
Drones are increasingly used in areas like surveillance, agriculture, and monitoring. However, detecting objects accurately in drone images is tough because of factors like altitude changes and fast movement. This project aims to solve those challenges using deep learning, making drone operations safer and more efficient.

## Problem
We want to create a system that can detect and classify objects in images taken by drones, even when the environment is unpredictable. Traditional methods struggle with the challenges of drone flight, so we’ll use deep learning to improve detection accuracy.

## Data
The VisDrone dataset is used for this project. It contains:

8,599 images:
Training: 6,471 images
Validation: 548 images
Testing: 1,580 images
It includes 12 object categories (e.g., pedestrian, car, bicycle, etc.). Some categories, like "ignored regions" and "others," are excluded from the evaluation.

The dataset has some imbalanced categories, meaning some objects (like people and cars) are more common than others (like tricycles).
**Dataset link**: https://github.com/VisDrone/VisDrone-Dataset?tab=readme-ov-file

## Goal
The aim is to develop a system that can detect objects in drone images accurately, even with changes in altitude, speed, and environment, using deep learning models trained on the VisDrone dataset.
