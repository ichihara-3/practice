List userList = [
  ["name": "aaa", age: 20, languages:["Java"]],
  ["name": "bbb", age: 25, languages:["Java", "PHP"]],
  ["name": "ccc", age: 30, languages:[]],
  ["name": "ddd", age: 35, languages:["Groovy"]],
]

userList.each {Map user ->
  println user.name
}

userList.each {Map user ->
  println "userName:${user.name}"
  user.languages.each {
    println it
  }
  println "" // 見やすくするために改行
}
