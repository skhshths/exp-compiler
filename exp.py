class Compiler:
  def __init__(self, path):
    self.path = path
    if not self.path.endswith(".exp"):
      print("FILE NOT .EXP FILE")
      exit()
    
  def parse(self):
    # get all cleaned lines in the .exp file
    data = []
    with open(self.path, "r") as f:
      data = [item.strip("\n") for item in f.readlines()]
    
    # loop through all lines
    for line in data:
      items = line.split(" ")
      print(items)
    
c = Compiler("test.exp")

c.parse()