<!DOCTYPE html> <html lang="en"> <head> <meta charset="UTF-8" /> </head> <body> <h1>Disaster Management Application Powered by Florence‑2 VLM</h1> <p> An innovative disaster management application that leverages a Visual Language Model—specifically Microsoft’s Florence‑2—to rapidly assess, cluster, and visualize disaster severity based solely on images and geotags. This project provides emergency responders with real‑time insights to prioritize and act during disaster scenarios. </p>
text
<h2>Table of Contents</h2>
<ol>
  <li><a href="#introduction">Introduction</a></li>
  <li><a href="#features">Features</a></li>
  <li><a href="#project-structure">Project Structure</a></li>
  <li><a href="#installation">Installation</a></li>
  <li><a href="#usage">Usage</a></li>
  <li><a href="#requirements">Requirements</a></li>
  <li><a href="#data-preparation">Data Preparation</a></li>
  <li><a href="#contributing">Contributing</a></li>
  <li><a href="#license">License</a></li>
  <li><a href="#contact">Contact</a></li>
</ol>

<h2 id="introduction">Introduction</h2>
<p>
  This repository implements a comprehensive disaster management pipeline
  that:
</p>
<ul>
  <li>
    Uses Florence‑2 VLM to evaluate images and generate a damage severity
    rating.
  </li>
  <li>
    Extracts geotags from images using EXIF metadata to determine disaster
    locations.
  </li>
  <li>
    Clusters geotagged data using a DBSCAN‑based algorithm to identify
    high‑priority disaster hotspots.
  </li>
  <li>
    Generates an interactive heatmap, visualizing the severity scores of
    different locations.
  </li>
  <li>
    Optimizes for low‑compute devices, ensuring ease of fine‑tuning and
    deployment.
  </li>
</ul>
<p>
  By leveraging geotagged images readily available from modern smartphones,
  the application offers a fast, efficient, and context‑aware method for
  assessing disasters and aiding emergency response.
</p>

<h2 id="features">Features</h2>
<ul>
  <li>
    <strong>VLM‑Powered Damage Assessment:</strong> Evaluates image-based
    disaster severity using a pre‑trained Florence‑2 model with user‑defined
    assessment factors.
  </li>
  <li>
    <strong>Custom Assessment Factors Management:</strong> Customize and
    manage disaster assessment criteria via a dedicated Streamlit module.
  </li>
  <li>
    <strong>Geotag Extraction:</strong> Automatically extracts and processes
    GPS data embedded in images.
  </li>
  <li>
    <strong>Clustering of Disaster Data:</strong> Utilizes DBSCAN clustering
    to pinpoint disaster hotspots based on geospatial data.
  </li>
  <li>
    <strong>Interactive Heatmap Visualization:</strong> Generates an intuitive
    heatmap (using Folium) for visual analysis of cluster severity.
  </li>
  <li>
    <strong>Low‑Compute Device Support:</strong> Optimized to run efficiently
    on devices without high‑end computing power.
  </li>
</ul>

<h2 id="project-structure">Project Structure</h2>
<pre>
.
├── dashboard.py # Main Streamlit dashboard for image processing, clustering, and mapping
├── factors.py # Streamlit module to manage disaster assessment factors
├── factors.txt # Contains default disaster assessment factors
├── damage_assessor.py # Module to assess image damage using Florence‑2 VLM
├── cluster_severity.py # Calculates average severity rating of each cluster
├── cluster_analysis.py # Clusters geotagged images using DBSCAN
├── data_preparation.py # Adds simulated geotags to images for disaster scenarios
├── map_generator.py # Generates an interactive disaster severity heatmap using Folium
├── geocoder.py # Converts geographic coordinates into human‑readable locations
├── data_utils.py # Utilities for downloading and preprocessing disaster images
├── config.json # Stores configuration settings (e.g., selected image folder)
├── damage_assessments.json # Output of image damage assessments
├── cluster_centroids.csv # Centroid coordinates for image clusters
├── cluster_severity.json # Average severity of each image cluster
└── README.html # This documentation file (HTML version)
</pre>

text
<h2 id="installation">Installation</h2>
<h3>Prerequisites</h3>
<ul>
  <li>Python 3.7 or higher</li>
  <li>
    <a href="https://streamlit.io/">Streamlit</a>
  </li>
  <li>
    <a href="https://huggingface.co/docs/transformers/">Transformers</a>
  </li>
  <li>
    <a href="https://pytorch.org/">PyTorch</a>
  </li>
  <li>Other dependencies as listed in <code>requirements.txt</code></li>
