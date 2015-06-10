from sklearn import tree
from createTestCase import *
from sklearn.externals.six import StringIO
import pydot 

class Tree(object):
	"""docstring for Tree"""
	def __init__(self):
		self.samples = None
		self.classifications = None
		self.clf = None

	def train(self):
		self.samples, self.classifications = retrieveTrainingData()
		self.clf = tree.DecisionTreeClassifier()
		self.clf = self.clf.fit(self.samples, self.classifications)

		return self.clf

	def printTreePDF(self, path = './tree.pdf'):
		if self.clf == None:
			raise NameError('Tree was not created!')
		else:
			dot_data = StringIO()
			tree.export_graphviz(self.clf, out_file=dot_data)
			graph = pydot.graph_from_dot_data(dot_data.getvalue())
			graph.write_pdf(path) 


	def predict(self, player1, player2, tournament):
		if self.clf == None:
			raise NameError('Tree was not created!')
		else:
			instance = createTrainingInstance(player1, player2, tournament)
			ans = self.clf.predict([instance])
			pct = self.clf.predict_proba([instance])
			return ans, instance, pct