class SomeClass {
  def someMethod() {
    "Groovy"
  }
}

def someClass = new SomeClass()
assert "groovy" == someClass.someMethod()
