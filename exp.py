class Compiler:
  def __init__(self, path):
    self.path = path
    self.variables = {}

    if not self.path.endswith(".exp"):
      print("FILE NOT .EXP FILE")
      exit()
  
  def _redprint(self, message):
    print(f"\033[91m{message}\033[0m")
  
  def _define_variable(self, var_name, value):
    """
    cases:
     - x = 5 + 5 + 5 + ...
     - x = 5 + 5
     - x = 3
     - x = y
    """
    if any(item in "+-*/" for item in value):
      if any(item in self.variables for item in value.split(" ")):
        ... # HERE
    self.variables[var_name] = value.strip("\"")

  def _comment(self):
    pass
  
  def _print(self, message):
    letters = list(message)

    if letters[0] == "\"":
      if "{" in message:
        letters = list(message.strip("\""))
        amount_left_brackets = message.count("{")
        amount_right_brackets = message.count("}")
        if amount_left_brackets != amount_right_brackets:
          self._redprint("Unclosed/extra '{' or '}'")
          exit()

        var_stack = []
        instances = []
        for index, letter in enumerate(letters):
          if letter == "{":
            lower = index
            from_current_letter = letters[lower:]
            final_target_var = "".join(from_current_letter[1:from_current_letter.index("}")])
            final_target_val = self.variables[final_target_var]
            var_stack.append(final_target_val)
            instances.append("{" + final_target_var + "}")

        current = "".join(letters)
        for instance in instances:
          current = current.replace(instance, self.variables[instance.strip("{").strip("}")])
        print(current)
      else:
        print(message.strip("\""))

    elif letters[0] != "\"":
      try:
        print(self.variables[message])
      except Exception as e:
        self._redprint(f"{e} is not defined")
        exit()

  def parse(self):
    # get all cleaned lines in the .exp file
    data = []
    with open(self.path, "r") as f:
      data = [item.strip("\n") for item in f.readlines()]
    
    # loop through all lines
    for line in data:
      items = line.split(" ")
      
      if line == "": continue

      if items[0] == ";":
        self._comment()
      
      elif items[0] == "print":
        self._print(" ".join(items).split("print ")[1])
      
      else:
        self._define_variable(items[0], line.split(" = ")[1])

c = Compiler("test.exp")

c.parse()
