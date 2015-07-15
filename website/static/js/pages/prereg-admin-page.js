'use strict';

var $osf = require('js/osfHelpers');
var ko = require('knockout');
var $ = require('jquery');
var Raven = require('raven-js');

var drafts;

// var Uploader = function(data) {

//     var self = this;

//     self.selectedFileName = ko.observable('no file selected');

//     $.extend(self, data);
// };

// module.exports = {
//     Uploader: Uploader
// };

ko.bindingHandlers.enterkey = {
    init: function (element, valueAccessor, allBindings, viewModel) {
        var callback = valueAccessor();
        $(element).keypress(function (event) {
            var keyCode = (event.which ? event.which : event.keyCode);
            if (keyCode === 13) {
                callback.call(viewModel);
                return false;
            }
            return true;
        });
    }
};

// should this not take data as a parameter? should it be a variable? should it not be in this file?
function adminView(data) {
    var self = this;
    //self.data = $.getJSON("/api/v1/drafts/");
    self.data = data.drafts;

    // REMOVE
    console.log(self.data);

    self.drafts = ko.pureComputed(function() {
        var row = self.sortBy();
        return data.drafts.sort(function (left, right) { 
            var a = deep_value(left, row).toLowerCase()
            var b = deep_value(right, row).toLowerCase()
            return a == b ? 0 : 
                (a < b ? -1 : 1); 
        });
    }, this);
    self.sortBy = ko.observable('registration_metadata.q1.value');

    // move these to an extension of the draft VM...if it fufills prereg?
    // variables for editing items in row
    self.edit = ko.observable(false);
    self.commentsSent = ko.observable('no');
    self.proofOfPub = ko.observable('no');
    self.paymentSent = ko.observable();
    self.notes = ko.observable('none');

    self.setSort = function(data, event) {
        self.sortBy(event.target.id);
    };

    self.highlightRow = function(data, event) {  
        var row = event.currentTarget;
        $(row).css("background","#E0EBF3"); 
    };

    self.unhighlightRow = function(data, event) {
        var row = event.currentTarget;
        $(row).css("background",""); 
    };

    self.formatTime = function(time) {
        var parsedTime = time.split(".");
        return parsedTime[0]; 
    };

    self.goToDraft = function(data, event) {
        if (self.edit() === false) {
            var path = "/project/" + data.branched_from.node.id + "/draft/" + data.pk;
            location.href = path;
        }
    };

    self.enlargeIcon = function(data, event) {
        var icon = event.currentTarget;
        $(icon).addClass("fa-2x");
    };

    self.shrinkIcon = function(data, event) {
        var icon = event.currentTarget;
        $(icon).removeClass("fa-2x");
    };

    self.editItem = function(item) {
        self.edit(true);
        var itemIndex = item[item.length - 1];
        var itemType = item.substring(0, item.length - 1);
        self.paymentSent(self.data[itemIndex].flags[itemType]);
        $('.'+item).hide();
        $('.input_' + item).show();
        $('.input_' + item).focus();
    };

    self.stopEditing = function(item) {
        self.edit(false);
        $('.'+item).show();
        $('.input_' + item).hide();
    };

}

// should this apply the binding? does it even need to get data?
$(document).ready(function() {
    var test = '/api/v1/drafts/';
    var request = $.ajax({
        url: test
    });
    request.done(function(data) {
    	$osf.applyBindings(new adminView(data), '#prereg-row');
    });
    request.fail(function(xhr, textStatus, error) {
        Raven.captureMessage('Failed to populate data', {
            url: test,
            textStatus: textStatus,
            error: error
        });
    });
});

var deepValue = function(obj, path){
    for (var i=0, path=path.split('.'), len=path.length; i<len; i++){
        obj = obj[path[i]];
    };
    return obj;
};
