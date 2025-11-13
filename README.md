# Groundwater Energy (GWE) Transport Modeling Tutorial

This repository contains a series of Jupyter notebooks demonstrating the integration of MODFLOW-6 groundwater energy transport modeling with PEST++ for parameter estimation and uncertainty analysis. The tutorials are based on the GMDSI Open Loop Low Temperature Geothermal System tutorials. Original materials available at: https://gmdsi.org/blog/gwe_slideshow/

## Overview

The tutorial demonstrates how to:

- Set up PEST++ interfaces with unstructured grid models
- Parameterize hydraulic conductivity fields using non-stationary geostatistics informed by conceptual geological knowledge
- Perform surrogate-based data assimilation and predictive uncertainty analysis using data space inversion

## Model Description

The model represents a shallow, channelized alluvial deposit system near a river with the following characteristics:

- Single-layer unstructured grid model
- Historical and forecast simulation periods
- Steady-state flow model with transient heat transport
- Open loop shallow geothermal system simulation with seasonal temperature variations

## Repository Structure

### Notebooks

- **`00_model.ipynb`** - Model introduction and basic setup
- **`01_setup_pstfrom.ipynb`** - PEST++ interface configuration
- **`02_priomc.ipynb`** - Prior Monte Carlo analysis
- **`03_dsi.ipynb`** - Data space inversion
- **`04_dsiae.ipynb`** - Data space inversion with autoencoder

## Getting Started

### Prerequisites

Create the conda environment:

```bash
conda env create -f environment.yml
conda activate gwe
```

### Running the Tutorials

1. Start with `00_model.ipynb` to understand the base model
2. Progress through the numbered notebooks in sequence
3. Each notebook builds on concepts from previous tutorials

**Note**: The initial model run takes approximately 5 minutes on a MacBook Pro. Runing the Prior Monte Carlo notebook can take a while (~60min).


