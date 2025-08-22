from med_pipeline_fixed import MedicalTo3D
import os

def test_cq500():
    print("🧠 Testing CQ500 CT Dataset (Fixed VTK)...")
    
    dicom_path = "sample_data/cq500/CQ500CT0 CQ500CT0/Unknown Study/CT 4cc sec 150cc D3D on-2"
    
    try:
        pipeline = MedicalTo3D()
        
        print("🔄 Loading DICOM series...")
        pipeline.load_dicom_series(dicom_path)
        
        print("⚙️ Preprocessing CT...")
        pipeline.preprocess_ct()
        
        print("🦴 Segmenting skull...")
        pipeline.segment_threshold(0.4, 1.0)
        
        print("🎨 Generating 3D mesh...")
        pipeline.generate_mesh(smoothing_iterations=10)
        
        output_file = "outputs/skull_model.stl"
        pipeline.export_stl(output_file)
        
        print(f"\n🎉 SUCCESS! Created: {output_file}")
        
        size_mb = os.path.getsize(output_file) / (1024 * 1024)
        print(f"💾 File size: {size_mb:.1f} MB")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    test_cq500()