</ul>
<h3>Step-by-Step Installation</h3>
<ol>
  <li>
    <p><strong>Clone the Repository:</strong></p>
    <pre>git clone https://github.com/yourusername/disaster-management-vlm.git
cd disaster-management-vlm</pre>
</li>
<li>
<p><strong>Set Up a Virtual Environment (Optional but Recommended):</strong></p>
<pre>python -m venv venv
source venv/bin/activate # On Windows: venv\Scripts\activate</pre>
</li>
<li>
<p><strong>Install Dependencies:</strong></p>
<pre>pip install -r requirements.txt</pre>
<p>
If you do not have a <code>requirements.txt</code>, install manually:
</p>
<pre>pip install streamlit transformers torch Pillow piexif scikit-learn pandas numpy folium pyproj geopy streamlit_folium</pre>
</li>
</ol>

text
<h2 id="usage">Usage</h2>
<h3>Data Preparation</h3>
<p>
  Place your disaster images in the <code>damaged_images</code> folder. If you
  need to simulate geotags for these images, run:
</p>
<pre>python data_preparation.py</pre>
<h3>Running the Application</h3>
<p>
  The main dashboard orchestrates the entire pipeline. To launch the
  application, run:
</p>
<pre>streamlit run .\dashboard.py</pre>
<p>
  The dashboard allows you to:
</p>
<ul>
  <li>
    Select the folder containing disaster images.
  </li>
  <li>
    Manage disaster assessment factors via a dedicated module.
  </li>
  <li>
    Process images to evaluate disaster severity using Florence‑2 VLM.
  </li>
  <li>Cluster data based on geotags.</li>
  <li>Generate an interactive heatmap to display cluster severity.</li>
</ul>
<h3>Managing Assessment Factors</h3>
<p>
  To update the disaster assessment criteria, run:
</p>
<pre>streamlit run factors.py</pre>

<h2 id="requirements">Requirements</h2>
<ul>
  <li>Operating System: Cross‑platform (Windows, macOS, Linux)</li>
  <li>Python: 3.7 or higher</li>
  <li>
    Hardware: Optimized for low‑compute devices (GPU recommended for faster
    processing)
  </li>
  <li>
    Key Libraries:
    <ul>
      <li>Streamlit – Interactive dashboard</li>
      <li>
        Hugging Face Transformers – For using the Florence‑2 Visual Language
        Model (VLM)
      </li>
      <li>PyTorch – Deep learning inference</li>
      <li>
        Pillow and piexif – Image processing and EXIF metadata manipulation
      </li>
      <li>scikit-learn – DBSCAN clustering</li>
      <li>Folium – Interactive mapping</li>
      <li>geopy – Reverse geocoding</li>
    </ul>
  </li>
</ul>

<h2 id="data-preparation">Data Preparation</h2>
<p>
  To simulate a disaster scenario:
</p>
<ol>
  <li>Ensure your disaster images are in the <code>damaged_images</code> folder.</li>
  <li>
    Run the following script to generate and embed simulated geotags based on Chicago
    coordinates:
  </li>
</ol>
<pre>python data_preparation.py</pre>

<h2 id="contributing">Contributing</h2>
<p>
  Contributions, issue reports, and feature suggestions are welcome! To contribute:
</p>
<ol>
  <li>Fork the repository.</li>
  <li>
    Create a feature branch:
    <code>git checkout -b feature/AmazingFeature</code>
  </li>
  <li>
    Commit your changes:
    <code>git commit -am 'Add some AmazingFeature'</code>
  </li>
  <li>Push the branch:
    <code>git push origin feature/AmazingFeature</code>
  </li>
  <li>Open a pull request with a clear description of your changes.</li>
</ol>
<p>
  Please maintain the existing code style and include tests where applicable.
</p>

<h2 id="license">License</h2>
<p>
  This project is licensed under the MIT License. See the <code>LICENSE</code> file for further details.
</p>

<h2 id="contact">Contact</h2>
<p>
  For any inquiries, suggestions, or support, please reach out:
</p>
<ul>
  <li><strong>Name:</strong> Your Name</li>
  <li>
    <strong>Email:</strong> <a href="mailto:your.email@example.com">your.email@example.com</a>
  </li>
  <li>
    <strong>LinkedIn:</strong>
    <a href="https://www.linkedin.com/in/yourprofile" target="_blank">Your LinkedIn Profile</a>
  </li>
</ul>
<p>
  By integrating modern AI with geospatial analytics, this disaster management application offers an efficient, low‑compute solution for rapid disaster response. Feel free to explore the code, provide feedback, and contribute to the project!
</p>
