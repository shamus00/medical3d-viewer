#!/usr/bin/env python3
"""
Volume renderer for internal anatomy
Shows brain tissue, vessels, etc. instead of just skull
"""

from med_pipeline_fixed import MedicalTo3D
import os
import SimpleITK as sitk

def create_brain_volume():
    print("🧠 Creating internal brain volume...")
    
    dicom_path = "sample_data/cq500/CQ500CT0 CQ500CT0/Unknown Study/CT 4cc sec 150cc D3D on-2"
    
    try:
        pipeline = MedicalTo3D()
        
        print("🔄 Loading DICOM series...")
        pipeline.load_dicom_series(dicom_path)
        
        print("⚙️ Preprocessing for brain tissue...")
        # Different windowing for soft tissue (brain)
        pipeline.preprocess_ct(window_min=-100, window_max=300)  # Brain window
        
        # Create multiple tissue layers
        print("🧠 Segmenting brain tissue...")
        
        # Brain tissue (gray/white matter)
        brain_threshold = sitk.BinaryThresholdImageFilter()
        brain_threshold.SetLowerThreshold(0.2)
        brain_threshold.SetUpperThreshold(0.7)
        brain_threshold.SetInsideValue(1)
        brain_threshold.SetOutsideValue(0)
        brain_seg = brain_threshold.Execute(pipeline.image)
        
        # Generate brain mesh
        pipeline.segmentation = brain_seg
        pipeline.generate_mesh(smoothing_iterations=5)
        pipeline.export_stl("outputs/brain_tissue.stl")
        print("✅ Brain tissue model: outputs/brain_tissue.stl")
        
        # Vessels/contrast (if present)
        vessel_threshold = sitk.BinaryThresholdImageFilter()
        vessel_threshold.SetLowerThreshold(0.7)
        vessel_threshold.SetUpperThreshold(1.0)
        vessel_threshold.SetInsideValue(1)
        vessel_threshold.SetOutsideValue(0)
        vessel_seg = vessel_threshold.Execute(pipeline.image)
        
        pipeline.segmentation = vessel_seg
        pipeline.generate_mesh(smoothing_iterations=3)
        pipeline.export_stl("outputs/vessels.stl")
        print("✅ Vessel model: outputs/vessels.stl")
        
        print("\n🎉 Created multiple anatomical models!")
        print("📁 Check outputs/ folder for:")
        print("   - brain_tissue.stl (gray/white matter)")
        print("   - vessels.stl (bright structures)")
        print("   - skull_model.stl (your original skull)")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    create_brain_volume()
