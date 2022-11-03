List list = ["-5", "-4", null, "-3", "-2", null, "-1", "0", null, "1", "2", "3", null, "4", "5", null]

// Java8のOptional版
def optionalVersion = {->
  list.collect {
    Optional.ofNullable(it)
  }.collect {
    it.map{it.toInteger()}
  }.collect {
    it.filter{it % 2 == 0 && it > 0}
  }.collect {
    it.map{it * 2}
  }.collect {
    it.orElse(0)
  }.sum()
}

assert 12 == optionalVersion()

// Groovyのセーフナビゲーション版(エルビス演算子も利用)
def safeNaviVersion = {->
  list.collect {
    it?.toInteger()?:0
  }.findAll {
    it % 2 == 0 && it > 0
  }.collect {
    it * 2
  }.sum()
}

assert 12 == safeNaviVersion()
