var app = angular.module("personManager", ['ngRoute','mgcrea.ngStrap','personController','ngSanitize','angular-bind-html-compile', 'ngResource']);
var path = '/api';

app.config(['$routeProvider',
  function($routeProvider) {
    $routeProvider.
      when('/persons', {
        templateUrl: '/static/partials/personsView.html',
        controller: 'personList'
      }).
      when('/persons/:id', {
        templateUrl: '/static/partials/personForm.html',
        controller: 'personEdit'
      }).
      otherwise({
        redirectTo: '/persons'
      });
  }]);

/*, {}, {
		query:  {method:'GET', params:{personId:''}, isArray:true},
		post:   {method:'POST'},
		update: {method:'PUT', params: {personId: '@personId'}},
		remove: {method:'DELETE', params: {personId: '@personId'}}
    });*/