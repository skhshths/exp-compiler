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
  
  def _is_number(self, x):
    points = []
    for item in list(x):
      if item in "1234567890": points.append(True)
      else: points.append(False)
    return False if False in points else True

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
    x = " ".join(items).split(" in ")[1]
    if "list(" in x:
      r = [int(item) for item in " ".join(items).split(" in ")[1].split("list(")[1].rstrip("):").split(", ")] # range
      lines_after = self.data[self.data.index(this_line) + 1:]
      i = self.data.index(this_line) # current global index
      targeted_lines = self._get_indented(i)

      for var in range(r[0], r[1] + 1):
        self.variables[target_var] = str(var)
        self.parse(targeted_lines)
    else:
      target = " ".join(items).split(" in ")[1].rstrip(":")
      target_val = self._get_val(target)

      i = self.data.index(this_line)
      targeted_lines = self._get_indented(i)

      for var in target_val:
        self.variables[target_var] = str(var)
        self.parse(targeted_lines)

  def _get_val(self, var_name):
    if "[" not in var_name:
      return self.variables[var_name]
    else:
      initial_name = var_name.split("[")[0]
      index = var_name.split("[")[1].rstrip("]")
      return self.variables[initial_name][int(index)]

  def _define_variable(self, var_name, value):
    """
    cases:
     - x = 5 + 5 + 5 + ...
     - x = 5 + 5
     - x = 3
     - x = y
     - x = { 1, 2, 3, 4, 5, ... }
    """
    split_values = value.split(" = ")

    if ".insert" in value or ".without" in value or ".intersect" in value or ".reverse" in value or ".split_after" in value or ".split_before" in value:
      if ".insert" in value:
        target_val = value.split(".insert(")[1].rstrip(")")
        if target_val not in self.variables:
          if self._is_number(target_val): target_val = int(target_val)
          else: target_val = target_val.strip("\"")

          target_set = value.split(".insert(")[0]
          target_set_val = self._get_val(target_set)
          out = target_set_val
          out.append(target_val)

          self.variables[var_name] = out
          return 0
        else:
          target_set = value.split(".insert(")[0]
          target_set_val = self._get_val(target_set)

          target_val = self._get_val(target_val)

          out = target_set_val

          if type(target_val) == list:
            for item in target_val:
              out.append(item)
          else:
            out.append(target_val)

          self.variables[var_name] = out
          return 0
      elif ".without" in value:
        target_val = value.split(".without(")[1].rstrip(")")
        if self._is_number(target_val): target_val = int(target_val)
        else: target_val = target_val.strip("\"")

        target_set = value.split(".without(")[0]
        target_set_val = self._get_val(target_set)
        out = target_set_val
        while target_val in out:
          out.remove(target_val)
        
        self.variables[var_name] = out
        return 0
      elif ".intersect" in value:
        target_val = self._get_val(value.split(".intersect(")[1].rstrip(")"))
        base_val = self._get_val(value.split(".intersect(")[0])
        out = []
        for index, item in enumerate(target_val):
          out.append(base_val[index])
          out.append(item)
        
        self.variables[var_name] = out
        return 0
      elif ".reverse" in value:
        base_val = value.split(".reverse()")[0]
        r = self._get_val(base_val)[::-1]
        self.variables[base_val] = r
        return 0
      elif ".split_after" in value:
        target_index = int(value.split(".split_after(")[1].rstrip(")"))
        target_set = value.split(".split_after(")[0]
        target_set_val = self._get_val(target_set)
        out = target_set_val[target_index:]
        
        self.variables[var_name] = out
        return 0
      elif ".split_before" in value:
        target_index = int(value.split(".split_before(")[1].rstrip(")"))
        target_set = value.split(".split_before(")[0]
        target_set_val = self._get_val(target_set)
        out = target_set_val[:target_index]
        
        self.variables[var_name] = out
        return 0
    
    if "sum" in value or "max" in value or "min" in value or "len" in value:
      if "sum" in value:
        target = value.split("sum(")[1].rstrip(")")
        s = sum(self._get_val(target))
        self.variables[var_name] = s
        return 0
      if "max" in value:
        target = value.split("max(")[1].rstrip(")")
        m = max(self._get_val(target))
        self.variables[var_name] = m
        return 0
      if "min" in value:
        target = value.split("min(")[1].rstrip(")")
        m = min(self._get_val(target))
        self.variables[var_name] = m
        return 0
      if "len" in value:
        target = value.split("len(")[1].rstrip(")")
        l = len(self._get_val(target))
        self.variables[var_name] = l
        return 0
    elif any(item in "+-*/" for item in value):
      split_values = split_values[0].split(" ")
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
    elif "{" in value:
      split = value.lstrip("{ ").rstrip(" }").split(", ")
      try:
        final = [int(item) for item in split]
      # theres an imposter among us... (a string)
      except ValueError:
        final = []
        for item in split:
          if self._is_number(item): final.append(int(item))
          else: final.append(item.strip("\""))

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
            final_target_val = self._get_val(final_target_var)
            var_stack.append(final_target_val)
            instances.append("{" + final_target_var + "}")

        current = "".join(letters)
        for instance in instances:
          out = self._get_val(instance.strip("{").strip("}"))
          current = current.replace(instance, str(out))
        self._say(current)
      else:
        self._say(message.strip("\""))

    elif letters[0] != "\"":
      try:
        self._say(self._get_val(message))
      except Exception as e:
        self._redprint(f"{e} is not defined")
        exit()

  def _drop(self, line):
    target = line.split(" ")[1]
    del self.variables[target]

  def parse(self, given):
    if given is None: given = self.data
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

if __name__ == "__main__":
  c_config = {
    "path": "test.exp",
    "is_debug": True
  }

  c = Compiler(config=c_config)

  c.parse(None)