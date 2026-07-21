from main import Compiler
import sys

user_arguments = sys.argv[1:]

filename = user_arguments[0]
try:
  is_debug = True if user_arguments[1] == "True" else False
except IndexError:
  is_debug = False

c_config = {
  "path": filename,
  "is_debug": is_debug
}

compiler = Compiler(c_config)

compiler.parse(None)