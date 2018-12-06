import os
import numpy as np
from plymit import (
    Ply,
    PlyFormatOptions,
    ElementSpecification,
    ElementProperty,
    ElementPropertyType,
    ListProperty,
)


def load_ply(filename):
    """
    Load a PLY file as a mesh dictionary with the fields
    "faces", "vertices", "normals", "colors".
    Currently designed to only to parse models from the SIXD benchmark
    """

    ply = Ply(filename)

    # Stack all info into mesh
    vertices = []
    normals = []
    colors = []
    for v in ply.elementLists["vertex"]:
        vertices.extend([v.x, v.y, v.z])
        normals.extend([v.nx, v.ny, v.nz])
        colors.extend([v.red, v.green, v.blue, v.alpha])

    vertices = np.array(vertices, dtype=np.float32).reshape((-1, 3))
    normals = np.array(normals, dtype=np.float32).reshape((-1, 3))
    colors = np.array(colors, dtype=np.uint8).reshape((-1, 4))

    # faces
    faces = np.array(ply.elementLists["face"], dtype=np.uint).reshape((-1, 3))

    return {"faces": faces, "vertices": vertices, "normals": normals, "colors": colors}


def load(filename):
    """
    Load file.
    Supported formats:
        PLY
    """
    _, extension = os.path.splitext(filename)

    if extension.lower() != ".ply":
        raise NotImplementedError()

    return load_ply(filename)


def save_ply(obj, filename):
    """
    Save a PLY file. Follows the same element convention of the models used in
    the SIXD benchmark
    """

    vertex = ElementSpecification("vertex")
    n_vertex = 0

    has_vertices = "vertices" in obj and obj["vertices"] is not None
    has_normals = "normals" in obj and obj["normals"] is not None
    has_colors = "colors" in obj and obj["colors"] is not None
    has_faces = "faces" in obj and obj["faces"] is not None

    if has_vertices:
        vertex.add_property(ElementProperty("x", ElementPropertyType.FLOAT))
        vertex.add_property(ElementProperty("y", ElementPropertyType.FLOAT))
        vertex.add_property(ElementProperty("z", ElementPropertyType.FLOAT))
        n_vertex = len(obj["vertices"])

    if has_normals:
        vertex.add_property(ElementProperty("nx", ElementPropertyType.FLOAT))
        vertex.add_property(ElementProperty("ny", ElementPropertyType.FLOAT))
        vertex.add_property(ElementProperty("nz", ElementPropertyType.FLOAT))
        n_vertex = len(obj["normals"])

    if has_colors:
        vertex.add_property(ElementProperty("red", ElementPropertyType.UCHAR))
        vertex.add_property(ElementProperty("green", ElementPropertyType.UCHAR))
        vertex.add_property(ElementProperty("blue", ElementPropertyType.UCHAR))
        vertex.add_property(ElementProperty("alpha", ElementPropertyType.UCHAR))
        n_vertex = len(obj["colors"])

    face = ElementSpecification(
        "face",
        ListProperty(
            "vertex_index", ElementPropertyType.UCHAR, ElementPropertyType.INT
        ),
    )
    n_faces = len(obj["faces"]) if has_faces else 0

    ply = Ply()

    elements = []
    for i in range(n_vertex):
        data = []
        if has_vertices:
            data.extend(obj["vertices"][i])
        if has_normals:
            data.extend(obj["normals"][i])
        if has_colors:
            data.extend(obj["colors"][i])
        elements.append(vertex(*data))
    ply.add_bulk_elements(elements)

    elements = []
    for i in range(n_faces):
        elements.append(face(obj["faces"][i]))
    ply.add_bulk_elements(elements)

    ply.write(filename, PlyFormatOptions.ASCII)


def save(obj, filename):
    """
    Save file.
    Supported formats:
        PLY
    """
    _, extension = os.path.splitext(filename)

    if extension.lower() != ".ply":
        raise NotImplementedError()

    save_ply(obj, filename)
