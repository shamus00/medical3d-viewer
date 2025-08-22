#!/usr/bin/env python3
"""
Test CQ500 CT Dataset
"""

from med_pipeline import MedicalTo3D
import os

def test_cq500():
    print("🧠 Testing CQ500 CT Dataset...")
    
    # Path to your linked dataset
    ct_scan_path = "sample_data/cq500/CQ500CT0/Unknown Study/CT 4cc sec 150cc D3D on"
    
    if not os.path.exists(ct_scan_path):
        print("❌ CT scan path not found!")
        print("Available paths:")
        for root, dirs, files in os.walk("sample_data"):
            if any(f.endswith('.dcm') for f in files):
                print(f"   📁 {root}")
        return
    
    print(f"📂 Found CT scan folder: {ct_scan_path}")
    
    # Count DICOM files
    dcm_files = [f for f in os.listdir(ct_scan_path) if f.endswith('.dcm')]
    print(f"📄 Found {len(dcm_files)} DICOM files")
    
    try:
        # Initialize pipeline
        pipeline = MedicalTo3D()
        
        # Load DICOM series
        print("🔄 Loading DICOM series...")
        pipeline.load_dicom_series(ct_scan_path)
        
        # Preprocess CT (standard head CT window)
        print("⚙️ Preprocessing CT...")
        pipeline.preprocess_ct(window_min=-1000, window_max=4000)
        
        # Segment skull (bone threshold)
        print("🦴 Segmenting skull...")
        pipeline.segment_threshold(lower_threshold=0.4, upper_threshold=1.0)
        
        # Generate mesh
        print("🎨 Generating 3D mesh...")
        pipeline.generate_mesh(smoothing_iterations=15)
        
        # Export STL
        output_file = "outputs/cq500_skull.stl"
        pipeline.export_stl(output_file)
        
        print("✅ Success! Generated skull model:")
        print(f"   📄 Output: {output_file}")
        print(f"   🔺 Vertices: {pipeline.mesh.GetNumberOfPoints():,}")
        print(f"   📐 Triangles: {pipeline.mesh.GetNumberOfCells():,}")
        
        # File size
        if os.path.exists(output_file):
            size_mb = os.path.getsize(output_file) / (1024 * 1024)
            print(f"   💾 File size: {size_mb:.1f} MB")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_cq500()
