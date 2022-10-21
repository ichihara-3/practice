@Grab(group='org.jsoup', module='jsoup', version='1.8.3')

import org.jsoup.Jsoup
import org.jsoup.nodes.Document
import org.jsoup.nodes.Element
import org.jsoup.select.Elements

Document document = Jsoup.connect("http://koji-k.github.io/groovy-tutorial/index.html").get()
document.select("a").collect {Element element ->
  "[${element.text()}](${element.attr("href")})"
}.each {
  println it
}
