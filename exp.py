class Compiler:
  def __init__(self, config):
    # given
    self.variables = {}

    # config
    self.path = config["path"]
    self.debug = config["is_debug"]

    if not self.path.endswith(".exp"):
      print("FILE NOT .EXP FILE")
      exit()

    with open(self.path, "r") as f:
      self.data = [item.strip("\n") for item in f.readlines()]
  def _say(self, message):
    if self.debug: print(f"\033[44m{message}\033[0m")
    else: print(message)

  def _redprint(self, message):
    print(f"\033[91m{message}\033[0m")

  def _get_indented(self, current_global_index):
    lines_after = self.data[current_global_index + 1:]
    while "" in [item.strip() for item in lines_after]:
      lines_after.remove("")
    targeted_indexes = []
    for index, line in enumerate(lines_after):
      if line.startswith("  "):
        targeted_indexes.append(index)
      else: break
    targeted_lines = [lines_after[i].strip() for i in targeted_indexes]
    return targeted_lines

  def _if(self, line):
    cgi = self.data.index(line) # current global index
    targeted_lines = self._get_indented(cgi)
    query = line.split("if ")[1].rstrip(":").split(" ")
    if "is" in query and "not" not in query:
      query = " ".join(query).split(" is ")
      for index, item in enumerate(query):
        if item in self.variables:
          query[index] = self.variables[item]

      if query[0] == query[1]:
        self.parse(targeted_lines)

    elif "is" in query and "not" in query:
      query = " ".join(query).split(" is not ")
      for index, item in enumerate(query):
        if item in self.variables:
          query[index] = self.variables[item]

      if query[0] != query[1]:
        self.parse(targeted_lines)
    elif "is" not in query and ">" in query:
      query = " ".join(query).split(" > ")
      for index, item in enumerate(query):
        if item in self.variables: query[index] = self.variables[item]

      if query[0] > query[1]: self.parse(targeted_lines)
    elif "is" not in query and "<" in query:
      query = " ".join(query).split(" < ")
      for index, item in enumerate(query):
        if item in self.variables: query[index] = self.variables[item]

      if query[0] < query[1]: self.parse(targeted_lines)

  def _loop(self, this_line, items):
    target_var = items[1]
    r = [int(item) for item in " ".join(items).split(" in ")[1].split("list(")[1].rstrip("):").split(", ")] # range
    lines_after = self.data[self.data.index(this_line) + 1:]
    i = self.data.index(this_line) # current global index
    targeted_lines = self._get_indented(i)

    for var in range(r[0], r[1] + 1):
      self.variables[target_var] = str(var)
      self.parse(targeted_lines)

  def _define_variable(self, var_name, value):
    """
    cases:
     - x = 5 + 5 + 5 + ...
     - x = 5 + 5
     - x = 3
     - x = y
    """
    split_values = value.split(" ")
    if any(item in "+-*/" for item in value):
      if any(item in self.variables for item in split_values):
        for index, item in enumerate(split_values):
          if item in self.variables:
            split_values[index] = self.variables[item]
        try:
          final = eval("".join(split_values))
        except Exception as e:
          self._redprint(e)
          exit()
        self.variables[var_name] = final
        return 0
      else:
        try: final = eval("".join(split_values))
        except Exception as e:
          self._redprint(e)
          exit()
        self.variables[var_name] = final
        return 0
    self.variables[var_name] = value.strip("\"")
    return 0

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
          current = current.replace(instance, str(self.variables[instance.strip("{").strip("}")]))
        self._say(current)
      else:
        self._say(message.strip("\""))

    elif letters[0] != "\"":
      try:
        self._say(self.variables[message])
      except Exception as e:
        self._redprint(f"{e} is not defined")
        exit()

  def _drop(self, line):
    target = line.split(" ")[1]
    del self.variables[target]

  def parse(self, given):
    if given == None: given = self.data
    # loop through all lines
    for line in given:
      if line.startswith(" "):
        first_word = line.split()[0]
        len_before_first_word = len(line.split(first_word)[0])
        items = line.split()
        if len_before_first_word % 2 != 0:
          self._redprint("Incorrect tabs")
          exit()
        for _ in range(len_before_first_word // 2):
          items.insert(0, "|TAB|")
      else:
        items = line.split()
      if line == "": continue

      if items[0] == ";":
        self._comment()
      
      elif items[0] == "print":
        self._print(" ".join(items).split("print ")[1])
      
      elif items[0] == "for":
        self._loop(line, items)

      elif items[0] == "|TAB|":
        pass

      elif items[0] == "drop":
        self._drop(line)

      elif items[0] == "if":
        self._if(line)

      else:
        self._define_variable(items[0], line.split(" = ")[1])

c_config = {
  "path": "test.exp",
  "is_debug": True
}

c = Compiler(config=c_config)

c.parse(None)
