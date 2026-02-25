const ejs = require('ejs');

exports.handler = async (event, context) => {
    const formTemplate = `
  <form action="watermark" method="post" enctype="multipart/form-data">
    <input type="file" name="image" accept="image/*">
    <input type="text" name="watermarkText" placeholder="Watermark text">
    <input type="number" name="fontSize" placeholder="Font Size">
    <input type="color" name="fontColor" placeholder="Font Color">
    <button type="submit">Submit</button>
  </form>
  `;

    const renderedHtml = await ejs.render(formTemplate, {});

    return {
        statusCode: 200,
        headers: {'Content-Type': 'text/html'},
        body: renderedHtml
    };
};
