# Pandoc file upload

This is a simple file-upload Flask app that hooks a file upload into a pandoc conversion. 

The example adds line-numbers to the uploaded docx using the supplied template
`templates\line-numbers.docx.`. Depending on requirements, this template could be changed to make
this application do other kinds of formatting as well.

Requirements:

* Docker (recommended)
* pandoc
* flask
