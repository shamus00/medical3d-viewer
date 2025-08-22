#!/usr/bin/env python3
import vtk
import json
import base64
import struct
import os
import numpy as np

def stl_to_gltf(stl_path, gltf_path, color=[0.8, 0.8, 0.9]):
    print(f"Converting {stl_path} → {gltf_path}")
    
    reader = vtk.vtkSTLReader()
    reader.SetFileName(stl_path)
    reader.Update()
    
    mesh = reader.GetOutput()
    points = mesh.GetPoints()
    polys = mesh.GetPolys()
    
    vertices = []
    for i in range(points.GetNumberOfPoints()):
        point = points.GetPoint(i)
        vertices.extend([point[0], point[1], point[2]])
    
    indices = []
    polys.InitTraversal()
    idList = vtk.vtkIdList()
    while polys.GetNextCell(idList):
        if idList.GetNumberOfIds() == 3:
            indices.extend([idList.GetId(0), idList.GetId(1), idList.GetId(2)])
    
    normals = compute_normals(vertices, indices)
    
    vertex_data = struct.pack(f'{len(vertices)}f', *vertices)
    normal_data = struct.pack(f'{len(normals)}f', *normals)
    index_data = struct.pack(f'{len(indices)}I', *indices)
    
    gltf = {
        "asset": {"version": "2.0"},
        "scene": 0,
        "scenes": [{"nodes": [0]}],
        "nodes": [{"mesh": 0}],
        "meshes": [{"primitives": [{"attributes": {"POSITION": 0, "NORMAL": 1}, "indices": 2, "material": 0}]}],
        "materials": [{"pbrMetallicRoughness": {"baseColorFactor": color + [1.0], "metallicFactor": 0.1, "roughnessFactor": 0.8}}],
        "accessors": [
            {"bufferView": 0, "componentType": 5126, "count": len(vertices) // 3, "type": "VEC3", "min": [min(vertices[i::3]) for i in range(3)], "max": [max(vertices[i::3]) for i in range(3)]},
            {"bufferView": 1, "componentType": 5126, "count": len(normals) // 3, "type": "VEC3"},
            {"bufferView": 2, "componentType": 5125, "count": len(indices), "type": "SCALAR"}
        ],
        "bufferViews": [
            {"buffer": 0, "byteLength": len(vertex_data)},
            {"buffer": 1, "byteLength": len(normal_data)},
            {"buffer": 2, "byteLength": len(index_data)}
        ],
        "buffers": [
            {"uri": "data:application/octet-stream;base64," + base64.b64encode(vertex_data).decode(), "byteLength": len(vertex_data)},
            {"uri": "data:application/octet-stream;base64," + base64.b64encode(normal_data).decode(), "byteLength": len(normal_data)},
            {"uri": "data:application/octet-stream;base64," + base64.b64encode(index_data).decode(), "byteLength": len(index_data)}
        ]
    }
    
    with open(gltf_path, 'w') as f:
        json.dump(gltf, f, indent=2)
    
    print(f"✅ Done: {len(vertices)//3:,} vertices")

def compute_normals(vertices, indices):
    normals = [0.0] * len(vertices)
    
    for i in range(0, len(indices), 3):
        i0, i1, i2 = indices[i], indices[i+1], indices[i+2]
        
        v0 = np.array([vertices[i0*3], vertices[i0*3+1], vertices[i0*3+2]])
        v1 = np.array([vertices[i1*3], vertices[i1*3+1], vertices[i1*3+2]])
        v2 = np.array([vertices[i2*3], vertices[i2*3+1], vertices[i2*3+2]])
        
        normal = np.cross(v1 - v0, v2 - v0)
        length = np.linalg.norm(normal)
        if length > 0:
            normal /= length
        
        for idx in [i0, i1, i2]:
            normals[idx*3] += normal[0]
            normals[idx*3+1] += normal[1]
            normals[idx*3+2] += normal[2]
    
    for i in range(0, len(normals), 3):
        length = (normals[i]**2 + normals[i+1]**2 + normals[i+2]**2)**0.5
        if length > 0:
            normals[i] /= length
            normals[i+1] /= length
            normals[i+2] /= length
    
    return normals

def convert_all_models():
    models = [
        ("outputs/skull_model.stl", "outputs/skull.gltf", [0.95, 0.95, 0.85]),
        ("outputs/brain_tissue.stl", "outputs/brain.gltf", [0.83, 0.65, 0.65]),
        ("outputs/vessels.stl", "outputs/vessels.gltf", [0.8, 0.2, 0.2])
    ]
    
    print("🔄 Converting STL to GLTF...")
    
    for stl_file, gltf_file, color in models:
        if os.path.exists(stl_file):
            stl_to_gltf(stl_file, gltf_file, color)
        else:
            print(f"⚠️  {stl_file} not found")
    
    print("✅ Conversion complete!")

if __name__ == "__main__":
    convert_all_models()
