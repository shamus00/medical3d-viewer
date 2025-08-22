# 🏥 Medical 3D Pipeline

Convert medical scans (CT, MRI, etc.) into interactive 3D models for web viewing.

## Quick Start

1. **Activate environment:**
   ```bash
   source medical3d_env/bin/activate  # Linux/Mac
   # OR
   medical3d_env\Scripts\activate     # Windows
   ```

2. **Run the starter:**
   ```bash
   python start.py
   ```

3. **Test with your data:**
   - Put DICOM/NRRD files in `sample_data/`
   - Choose option 1 in the starter menu

## Project Structure

```
medical3d_pipeline/
├── med_pipeline.py      # Main processing pipeline
├── test_pipeline.py     # Test script
├── start.py            # Interactive starter
├── requirements.txt    # Python dependencies
├── sample_data/       # Your medical scan files
├── outputs/          # Generated 3D models
└── medical3d_env/    # Python virtual environment
```

## Usage Examples

```python
from med_pipeline import MedicalTo3D

# Basic workflow
pipeline = MedicalTo3D()
pipeline.load_nrrd("scan.nrrd")
pipeline.segment_threshold(0.3, 0.8)
pipeline.generate_mesh()
pipeline.export_gltf("model.gltf")
```

Happy 3D modeling! 🚀
