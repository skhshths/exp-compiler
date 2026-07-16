# exp-compiler
part 2

## comments
#### ; this is a comment <- add a ';' before every commented line.

## variables
#### x = 5
#### print x <- prints 5
#### x = "hello world"
#### print x <- prints "hello world" (without quotes)

## printing to the console
#### { print "hello" } <- prints "hello" to the console
#### { print x } <- prints whatever value is stored in x AS A STRING (very important)
#### { print "i am {x} years old" } <- prints: i am {whatever x is} years old. this entire thing is a string

## for loops
#### { for x in list(0, 5):
####   print x } <- prints all values of 0 through 5 (double inclusive)

## if statements
#### if x is 5:
#### if x is not 5:
#### if x > 5:
#### if x < 5:
#### For all 4, code indented after only runs if statement is true.

## dropping
#### x = 5 <- initializes x
#### print x <- prints 5
#### drop x <- erases x from memory
#### print x <- var not defined error
