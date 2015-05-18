var personControllers = angular.module('personController', []);
  
personControllers.controller('personList', ['$scope', '$http', '$sce', '$resource', '$alert',
	function ($scope, $http, $sce, $resource, $alert) {
		console.log('personList init');
		
		Persons = $resource('/api/persons/:id', null, 
								{
									'update': { method:'PUT' }
								}
							);
		
		$http.get('/static/partials/personForm.html').success(function(data) {
			$scope.personInputTemplate = $sce.trustAsHtml(data);
		});
		
		$scope.reloadPersons = function(){
			Persons.query({}, function(users, getResponseHeaders){ 
				$scope.persons = users;
			});
		}
		
		$scope.reloadPersons();
		
		$scope.setActivePerson = function (idPerson) {
			Persons.get({id:idPerson}, function(user, getResponseHeaders){ 
				$scope.person = user;
			});
		}
		
		$scope.clearPerson = function(){ $scope.person = { id:null } };
		
		var successCallback = function(data, resp){
								$scope.reloadPersons();
								$scope.clearPerson();
							};
		
		
		var errorCallback = function(data, resp){
								var message = '';
								for(prop in data.data)
									message += prop + ':' + data.data[prop] + ' <br/>';
								$alert({title: 'Error', content: message, placement: 'top', type: 'danger', show: true});
							};
				
		$scope.savePerson = function(){
			if($scope.person && $scope.person !== 'undefined')
				if(!$scope.person.id || $scope.person.id === 'undefined' || $scope.person.id == 0)
					Persons.save($scope.person, successCallback, errorCallback);
				else
					Persons.update({id:$scope.person.id}, $scope.person,successCallback, errorCallback);
		};
	}]
);

personControllers.controller('personEdit', ['$scope', '$http', '$routeParams', 
	function ($scope, $http, $routeParams) {
		$http.get(path + '/persons/'+$routeParams.id).success(function(data) {
			$scope.person = data;
		})
	}]
);
