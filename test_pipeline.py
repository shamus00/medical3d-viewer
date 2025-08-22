#!/usr/bin/env python3
"""
Test script for Medical 3D Pipeline
"""

from med_pipeline import MedicalTo3D
import os

def test_pipeline():
    """Test the pipeline with dummy data"""
    print("🧪 Testing Medical 3D Pipeline...")
    
    # Check if we have sample data
    sample_files = []
    if os.path.exists('sample_data'):
        for file in os.listdir('sample_data'):
            if file.endswith(('.nrrd', '.dcm', '.nii', '.nii.gz')):
                sample_files.append(os.path.join('sample_data', file))
    
    if not sample_files:
        print("📁 No sample data found in sample_data/ folder")
        print("   Add some NRRD, DICOM, or NIfTI files to test the pipeline")
        return
    
    print(f"📂 Found {len(sample_files)} sample files")
    
    # Test with first file
    test_file = sample_files[0]
    print(f"🔬 Testing with: {test_file}")
    
    try:
        pipeline = MedicalTo3D()
        
        # Load based on file type
        if test_file.endswith('.dcm'):
            # For DICOM, pass the directory
            dicom_dir = os.path.dirname(test_file)
            pipeline.load_dicom_series(dicom_dir)
            pipeline.preprocess_ct()
        else:
            # For NRRD/NIfTI
            pipeline.load_nrrd(test_file)
        
        # Process
        pipeline.segment_threshold(0.3, 0.8)
        pipeline.generate_mesh(smoothing_iterations=10)
        
        # Export
        output_file = f"outputs/test_model_{os.path.basename(test_file)}.stl"
        pipeline.export_gltf(output_file)
        
        print(f"✅ Test completed! Output: {output_file}")
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        print("💡 This is normal if you don't have proper medical scan files yet")

if __name__ == "__main__":
    test_pipeline()
