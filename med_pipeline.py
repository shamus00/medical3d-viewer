#!/usr/bin/env python3
"""
Medical Scan to 3D GLTF Pipeline
Converts DICOM/NRRD medical images to interactive GLTF models
"""

import SimpleITK as sitk
import vtk
import numpy as np
import os
from pathlib import Path
import json
import base64
import struct

class MedicalTo3D:
    def __init__(self):
        self.image = None
        self.segmentation = None
        self.mesh = None
        
    def load_dicom_series(self, dicom_folder):
        """Load DICOM series from folder"""
        print(f"Loading DICOM series from {dicom_folder}")
        
        series_reader = sitk.ImageSeriesReader()
        dicom_names = series_reader.GetGDCMSeriesFileNames(dicom_folder)
        
        if not dicom_names:
            raise ValueError(f"No DICOM files found in {dicom_folder}")
            
        series_reader.SetFileNames(dicom_names)
        self.image = series_reader.Execute()
        print(f"Loaded image: {self.image.GetSize()} voxels")
        return self.image
    
    def load_nrrd(self, nrrd_path):
        """Load NRRD file"""
        print(f"Loading NRRD from {nrrd_path}")
        self.image = sitk.ReadImage(nrrd_path)
        print(f"Loaded image: {self.image.GetSize()} voxels")
        return self.image
    
    def preprocess_ct(self, window_min=-1000, window_max=4000):
        """Pre-process CT scan"""
        print("Pre-processing CT scan...")
        self.image = sitk.Cast(self.image, sitk.sitkFloat32)
        
        windower = sitk.IntensityWindowingImageFilter()
        windower.SetWindowMinimum(window_min)
        windower.SetWindowMaximum(window_max) 
        windower.SetOutputMinimum(0.0)
        windower.SetOutputMaximum(1.0)
        
        self.image = windower.Execute(self.image)
        return self.image
    
    def segment_threshold(self, lower_threshold=0.3, upper_threshold=1.0):
        """Segment using threshold"""
        print(f"Segmenting with threshold [{lower_threshold}, {upper_threshold}]")
        
        thresholder = sitk.BinaryThresholdImageFilter()
        thresholder.SetLowerThreshold(lower_threshold)
        thresholder.SetUpperThreshold(upper_threshold)
        thresholder.SetInsideValue(1)
        thresholder.SetOutsideValue(0)
        
        self.segmentation = thresholder.Execute(self.image)
        self.segmentation = self._keep_largest_component()
        
        smoother = sitk.BinaryMedianImageFilter()
        smoother.SetRadius([1, 1, 1])
        self.segmentation = smoother.Execute(self.segmentation)
        
        return self.segmentation
    
    def generate_mesh(self, smoothing_iterations=20):
        """Generate mesh using Marching Cubes"""
        print("Generating mesh with Marching Cubes...")
        
        vtk_image = self._sitk_to_vtk(self.segmentation)
        
        marching_cubes = vtk.vtkMarchingCubes()
        marching_cubes.SetInputData(vtk_image)
        marching_cubes.SetValue(0, 0.5)
        marching_cubes.Update()
        
        if smoothing_iterations > 0:
            print(f"Smoothing mesh ({smoothing_iterations} iterations)...")
            smoother = vtk.vtkWindowedSincPolyDataFilter()
            smoother.SetInputConnection(marching_cubes.GetOutputPort())
            smoother.SetNumberOfIterations(smoothing_iterations)
            smoother.SetPassBand(0.001)
            smoother.Update()
            self.mesh = smoother.GetOutput()
        else:
            self.mesh = marching_cubes.GetOutput()
        
        print(f"Generated mesh: {self.mesh.GetNumberOfPoints()} vertices")
        return self.mesh
    
    def export_gltf(self, output_path, embed_data=True):
        """Export mesh as GLTF"""
        print(f"Exporting GLTF to {output_path}")
        
        # Simple GLTF export - you can expand this
        writer = vtk.vtkSTLWriter()
        writer.SetFileName(output_path.replace('.gltf', '.stl'))
        writer.SetInputData(self.mesh)
        writer.Write()
        
        print("✅ Model exported (STL format for now)")
        return output_path
    
    def _keep_largest_component(self):
        """Keep only the largest connected component"""
        connected_filter = sitk.ConnectedComponentImageFilter()
        connected = connected_filter.Execute(self.segmentation)
        
        label_stats = sitk.LabelShapeStatisticsImageFilter()
        label_stats.Execute(connected)
        
        if label_stats.GetNumberOfLabels() == 0:
            return self.segmentation
            
        largest_label = max(label_stats.GetLabels(), 
                          key=lambda l: label_stats.GetPhysicalSize(l))
        
        threshold_filter = sitk.BinaryThresholdImageFilter()
        threshold_filter.SetLowerThreshold(largest_label)
        threshold_filter.SetUpperThreshold(largest_label)
        threshold_filter.SetInsideValue(1)
        threshold_filter.SetOutsideValue(0)
        
        return threshold_filter.Execute(connected)
    
    def _sitk_to_vtk(self, sitk_image):
        """Convert SimpleITK image to VTK"""
        array = sitk.GetArrayFromImage(sitk_image)
        vtk_array = vtk.util.numpy_support.numpy_to_vtk(array.ravel(), deep=True)
        
        vtk_image = vtk.vtkImageData()
        vtk_image.SetDimensions(sitk_image.GetSize())
        vtk_image.SetSpacing(sitk_image.GetSpacing())
        vtk_image.SetOrigin(sitk_image.GetOrigin())
        vtk_image.GetPointData().SetScalars(vtk_array)
        
        return vtk_image

def main():
    """Example usage"""
    print("🏥 Medical 3D Pipeline Ready!")
    print("\nExample usage:")
    print("pipeline = MedicalTo3D()")
    print("pipeline.load_nrrd('path/to/scan.nrrd')")
    print("pipeline.segment_threshold(0.3, 1.0)")
    print("pipeline.generate_mesh()")
    print("pipeline.export_gltf('output.gltf')")

if __name__ == "__main__":
    main()
