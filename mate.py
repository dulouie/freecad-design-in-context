import FreeCAD
import FreeCADGui
import PartDesign

def isCoordinateSystem(selection):
	#if obj.isDerivedFrom('PartDesign::CoordinateSystem'):
	for obj in selection:
		if obj.TypeId != 'PartDesign::CoordinateSystem':
			return False
			print("False")
	return True
	print("True")

class MatePlacement:

	def getBodyOf(self, obj):
		return obj.getParentGeoFeatureGroup()

	def getLinkOf(self, obj):
			return obj.Parents[1][0]

	def getLinkElementOf(self, obj):
			return obj.InListRecursive[-1]

	def setRelationship(self, selection):
		self.parent = self.getBodyOf(selection[0])
		self.child = self.getBodyOf(selection[1])
		self.parent_mate = selection[0]
		self.child_mate = selection[1]

	def setExpression(self):
		self.expression = self.parent.Name + '.Placement * ' + self.parent_mate.Name + '.Placement * ' + self.child_mate.Name + '.Placement ^ (-1)'
		print(self.expression)
		#child.setExpression('LinkPlacement',expression)
		#child.setExpression('Placement',None)
		self.child.setExpression('Placement',self.expression)

	def clearExpression(self):
		self.child.setExpression('Placement',None)


doc = App.ActiveDocument
selection = FreeCADGui.Selection.getSelection()

if len(selection) == 2:
	if selection[0].TypeId == 'PartDesign::CoordinateSystem':
		if selection[1].TypeId == 'PartDesign::CoordinateSystem':
			mate = MatePlacement()
			mate.setRelationship(selection)
			mate.setExpression()
		else:
			print("Second selection is not a LCS")
	else:
		print("First selection is not a LCS")
else:
	print("Select exact two objects!")

doc.recompute()









