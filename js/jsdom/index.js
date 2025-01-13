import jsdom from 'jsdom';

const HTML = `
<!DOCTYPE html>
<html>
  <head>
    <meata charset="utf-8">
  </head>
  <body>
    <div id="app"></div>
    <table>
      <tr>
        <th>name</th>
        <th>age</th>
      </tr>
      <tr>
        <td>Tom</td>
        <td>20</td>
      </tr>
  </body>
</html>

`

function main() {
    const dom = new jsdom.JSDOM(HTML);
    console.log(dom.serialize())
}

main()