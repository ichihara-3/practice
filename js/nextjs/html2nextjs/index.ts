import fs from 'fs'
import Converter from './covert'
import { modify } from './modify'

const handleArgs = () => {
    if (process.argv.length < 3) {
        console.log('Usage: node index.mjs <file-path>')
        process.exit(1)
    }
    const filePath = process.argv[2]
    return filePath
}

function main() {
    const filePath = handleArgs()
    const html = fs.readFileSync(filePath, 'utf8')
    const converter = new Converter()

    const jsx = modify(converter.covert(html))
    console.log(jsx)
}

main()

