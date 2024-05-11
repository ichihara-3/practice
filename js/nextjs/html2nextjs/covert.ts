import HTMLToJSX from 'htmltojsx';

export default class Converter {
    private converter: HTMLToJSX;

    constructor(createClass: boolean = false) {
        this.converter = new HTMLToJSX({
            createClass: createClass,
        });
    }

    covert = (html: string) => {
        const jsx = this.converter.convert(html);
        return jsx;
    }
};
