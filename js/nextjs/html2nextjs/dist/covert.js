"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const htmltojsx_1 = __importDefault(require("htmltojsx"));
class Converter {
    constructor(createClass = false) {
        this.covert = (html) => {
            const jsx = this.converter.convert(html);
            return jsx;
        };
        this.converter = new htmltojsx_1.default({
            createClass: createClass,
        });
    }
}
exports.default = Converter;
;
