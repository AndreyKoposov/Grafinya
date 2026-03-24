function getOntologySubBtns() {
    return [
        {
            name: 'XML',
            id: 0,
            getContent: () => { return xmlPageContent },
            start: startXmlPage
        }
    ];
}
