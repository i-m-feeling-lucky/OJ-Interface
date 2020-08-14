require.config({ paths: { 'vs': '/static/node_modules/monaco-editor/min/vs' } });
require(['vs/editor/editor.main'], function () {

    // 初始化变量
    // var fileCounter = 0;
    let editor;
    let defaultCode = [
        '#include <stdio.h>\n',
        'int main(){',
        '   printf("Hello World!\\n");',
        '   return 0;',
        '}'
    ].join('\n');

    // 定义编辑器主题
    monaco.editor.defineTheme('myTheme', {
        base: 'vs',
        inherit: true,
        rules: [{ background: 'EDF9FA' }],
        // colors: { 'editor.lineHighlightBackground': '#0000FF20' }
    });
    monaco.editor.setTheme('myTheme');

    // 新建一个编辑器
    function newEditor(container_id, code, language) {
        let model = monaco.editor.createModel(code, language);
        editor = monaco.editor.create(document.getElementById(container_id), {
            model: model,
        });
        // alert(editor.getValue());
        // editorArray.push(editor);
        return editor;
    }

    // 新建一个 div
    function addNewEditor(code, language) {
        // var new_container = document.createElement('DIV');
        // new_container.id = "container-" + fileCounter.toString(10);
        // new_container.className = "container";
        // document.getElementById("root").appendChild(new_container);
        newEditor("EditorArea", code, language);
        // fileCounter += 1;
    }

    addNewEditor(defaultCode, 'c');

    // 语法高亮
    let languageSelected = document.querySelector('.language');
    languageSelected.onchange = function () {
        monaco.editor.setModelLanguage(window.monaco.editor.getModels()[0], languageSelected.value)
    }

    // 提交按钮
    let submit = document.getElementById("submit");
    submit.onclick = function () {
        console.log('Hello');
        document.getElementById('code').value = editor.getValue();
        console.log(document.getElementById('code').value);
    }
});
