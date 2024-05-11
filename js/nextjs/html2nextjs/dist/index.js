"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const jsdom_1 = __importDefault(require("jsdom"));
const fs_1 = __importDefault(require("fs"));
const covert_1 = __importDefault(require("./covert"));
const modify = (jsx) => {
    const dom = new jsdom_1.default.JSDOM(jsx);
    const document = dom.window.document;
    document.getElementsByTagName;
    return jsx;
};
const handleArgs = () => {
    if (process.argv.length < 3) {
        console.log('Usage: node index.mjs <file-path>');
        process.exit(1);
    }
    const filePath = process.argv[2];
    return filePath;
};
function main() {
    const filePath = handleArgs();
    const html = fs_1.default.readFileSync(filePath, 'utf8');
    const converter = new covert_1.default();
    const jsx = modify(converter.covert(html));
    console.log(jsx);
}
main();
