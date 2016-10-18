/*jshint globalstrict:true */
/*global angular:true */
'use strict';


/* Application Module */
angular.module('multiselect', [
  'multiselect.controllers',
  'multiselect.service',
  'elasticjs.service'
]);


/* Controller Module */
angular.module('multiselect.controllers', [])
  .controller('SearchCtrl', function($scope, translator, ejsResource, $timeout) {
    $scope.offset = 0;
    $scope.center_num = [];
    $scope.next= 'Next';
    $scope.poutof="";
    $scope.resultsArr = [];
    var number_hits = 0;
    $scope.bodyArr = [];
    var pieArrAnalysis = [];
    var pieArrWorkflow = [];
    var pieArrFile = [];
    var bodyStr;
    // point to your ElasticSearch server
    //var ejs = ejsResource('http://mzgephdfgnfskfpm.api.qbox.io');
    //var ejs = ejsResource('http://ucsc-cgl.org:9200');
    var ejs = ejsResource('http://localhost:8080');
    var index = 'analysis_file_index';
    var type = 'meta';
    // the fields we want to facet on
    var facets = ['center_name', 'program', 'project', 'workflow', 'analysis_type', 'specimen_type', 'file_type'];
    
    // for storing selected filters
    // format will be {field: [term1, term2], field2: [term1, term2]}
    var filters = {};

    // add's or removes a filter term
    $scope.handleFilter = function (field, term) {
      if (!_.has(filters, field)) {
        filters[field] = [];
      }

      var termIdx = _.indexOf(filters[field], term);
      if (termIdx === -1) {
        // add the filter
        filters[field].push(term);
      } else {
        // remove the filter
        filters[field].splice(termIdx, 1);
        if (filters[field].length === 0) {
          delete filters[field];
        }
      }
      $scope.offset=0;
      $scope.refresh($scope.offset)
      
    };

    // if a filter is applied or not
    $scope.hasFilter = function (field, term) {
      return (_.has(filters, field) && _.contains(filters[field], term));
    }
   
    
    // define our search function that will be called when a user
    // submits a search or selects a facet
    $scope.search = function(sizeVar) {
      // setup the request
      var request = ejs.Request()
        .indices(index)
        .types(type)
        .sort('_id') // sort by document id
        .query(ejs.MatchAllQuery()) // match all documents
        .size(sizeVar) //number of items on table
        .from($scope.offset*10); //starting point
      console.log("offset " + $scope.offset);
      // create the facets
      var facetObjs = _.map(facets, function (facetField) {
        return ejs.TermsFacet(facetField + 'Facet')
          .field(facetField)
          .allTerms(true);
      });
      
      // create the filters
      var filterObjs = _.map(filters, function (filterTerms, filterField) {
        return ejs.TermsFilter(filterField, filterTerms);
      });

      // apply the facets to the request
      // make sure to add any facet filters (to update counts)
      _.each(facetObjs, function (facetObj) {
        var facetFilters = _.filter(filterObjs, function (filterObj) {
          return facetObj.field() !== filterObj.field();
        });

        if (facetFilters.length === 1) {
          facetObj.facetFilter(facetFilters[0]);
        } else if (facetFilters.length > 1) {
          facetObj.facetFilter(ejs.BoolFilter().must(facetFilters));
        }
        request.facet(facetObj);
      });

      // apply search filters to the request
      if (filterObjs.length === 1) {
        request.filter(filterObjs[0]);
      } else if (filterObjs.length > 1) {
        request.filter(ejs.BoolFilter().must(filterObjs));
      }
      
      // execute the search
      $scope.restQry = translator(request._self());
      $scope.results = request.doSearch();
      $scope.resultsArr.push($scope.results);
      console.log($scope.resultsArr);
    };
      //for paging, refresh chart on 
      $scope.refresh = function(pcount){
         $scope.offset = $scope.offset+pcount;
         drawAnalysisChart();
         drawWorkflowChart();
         drawFileChart();
         $scope.search(10);
         $scope.resultloop();
         if($scope.offset === 0){
            $scope.back = "";
         }
         else{
            $scope.back = "Back";
         }
         if(($scope.offset*10)+10 > number_hits){
            $scope.next = "";
         }
         else{
            $scope.next = "Next";
         }
         if($scope.offset === 0){
            $scope.poutof = "";
            $scope.of = "";
         }
         else{
         $scope.poutof = Math.ceil((number_hits)/10);
         $scope.of = "of";
         }
      }
      
      $scope.search(10);
      
      //download as tsv
      var titledown = "Project\tDonor\tSpecimen\tType\tAnalysis Type\tWorkflow\tFile Type\tFile"
      $scope.downloadfile = function(numDown){
         var offsetTemp = $scope.offset;
         $scope.offset = 0;
         $scope.search(numDown);
         bodydown(numDown);
         var file = new File([titledown+"\n"+bodyStr], "results.tsv", {type: "text/plain;charset=utf-8"});
         saveAs(file);

      }
      
      //finds total number of hits
      $scope.resultloop = function(){
         //console.log($scope.resultsArr[0].$$v);
         //console.log($scope.resultsArr.length-1);
         number_hits = $scope.resultsArr[0].$$v.hits.total;
         while ($scope.resultsArr.length > 1){
            $scope.resultsArr.splice(index, 1);
         }
         return number_hits;
      }
      
      //download as tsv helper function
      var bodydown = function(numofhits){
         console.log("resultsArr ");
         console.log($scope.resultsArr);
         $scope.bodyArr = [];
         for (var i=0; i<numofhits; i++){
            var projectDown = $scope.resultsArr[0].$$v.hits.hits[i]._source.project;
            var donorDown = $scope.resultsArr[0].$$v.hits.hits[i]._source.donor;
            var specimen_typeDown = $scope.resultsArr[0].$$v.hits.hits[i]._source.specimen_type;
            var analysis_typeDown = $scope.resultsArr[0].$$v.hits.hits[i]._source.analysis_type;
            var workflowDown = $scope.resultsArr[0].$$v.hits.hits[i]._source.workflow;
            var file_typeDown =$scope.resultsArr[0].$$v.hits.hits[i]._source.file_type;
            var titleDown =$scope.resultsArr[0].$$v.hits.hits[i]._source.title;
            var download_idDown = $scope.resultsArr[0].$$v.hits.hits[i]._source.download_id;
            $scope.bodyArr.push(projectDown+"\t"+donorDown+"\t"+specimen_typeDown+"\t"+analysis_typeDown+"\t"+workflowDown+"\t"+file_typeDown+"\t"+titleDown+"\t"+download_idDown);
         }
         bodyStr = $scope.bodyArr[0];
         for (var i=1;i<numofhits;i++){
            bodyStr = bodyStr.concat("\n");
            bodyStr = bodyStr.concat($scope.bodyArr[i]);
         }
      }
      
      // turns pie data into array format
      $scope.piedata = function(pienum){
         pieArrAnalysis =[];
         var pieTemp = [];
         var pieTemp2 = [];
         for (var i=0; i<$scope.resultsArr[0].$$v.facets.analysis_typeFacet.terms.length; i++){
            pieTemp = [];
            pieTemp.push($scope.resultsArr[0].$$v.facets.analysis_typeFacet.terms[i].term);
            pieTemp.push($scope.resultsArr[0].$$v.facets.analysis_typeFacet.terms[i].count);
            pieTemp2.push(pieTemp);
         }
         for (var i=0; i<$scope.resultsArr[0].$$v.facets.analysis_typeFacet.terms.length; i++){
            pieArrAnalysis.push(pieTemp2[i]);
         }
         pieArrWorkflow =[];
         pieTemp2 = [];
         for (var i=0; i<$scope.resultsArr[0].$$v.facets.workflowFacet.terms.length; i++){
            pieTemp = [];
            pieTemp.push($scope.resultsArr[0].$$v.facets.workflowFacet.terms[i].term);
            pieTemp.push($scope.resultsArr[0].$$v.facets.workflowFacet.terms[i].count);
            pieTemp2.push(pieTemp);
         }
         for (var i=0; i<$scope.resultsArr[0].$$v.facets.workflowFacet.terms.length; i++){
            pieArrWorkflow.push(pieTemp2[i]);
         }
         pieArrFile =[];
         pieTemp2 = [];
         for (var i=0; i<$scope.resultsArr[0].$$v.facets.file_typeFacet.terms.length; i++){
            pieTemp = [];
            pieTemp.push($scope.resultsArr[0].$$v.facets.file_typeFacet.terms[i].term);
            pieTemp.push($scope.resultsArr[0].$$v.facets.file_typeFacet.terms[i].count);
            pieTemp2.push(pieTemp);
         }
         for (var i=0; i<$scope.resultsArr[0].$$v.facets.file_typeFacet.terms.length; i++){
            pieArrFile.push(pieTemp2[i]);
         }
         console.log(pieArrAnalysis);
         console.log(pieArrWorkflow);
         console.log(pieArrFile);
      }
      
      //pie chart maker
      var chart;
      google.charts.load('current', {'packages':['corechart']});
      google.charts.setOnLoadCallback(drawAnalysisChart);
      function drawAnalysisChart() {
         $scope.piedata(number_hits);
         var data = new google.visualization.DataTable();
         data.addColumn('string', 'Type');
         data.addColumn('number', 'Number');
         data.addRows(pieArrAnalysis);

         var options = {
            title: 'Analysis Type',
            width: 425,
            height: 300
         };

         chart = new google.visualization.PieChart(document.getElementById('piechartAnalysis'));

         chart.draw(data, options);
      }      
      google.charts.setOnLoadCallback(drawWorkflowChart);
      function drawWorkflowChart() {
         $scope.piedata(number_hits);
         var data = new google.visualization.DataTable();
         data.addColumn('string', 'Type');
         data.addColumn('number', 'Number');
         data.addRows(pieArrWorkflow);
         
         var options = {
            title: 'Workflow Type',
            width: 425,
            height: 300
         };

         chart = new google.visualization.PieChart(document.getElementById('piechartWorkflow'));

         chart.draw(data, options);
      }    
      google.charts.setOnLoadCallback(drawFileChart);
      function drawFileChart() {
         $scope.piedata(number_hits);
         var data = new google.visualization.DataTable();
         data.addColumn('string', 'Type');
         data.addColumn('number', 'Number');
         data.addRows(pieArrFile);
         
         var options = {
            title: 'File Type',
            width: 425,
            height: 300
         };

         chart = new google.visualization.PieChart(document.getElementById('piechartFile'));

         chart.draw(data, options);
      }    
      
      
  });

    
