@Grapes([
  @Grab(group='org.jsoup', module='jsoup', version='1.8.3'),
  @Grab(group='com.h2database', module='h2', version='1.4.190'),
  @GrabConfig(systemClassLoader = true)
])

import org.jsoup.Jsoup
import org.jsoup.nodes.Document
import org.jsoup.nodes.Element
import groovy.sql.*

Document document = Jsoup.connect("http://koji-k.github.io/groovy-tutorial/index.html").get()
List<String> links = document.select("a").collect {Element element ->
  "[${element.text()}](${element.attr("href")})"
}

// DBに接続(インメモリのh2)
def connection = Sql.newInstance("jdbc:h2:mem:", "org.h2.Driver")
// テーブルを作成
connection.execute 'CREATE table links(link clob)'

// INSERT
links.each {String link ->
  connection.execute("INSERT INTO links(link) VALUES(?)",[link])
}

// データをDBから取得して表示(H2を使っているので、TEXTがCLOB型になってちょっと特殊)
connection.rows("SELECT link from links").each {
  org.h2.jdbc.JdbcClob link = it[0]
  println link.getSubString(1, link.length() as Integer)
}
