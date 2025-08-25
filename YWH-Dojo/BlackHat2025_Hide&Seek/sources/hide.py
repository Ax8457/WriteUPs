msg = "Keep looking, there was nothing in the "
def selfDestruct():
    from os import remove
    remove("/tmp/lib/hide.py")    

def notfound():
  from random import choice
  return choice([
    "Nothing to be found here! &#x1F440;",
    "Well... I used to be here &#x1F3C3;&#x1F4A8;",
    "That hiding place is useless, I'm not hiding there &#x1F926;",
    "Give me five, you didn't found me! &#x1F91A;",
    "Don't walk in there! &#x1F62C;",
    "Didn't you already check that place? &#x1F928;",
    "Keep looking, I'm grabbing some tea meanwhile &#x1F375;",
  ])

def validate(value):
  return "{flag}" in value

def kitchen():
    return msg+"kitchen!"

def locker():
    return "You found me! - {flag}"

def basement():
    return msg+"basement!"

def garage():
    return msg+"garage!"
