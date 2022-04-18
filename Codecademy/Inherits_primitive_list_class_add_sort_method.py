class SortedList(list):
  def append(self, value):
    super().append(value)
    return self.sort()


new = SortedList([1, 8, 6])
print(new)
#print(new.append([1, 8, 6]))
print(new.append(3))
print(new)