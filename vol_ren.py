#Xiangzhen Sun
#ISC5307
#Project 5 -Mummy

import vtk
import sys
from Tkinter import *
# Add this line and one after the renderer
style = vtk.vtkInteractorStyleTrackballCamera()

reader1 = vtk.vtkStructuredPointsReader()
reader1.SetFileName("mummy.128.vtk")

# Create transfer functions for opacity and color
opacityTransferFunction = vtk.vtkPiecewiseFunction()
opacityTransferFunction.AddPoint(0, 0.0)
opacityTransferFunction.AddPoint(50, 0.0)
opacityTransferFunction.AddPoint(55, 0.1)
opacityTransferFunction.AddPoint(80, 0.1)
opacityTransferFunction.AddPoint(100, 1.0)
opacityTransferFunction.AddPoint(120, 1.0)

colorTransferFunction = vtk.vtkColorTransferFunction()
colorTransferFunction.AddRGBPoint(0, 0.0, 0.0, 0.0)
colorTransferFunction.AddRGBPoint(64, 1.0, 0.0, 0.0)
colorTransferFunction.AddRGBPoint(128, 0.0, 0.0, 1.0)
colorTransferFunction.AddRGBPoint(156, 0.0, 1.0, 0.2)
colorTransferFunction.AddRGBPoint(192, 0.0, 1.0, 0.0)
colorTransferFunction.AddRGBPoint(255, 0.0, 0.2, 0.0)

# Create properties, mappers, volume actors, and ray cast function
volumeProperty = vtk.vtkVolumeProperty()
volumeProperty.SetColor(colorTransferFunction)
volumeProperty.SetScalarOpacity(opacityTransferFunction)
volumeProperty.ShadeOn()
volumeProperty.SetInterpolationTypeToLinear()
#volumeProperty.SetInterpolationTypeToNearest()

compositeFunction = vtk.vtkVolumeRayCastCompositeFunction()
volumeMapper = vtk.vtkVolumeRayCastMapper()
volumeMapper.SetInputConnection(reader1.GetOutputPort())
volumeMapper.SetVolumeRayCastFunction(compositeFunction)
volumeMapper.SetSampleDistance(0.5)
#volumeMapper.SetSampleDistance(1.0)
#volumeMapper.SetSampleDistance(8.0)
#volumeMapper.SetSampleDistance(0.2)

volume = vtk.vtkVolume()
volume.SetMapper(volumeMapper)
volume.SetProperty(volumeProperty)

# Create outline
outline = vtk.vtkOutlineFilter()
outline.SetInputConnection(reader1.GetOutputPort())

outlineMapper = vtk.vtkPolyDataMapper()
outlineMapper.SetInputConnection(outline.GetOutputPort())

outlineActor = vtk.vtkActor()
outlineActor.SetMapper(outlineMapper)
############################################################
eval("outlineActor.GetProperty()").SetColor(1, 1, 1)

# Okay now the graphics stuff
ren1 = vtk.vtkRenderer()
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren1)
renWin.SetSize(512, 512)

iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)
iren.SetInteractorStyle(style)

#ren1 AddActor outlineActor
ren1.AddVolume(volume)
ren1.SetBackground(0, 0, 0)
renWin.Render()

def TkCheckAbort(object_binding, event_name):
	foo = renWin.GetEventPending()
	if(foo != 0):
		renWin.SetAbortRender(1)

#renWin SetAbortCheckMethod {TkCheckAbort}
renWin.AddObserver("AbortCheckEvent", TkCheckAbort)

#iren SetUserMethod {wm deiconify .vtkInteract}
#iren.AddObserver("LeftButtonPressEvent", leftButtonPressEvent)
iren.Initialize()

frame = 0
w2if = vtk.vtkWindowToImageFilter()
writer = vtk.vtkPNGWriter()

def saveFrame():
	global frame
	name = "frame{:0>3}.png".format(frame)
	w2if.SetInput(renWin)
	writer.SetInputConnection(w2if.GetOutputPort())
	writer.SetFileName(name)
	writer.Write()
	frame = frame + 1
	name = "frame{:0>3}.png".format(frame)
	#.save configure -text [format "save %s" $name]
	save.configure(text = "save {0!s}".format(name))
	#save.config(text = ...)

def Quit():
	sys.exit()

save = Button(text = "save frame000.ppm", command = saveFrame)
quit = Button(text = "bye", command = Quit)
save.pack()
quit.pack()

#iren.Start()
mainloop()
