"""
Module:     scipy_ex.py
Author:     Dennis Barger
Created:    12/4/2018

Description:
Example using scipy and numpy packages.  The numpy package is used to calculate
the product of two matrices.  The scipy package is used to calculate the smallest
convex set containing a list of random points on a plane.
"""

import numpy as np
from scipy.spatial import ConvexHull
import json

def main(event, context):
    try:
        matrix_a = np.random.randint(10, size = (4,4))
        matrix_b = np.random.randint(10, size = (4,4))
        matrix_p = matrix_a.dot(matrix_b)

        print("Product of two matrices\n: {}".format(matrix_p))

        num_points = 10
        points = np.random.rand(num_points, 2)

        hull = ConvexHull(points)
        hull_txt = "The smalles convex set containing all {} points has {} sides".format(num_points, len(hull.simplices))

        if hull_txt is None:
            response = "No hull text"
        else:
            response = hull_txt

        return {
            "status_code": 200,
            "body": json.dumps(response)
        }

    except Exception as e:
        return {
            "status_code": 400,
            "body": json.dumps(e)
        }

if __name__ == "__main__":
    event = {}
    context = {}
    response = main(event, context)
    print(response)