/* Service Module */
angular.module('multiselect.service', [])
  .factory('translator', function () {
    var RealTypeOf = function(v) {
      if (typeof(v) == "object") {
        if (v === null) return "null";
        if (v.constructor == [].constructor) return "array";
        if (v.constructor == (new Date()).constructor) return "date";
        if (v.constructor == (new RegExp()).constructor) return "regex";
        return "object";
      }
      return typeof(v);
    };

    var FormatJSON = function(oData, sIndent) {
      if (arguments.length < 2) {
        sIndent = "";
      }

      var sIndentStyle = "    ";
      var sDataType = RealTypeOf(oData);
      var sHTML = "";
      var iCount = 0;

      // open object
      if (sDataType == "array") {
        if (oData.length === 0) {
          return "[]";
        }
        sHTML = "[";
      } else {
        iCount = 0;
        _.each(oData, function() {
          iCount++;
          return;
        });
        if (iCount === 0) { // object is empty
          return "{}";
        }
        sHTML = "{";
      }

      // loop through items
      iCount = 0;
      _.each(oData, function(vValue, sKey) {
        if (iCount > 0) {
          sHTML += ",";
        }
        if (sDataType == "array") {
          sHTML += ("\n" + sIndent + sIndentStyle);
        } else {
          sHTML += ("\n" + sIndent + sIndentStyle + "\"" + sKey + "\"" + ": ");
        }

        // display relevant data type
        switch (RealTypeOf(vValue)) {
          case "array":
          case "object":
            sHTML += FormatJSON(vValue, (sIndent + sIndentStyle));
            break;
          case "boolean":
          case "number":
            sHTML += vValue.toString();
            break;
          case "null":
            sHTML += "null";
            break;
          case "string":
            sHTML += ("\"" + vValue + "\"");
            break;
          default:
            sHTML += ("TYPEOF: " + typeof(vValue));
        }

        // loop
        iCount++;
      });

      // close object
      if (sDataType == "array") {
        sHTML += ("\n" + sIndent + "]");
      } else {
        sHTML += ("\n" + sIndent + "}");
      }

      // return
      return sHTML;
    };

    return FormatJSON;
  });

