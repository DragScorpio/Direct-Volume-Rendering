#Xiangzhen Sun
#ISC5307
#Project 5 - Mummy

import vtk
import sys
from Tkinter import *
###### Read the Data File ######

reader = vtk.vtkStructuredPointsReader()
reader.SetFileName("mummy.128.vtk")

###### Transfer Functions ######

opacityTransferFunction = vtk.vtkPiecewiseFunction()
opacityTransferFunction.AddPoint(0, 0.0)
opacityTransferFunction.AddPoint(75, 0.0)
opacityTransferFunction.AddPoint(95, 0.0)
opacityTransferFunction.AddPoint(110, 0.4)
opacityTransferFunction.AddPoint(120, 0.6)
opacityTransferFunction.AddPoint(145, 1.0)
opacityTransferFunction.AddPoint(255, 1.0)

colorTransferFunction = vtk.vtkColorTransferFunction()
colorTransferFunction.AddRGBPoint(75.0, 0.4, 0.4, 0.4)
colorTransferFunction.AddRGBPoint(95.0, 0.8, 0.8, 0.8)
colorTransferFunction.AddRGBPoint(110.0, 0.6, 0.6, 0.6)
colorTransferFunction.AddRGBPoint(120.0, 0.6, 0.6, 0.6)
colorTransferFunction.AddRGBPoint(145.0, 0.4, 0.4, 0.4)
colorTransferFunction.AddRGBPoint(255.0, 0.2, 0.2, 0.2)

#Volume Properties

volumeProperty = vtk.vtkVolumeProperty()
volumeProperty.SetScalarOpacity(opacityTransferFunction)
volumeProperty.SetColor(colorTransferFunction)
volumeProperty.ShadeOn()

#Set Raycasting Variables

MIPFunction = vtk.vtkVolumeRayCastMIPFunction()
volumeMapper = vtk.vtkVolumeRayCastMapper()
volumeMapper.SetInputConnection(reader.GetOutputPort())
volumeMapper.SetVolumeRayCastFunction(MIPFunction)

volumeMapper.SetSampleDistance(0.5)
#volumeMapper.SetSampleDistance(1.0)
#volumeMapper.SetSampleDistance(2.0)
#volumeMapper.SetSampleDistance(4.0)

###### Create Volume ######

volume = vtk.vtkVolume()
volume.SetMapper(volumeMapper)
volume.SetProperty(volumeProperty)

###### Render, Window, Interactor ######

ren1 = vtk.vtkRenderer()
ren1.SetBackground(0, 0, 0)
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren1)
renWin.SetSize(512, 512)
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)

###### Borrow From camframe.tcl ######
frame = 0

w2if = vtk.vtkWindowToImageFilter()
writer = vtk.vtkPNGWriter()

def saveFrame():
	global frame
	name = "Frame{:0>3}.png".format(frame)
	w2if.SetInput(renWin)
	writer.SetInputConnection(w2if.GetOutputPort())
	writer.SetFileName(name)
	writer.Write()
	frame = frame + 1
	name = "Frame{:0>3}.png".format(frame)
	save.config(text = "save {0!s}".format(name))

def Quit():
    sys.exit()

#name = "frame{:0>3}.ppm"
save = Button(text = "Save Frame000.ppm", command = saveFrame)
quit = Button(text = "Quit", command = Quit)

###### Pack GUI Objects ######

save.pack()
quit.pack()

#def leftButtonPressEvent(self):
#	self.OnLeftButtonDown()
#	return

ren1.AddVolume(volume)
renWin.Render()
#iren.AddObserver("LeftButtonPressEvent", leftButtonPressEvent)
iren.SetDesiredUpdateRate(1.0)
iren.Initialize()
#iren.Start()
mainloop()
