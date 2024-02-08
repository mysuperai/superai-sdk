from typing import Dict, List, Tuple

from shapely.geometry import Polygon, box
from shapely.strtree import STRtree


def extract_polygon(annotation: dict) -> Tuple[int, Polygon]:
    """Extracts a Shapely Polygon from an annotation data model or a dictionary.

    Args:
        annotation: extract polygon from a general annotation data model, a dict or a tuple
    Returns:
        Tuple of page number the annotation is present in, and corresponding Shapely Polygon
    """

    if isinstance(annotation, tuple):
        page_number, bbox_bounds = annotation[0], annotation[-1]
        return page_number, box(*bbox_bounds)

    bbox = annotation["boundingBox"]
    page_number = annotation["pageNumber"] - 1

    annotation_poly = box(
        minx=bbox["left"],
        miny=bbox["top"],
        maxx=bbox["left"] + bbox["width"],
        maxy=bbox["top"] + bbox["height"],
    )
    return page_number, annotation_poly


def create_page_rtrees(
    annotations: List[dict],
) -> Tuple[Dict[Tuple[int, int], int], Dict[int, STRtree]]:
    """Creates per-page R-trees from a list of general annotation data models."""
    page_idxs = {}
    annotation_polys = {}
    for annotation_idx, annotation in enumerate(annotations):
        page_number, annotation_poly = extract_polygon(annotation)
        page_annotations = annotation_polys.setdefault(page_number, [])

        # Create mapping from R-tree index to original annotation index
        page_idxs[(page_number, len(page_annotations))] = annotation_idx
        page_annotations.append(annotation_poly)

    # Create a R-tree for every page containing all annotations in said page
    page_rtrees = {page_number: STRtree(annot_polys) for page_number, annot_polys in annotation_polys.items()}
    return page_idxs, page_rtrees


def intersect(box1, box2):
    """
    Tests whether two bounding boxes intersect.
    """
    # Determine the coordinates of the bounding boxes
    box1_top = box1["top"]
    box1_bottom = box1["top"] + box1["height"]
    box1_left = box1["left"]
    box1_right = box1["left"] + box1["width"]

    box2_top = box2["top"]
    box2_bottom = box2["top"] + box2["height"]
    box2_left = box2["left"]
    box2_right = box2["left"] + box2["width"]

    # Check for intersection
    if box1_left < box2_right and box1_right > box2_left and box1_top < box2_bottom and box1_bottom > box2_top:
        return True
    else:
        return False
