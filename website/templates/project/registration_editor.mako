<div id="registrationEditorScope">
    <select class="form-control" id="registrationSchemaSelect" data-bind="options: schemas,
                           optionsText: 'title',
                           optionsValue: 'id',
                           value: selectedSchemaId">
    </select>
    <div class='container'>
        <div class='row'>
            <div class='span8 col-md-12 columns eight large-8'>
                <h2 id="schemaTitle">Select an option above</h2>
                <p>
                    <ul class="nav navbar-nav" data-bind="foreach: schema().pages">
                        <li>
                            <a style="padding-bottom:0px;text-align:center;margin:2px;position:absolute;width:100%" data-bind="text: title,
                                click: $root.selectPage"></a>

                            <ul class="nav navbar-nav" data-bind="foreach: $root.schema().pages[$index()].questions">
                                <li><a style="padding-top:0px;padding-right:5px;position:relative;" data-bind="text: $root.schema().pages[0].questions[$index()].id, click: $root.selectQuestion"></a></li>
                            </ul>
                        </li>                
                    </ul>
                </p>
                <br />
                <br />
                <br />
                <div id="registrationEditor"></div>
                <button data-bind="css: {disabled: disableSave},                                 
                                 click: save" type="button" class="btn btn-success">Save</button>
            </div>
        </div>
    </div>
</div>
