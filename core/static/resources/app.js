var app = angular.module('gitcompare', []);

function Ctrl($scope, $http) {

    $scope.repository = [];

    $scope.submit = function() {
        var httpRequest = $http({
            method: 'GET',
            url: '/api?slugs=' + $scope.repository_slugs,

        }).success(function(data, status) {
            $scope.repository = data.result;
        });

    };

}