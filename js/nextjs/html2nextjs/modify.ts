import jsdom from 'jsdom';

class Modifier {
    private dom: jsdom.JSDOM;
    private document: Document;

    constructor() {
        this.dom = new jsdom.JSDOM(jsx);
        this.document = this.dom.window.document;
    }


}

export const modify = (jsx: string) => {
    const dom = new jsdom.JSDOM(jsx);
    const document = dom.window.document;
    document.getElementsByTagName;

    return jsx;
};
