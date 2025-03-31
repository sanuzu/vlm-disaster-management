Disaster Management Application Powered by Florence‑2 VLM
An innovative disaster management application that leverages a Visual Language Model—specifically Microsoft’s Florence‑2—to rapidly assess, cluster, and visualize disaster severity based solely on images and geotags. This project aims to provide emergency responders with real‑time insights to prioritize and act during disaster scenarios.

Table of Contents
Introduction

Features

Project Structure

Installation

Usage

Requirements

Data Preparation

Contributing

License

Contact

Introduction
This repository implements a complete disaster management pipeline that:

Uses Florence‑2 VLM to evaluate images and generate a damage severity rating.

Extracts geotags from images using EXIF metadata to determine disaster locations.

Clusters geotagged data using a DBSCAN‑based algorithm to identify high‑priority disaster hotspots.

Generates an interactive heatmap, visualizing the severity scores of different locations.

Optimizes for low‑compute devices, ensuring ease of fine‑tuning and deployment.

By leveraging geotagged images—readily available from modern smartphones—the application provides a fast, efficient, and context‑aware method for assessing disasters and aiding in emergency response.

Features
VLM‑Powered Damage Assessment: Evaluates image-based disaster severity using a pre‑trained Florence‑2 model with user‑defined assessment factors.

Custom Assessment Factors Management: Customize and manage disaster assessment criteria via a dedicated Streamlit module.

Geotag Extraction: Automatically extracts and processes GPS info embedded in images.

Clustering of Disaster Data: Utilizes DBSCAN clustering to pinpoint disaster hotspots based on geospatial data.

Interactive Heatmap Visualization: Creates an intuitive heatmap (using Folium) for visual analysis of cluster severity.

Low‑Compute Device Support: Optimized to run efficiently on devices without high‑end computing resources.

Project Structure
text
.
├── dashboard.py             # Main Streamlit dashboard for image processing, clustering, and mapping
├── factors.py               # Streamlit module to manage disaster assessment factors
├── factors.txt              # Contains default disaster assessment factors
├── damage_assessor.py       # Module to assess image damage using Florence‑2 VLM
├── cluster_severity.py      # Calculates average severity rating of each cluster
├── cluster_analysis.py      # Clusters geotagged images using DBSCAN
├── data_preparation.py      # Adds simulated geotags to images for disaster scenarios
├── map_generator.py         # Generates an interactive disaster severity heatmap using Folium
├── geocoder.py              # Converts geographic coordinates into human‑readable locations
├── data_utils.py            # Utilities for downloading and preprocessing disaster images
├── config.json              # Stores configuration settings (e.g., selected image folder)
├── damage_assessments.json  # Output of image damage assessments
├── cluster_centroids.csv    # Centroid coordinates for image clusters
├── cluster_severity.json    # Average severity of each image cluster
└── README.md                # This documentation file
Installation
Prerequisites
Python 3.7 or higher

Streamlit

Transformers

PyTorch

Other dependencies as listed in requirements.txt

Step-by-Step Installation
Clone the Repository:

bash
git clone https://github.com/yourusername/disaster-management-vlm.git
cd disaster-management-vlm
Set Up a Virtual Environment (Optional but Recommended):

bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
Install Dependencies:

If a requirements.txt file is available, run:

bash
pip install -r requirements.txt
Otherwise, manually install the required packages:

bash
pip install streamlit transformers torch Pillow piexif scikit-learn pandas numpy folium pyproj geopy streamlit_folium
Usage
Data Preparation
Place your disaster images in the damaged_images folder. If you need to simulate geotags for these images using predefined Chicago coordinates, run:

bash
python data_preparation.py
Running the Application
The main dashboard orchestrates the entire pipeline. To launch the application, run:

bash
streamlit run .\dashboard.py
The dashboard lets you:

Select Image Folder: Choose the folder containing disaster images.

Manage Assessment Factors: Customize the factors that influence the damage rating process.

Process Images: Run the DAMAGE ASSESSOR to evaluate disaster severity using the Florence‑2 model.

Cluster Data: Automatically cluster images based on geotags.

Visualize Severity: Generate an interactive heatmap (via map_generator.py) to display cluster severity.

Managing Assessment Factors
If you wish to modify or update the disaster assessment criteria, launch the factors management module:

bash
streamlit run factors.py
This tool allows you to add or remove assessment factors, which directly influence the damage estimation process during image assessment.

Requirements
Operating System: Cross‑platform (compatible with Windows, macOS, Linux)

Python: 3.7+

Hardware: Ideal for low‑compute devices; GPU is recommended for faster Florence‑2 inference.

Key Libraries:

Streamlit for the interactive dashboard

Hugging Face Transformers for the VLM (Florence‑2)

PyTorch for deep learning inference

Pillow and piexif for image processing and EXIF metadata manipulation

scikit-learn for DBSCAN clustering

Folium for interactive map generation

geopy for reverse geocoding

Data Preparation
To simulate a disaster scenario, use the data_preparation.py script to:

Fetch images from the damaged_images folder.

Generate simulated geotags based on predefined Chicago disaster center coordinates.

Embed GPS metadata into the images for further processing.

Run:

bash
python data_preparation.py
Contributing
Contributions, issue reports, and feature suggestions are welcome!

Fork the repository.

Create a feature branch: git checkout -b feature/AmazingFeature

Commit your changes: git commit -am 'Add some AmazingFeature'

Push to the branch: git push origin feature/AmazingFeature

Open a pull request with a thorough description of your changes.

Please adhere to the existing code style and include tests where applicable.

License
This project is licensed under the MIT License. See the LICENSE file for further details.

Contact
For any inquiries, suggestions, or support, please reach out:

Name: Your Name

Email: your.email@example.com

LinkedIn: Your LinkedIn Profile

By integrating modern AI with geospatial analytics, this disaster management application offers an efficient, low‑compute solution for rapid disaster response. Feel free to explore the code, provide feedback, and contribute to the project!

Simply copy and paste this text into your GitHub repository’s README.md file for a professional and detailed project overview. Enjoy!
