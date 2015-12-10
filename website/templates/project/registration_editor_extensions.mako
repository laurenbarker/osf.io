<!-- OSF Upload -->
<script type="text/html" id="osf-upload">
  <span data-bind="template: {data: $data, name: format}"></span>
</script>

<script type="text/html" id="osf-upload-open">
  <div id="selectedFile">File selected for upload:
    <span id="fileName" data-bind="text: extra().selectedFileName">no file selected</span>
    <button data-bind="visible: hasSelectedFile,
                       click: unselectFile"
            style="margin-left: 5px;"
            class="btn btn-xs btn-danger fa fa-times"></button>
  </div>
  <div data-bind="attr.id: $data.id, osfUploader">
    <div class="spinner-loading-wrapper">
      <div class="logo-spin logo-lg"></div>
      <p class="m-t-sm fg-load-message"> Loading files...  </p>
    </div>
  </div>
</script>

<script type="text/html" id="osf-upload-toggle">
  <div id="selectedFile">File selected for upload:
    <span id="fileName" data-bind="text: extra().selectedFileName">no file selected</span>
    <button data-bind="visible: hasSelectedFile,
                       click: unselectFile"
            style="margin-left: 5px;"
            class="btn btn-xs btn-danger fa fa-times"></button>
  </div>
  <a data-bind="click: toggleUploader">Attach File</a>
  <span data-bind="visible: showUploader">
    <div data-bind="attr.id: $data.id, osfUploader">
      <div class="spinner-loading-wrapper">
	<div class="logo-spin logo-lg"></div>
	<p class="m-t-sm fg-load-message"> Loading files...  </p>
      </div>
    </div>
  </span>
</script>

<!--Author Import -->
<script type="text/html" id="osf-author-import">
    <a data-bind="click: authorDialog, visible: contributors.length > 1">Import Contributors</a>

    <span data-bind="template: {data: $data, name: format}"></span>

</script>

<script type="text/html" id="importContributors">
    <div col-lg-12>
        <p>Select: <a data-bind="click: setContributorBoxes(true) " >All</a> | <a data-bind="click: setContributorBoxes(false)">None</a></p>
    </div>
    <div data-bind="foreach: {data: contributors, as: 'contrib'}">
        <div class="checkbox" id="contribBoxes">
            <label>
                <input type="checkbox" data-bind="value: contrib">
                <span data-bind="text: contrib"></span>
            </label>
        </div>
    </div>
    <p>If you would like to add contributors to your OSF project, you can do that on your <a href="${web_url_for('node_contributors', pid=node['id'])}">Contributors Page</a> </p>
</script>
