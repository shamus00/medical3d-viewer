#!/usr/bin/env python3
"""
Test CQ500 CT Dataset - Handle spaces in folder names
"""

from med_pipeline import MedicalTo3D
import os

def find_dicom_folder():
    """Find a folder with DICOM files, handling spaces in names"""
    base_path = "sample_data/cq500"
    
    # Get all directories (ignore ._ files)
    try:
        all_items = os.listdir(base_path)
        directories = [item for item in all_items 
                      if os.path.isdir(os.path.join(base_path, item)) 
                      and not item.startswith('._')]
        
        print(f"📂 Found {len(directories)} patient directories")
        
        # Try the first few directories
        for patient_folder in sorted(directories)[:3]:
            patient_path = os.path.join(base_path, patient_folder)
            print(f"🔍 Checking: '{patient_folder}'")
            
            # Walk through this patient's folders to find DICOM files
            for root, dirs, files in os.walk(patient_path):
                dcm_files = [f for f in files if f.endswith('.dcm')]
                if dcm_files:
                    print(f"  ✅ Found {len(dcm_files)} DICOM files in: {root}")
                    return root, len(dcm_files)
        
        print("❌ No DICOM files found in first few directories")
        return None, 0
        
    except Exception as e:
        print(f"❌ Error exploring directories: {e}")
        return None, 0

def test_cq500():
    print("🧠 Testing CQ500 CT Dataset (handling spaces)...")
    
    # Find DICOM files
    dicom_path, file_count = find_dicom_folder()
    
    if not dicom_path:
        print("❌ No DICOM files found!")
        return
    
    print(f"✅ Using: {dicom_path}")
    print(f"📄 DICOM files: {file_count}")
    
    try:
        # Initialize pipeline
        pipeline = MedicalTo3D()
        
        # Load DICOM series
        print("🔄 Loading DICOM series...")
        pipeline.load_dicom_series(dicom_path)
        
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
        patient_name = os.path.basename(os.path.dirname(dicom_path)).replace(' ', '_')
        output_file = f"outputs/cq500_skull_{patient_name}.stl"
        pipeline.export_stl(output_file)
        
        print("🎉 SUCCESS! Generated skull model:")
        print(f"   📄 Output: {output_file}")
        print(f"   🔺 Vertices: {pipeline.mesh.GetNumberOfPoints():,}")
        print(f"   📐 Triangles: {pipeline.mesh.GetNumberOfCells():,}")
        
        # File size
        if os.path.exists(output_file):
            size_mb = os.path.getsize(output_file) / (1024 * 1024)
            print(f"   💾 File size: {size_mb:.1f} MB")
            
        print(f"\n🎮 You can now view {output_file} in any 3D viewer!")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_cq500()
