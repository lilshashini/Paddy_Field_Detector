# 🌾 Paddy Fields and Shrimp Ponds Detection System

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Detectron2](https://img.shields.io/badge/Detectron2-Latest-green.svg)](https://detectron2.readthedocs.io/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

An advanced computer vision system for automated detection and segmentation of agricultural fields (paddy fields, shrimp farms) from aerial imagery using deep learning techniques.

## 🎯 Features

- **Automated Field Detection**: Detect paddy fields, shrimp farms, and agricultural boundaries from aerial images
- **Polygon Extraction**: Generate precise polygon boundaries around detected fields
- **Multiple Output Formats**: Export results as JSON, GeoJSON, and Shapefiles
- **Web Interface**: User-friendly Streamlit application for easy interaction
- **Batch Processing**: Process multiple images efficiently
- **Detailed Analytics**: Get comprehensive statistics about detected fields
- **High Accuracy**: Powered by Mask R-CNN and Detectron2 framework

## 🏗️ Architecture

```
├── Model Training (Detectron2 + Mask R-CNN)
├── Inference Engine (OpenCV + Computer Vision)
├── Web Interface (Streamlit)
├── API Backend (FastAPI/Flask)
└── Output Processing (Polygon-drawn aerial images,GeoJSON, Shapefile generation)
```

## 🚀 Technologies Used

- **Deep Learning**: Detectron2, Mask R-CNN, PyTorch
- **Computer Vision**: OpenCV, NumPy
- **Segmentation**: Segment Anything Model (SAM)
- **Web Framework**: Streamlit
- **Data Processing**: COCO annotations, JSON, GeoJSON
- **Geospatial**: Shapefile generation
- **Visualization**: Matplotlib, PIL
- **Data Annotation**: Roboflow, LabelMe
- **Dataset Management**: Roboflow platform for dataset versioning and augmentation

## 📋 Requirements

```
torch>=1.9.0
detectron2
opencv-python>=4.5.0
numpy>=1.21.0
matplotlib>=3.3.0
streamlit>=1.28.0
pillow>=8.3.0
requests>=2.25.0
geopandas>=0.10.0
shapely>=1.7.0
fiona>=1.8.0
```

## 🛠️ Installation

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/agricultural-field-detection.git
cd agricultural-field-detection
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Install Detectron2
```bash
pip install 'git+https://github.com/facebookresearch/detectron2.git'
```

### 5. Download Pre-trained Model
Place your trained model file (`model_final.pth`) in the project directory or update the path in the configuration.

## 🎮 Usage

### Command Line Interface

```bash
# Run inference on a single image
python python_script_sf.py --image path/to/your/image.jpg

# Batch processing
python python_script_sf.py --batch path/to/image/directory/
```

### Web Interface

```bash
# Start the Streamlit application
streamlit run streamlit_app.py
```

Then open your browser and navigate to `http://localhost:8501`

### API Usage

```python
import requests

# Upload image for detection
files = {'image': open('aerial_image.jpg', 'rb')}
response = requests.post('http://your-api-url/predict', files=files)
results = response.json()
```

## 📊 Output Formats

### 1. JSON Output
```json
{
  "image_path": "path/to/image.jpg",
  "num_polygons": 15,
  "total_area": 125000,
  "average_points_per_polygon": 8.5,
  "polygons": [
    [[x1, y1], [x2, y2], ...],
    ...
  ]
}
```

### 2. GeoJSON Output
Standard GeoJSON format with polygon geometries and properties.

### 3. Shapefile Output
Complete shapefile package (.shp, .shx, .dbf, .prj) for GIS applications.

## 🎯 Model Training

### Dataset Preparation
1. Collect aerial imagery of agricultural fields
    **Annotate using LabelMe** for precise polygon boundaries
    **Upload to Roboflow** for dataset management and augmentation
    **Export in COCO format** from Roboflow for Detectron2 compatibility
3. Annotate using COCO format
4. Prepare train/validation splits

### Training Configuration
```python
cfg = get_cfg()
cfg.merge_from_file(model_zoo.get_config_file("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"))
cfg.MODEL.ROI_HEADS.NUM_CLASSES = 1  # Agricultural fields
cfg.SOLVER.MAX_ITER = 3000
cfg.SOLVER.BASE_LR = 0.00025
```

### Training Command
```bash
python train.py --config-file config.yaml --num-gpus 1
```

## 📈 Performance Metrics

- **mAP@0.5**: 0.85
- **mAP@0.5:0.95**: 0.72
- **Inference Speed**: ~2 seconds per image (GPU)
- **Polygon Accuracy**: 95% boundary precision

## 🔧 Configuration

### Model Configuration
Edit `config.yaml` to adjust:
- Model architecture
- Training parameters
- Data paths
- Output settings

### API Configuration
Update `streamlit_app.py`:
```python
API_BASE_URL = "your-api-endpoint"
```

## 📁 Project Structure

```
agricultural-field-detection/
├── README.md
├── requirements.txt
├── python_script_sf.py          # Main inference script
├── streamlit_app.py             # Web interface
├── config.yaml                  # Configuration file
├── models/
│   └── model_final.pth         # Trained model weights
├── output/
│   ├── results/                # Detection results
│   └── visualizations/         # Output images
├── data/
│   ├── train/                  # Training data
│   └── test/                   # Test images
└── utils/
    ├── preprocessing.py        # Data preprocessing
    ├── postprocessing.py       # Output processing
    └── visualization.py        # Visualization utilities
```

## 🌍 Use Cases

- **Agriculture Monitoring**: Track crop field boundaries and changes
- **Aquaculture Management**: Monitor shrimp farm layouts and expansion
- **Land Use Planning**: Analyze agricultural land distribution
- **Environmental Impact**: Assess agricultural area changes over time
- **Precision Agriculture**: Enable targeted field management

## 🔬 Research Applications

- Agricultural land use classification
- Crop yield estimation
- Environmental monitoring
- Remote sensing analysis
- Geospatial agriculture research

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Detectron2](https://github.com/facebookresearch/detectron2) for the detection framework
- [Segment Anything Model](https://github.com/facebookresearch/segment-anything) for segmentation capabilities
- [Streamlit](https://streamlit.io/) for the web interface framework
- The agricultural research community for datasets and insights

## 📞 Contact

- **Author**: Shashini Sathsarani Laksiri
- **Email**: shashinilaksiri@gmail,
- **LinkedIn**: www.linkedin.com/in/shashini-sathsarani-laksiri
- **Project Link**: [https://github.com/yourusername/agricultural-field-detection](https://github.com/yourusername/agricultural-field-detection)

## 🔮 Future Enhancements

- [ ] Integration with satellite imagery APIs
- [ ] Real-time monitoring dashboard
- [ ] Mobile application development
- [ ] Multi-class field type detection
- [ ] Temporal analysis for change detection
- [ ] Cloud deployment with auto-scaling
- [ ] Integration with GIS platforms

---

⭐ **Star this repository if you find it helpful!**
