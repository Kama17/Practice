class Node():
	def __init__(self, data = None):
		self.data = data
		self.next_node = None



class LL():
	def __init__(self):
		self.head_node = Node()

	def add_node(self, new_value):
		new_node = Node(new_value)
		curr_node = self.head_node

		if curr_node:
			while curr_node.next_node != None:
				curr_node = curr_node.next_node

			curr_node.next_node = new_node
		else:
			sefl.head_node = new_node

	def show(self):
		temp_node = self.head_node

		while temp_node.next_node != None:
			print(temp_node.data, end = " --> ")
			temp_node = temp_node.next_node

		print(temp_node.data, end = " --> ")
		print("End node")


ll = LL()

ll.add_node(1)
ll.add_node(2)
ll.add_node(3)
ll.add_node(4)
ll.add_node(5)
ll.add_node(6)

ll.show()
