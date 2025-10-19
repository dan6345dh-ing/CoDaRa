import numpy as np

# Datos: esfera (x^2 + y^2 + z^2)
def make_data(n=50):
    x, y, z = np.ogrid[-1:1:n*1j, -1:1:n*1j, -1:1:n*1j]
    return x**2 + y**2 + z**2

# --- Mayavi ---
def run_mayavi(data):
    from mayavi import mlab
    mlab.contour3d(data, contours=[0.5], opacity=0.5)
    mlab.title("Mayavi")
    print("[Mayavi] Cierra la ventana para continuar con VTK...")
    mlab.show()

# --- VTK ---
def run_vtk(data):
    from vtkmodules.vtkCommonDataModel import vtkImageData
    from vtkmodules.vtkFiltersCore import vtkContourFilter
    from vtkmodules.vtkRenderingCore import (
        vtkRenderWindow, vtkRenderWindowInteractor,
        vtkRenderer, vtkPolyDataMapper, vtkActor
    )
    from vtkmodules.util import numpy_support

    n = data.shape[0]
    img = vtkImageData()
    img.SetDimensions(n, n, n)

    flat = data.ravel(order="F")
    vtk_arr = numpy_support.numpy_to_vtk(flat)
    img.GetPointData().SetScalars(vtk_arr)

    contour = vtkContourFilter()
    contour.SetInputData(img)
    contour.SetValue(0, 0.5)

    mapper = vtkPolyDataMapper()
    mapper.SetInputConnection(contour.GetOutputPort())

    actor = vtkActor()
    actor.SetMapper(mapper)

    ren = vtkRenderer()
    ren.AddActor(actor)

    win = vtkRenderWindow()
    win.AddRenderer(ren)

    iren = vtkRenderWindowInteractor()
    iren.SetRenderWindow(win)

    print("[VTK] Cierra la ventana para terminar.")
    win.Render()
    iren.Start()

# --- Main ---
if __name__ == "__main__":
    data = make_data()
    run_mayavi(data)
    run_vtk(data)
