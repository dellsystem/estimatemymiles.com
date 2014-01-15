var module = angular.module('tools', []);
module.factory('APIService', function($http) {
   return {
        getRules: function(earningAirline, operatingAirline, fareClass) {
             return $http.get('/rules/' + earningAirline + '/' +
                              operatingAirline + '/' + fareClass + '/').then(
                    function(result) {
                        return result.data;
                    });
        }
   }
});


module.controller('ToolCtrl', function($scope, APIService) {
    $scope.alliance = null;
    $scope.earningAirline = null;
    $scope.earningPartners = [];
    $scope.operatingAirline = null;
    $scope.fareClass = null;

    $scope.isAllianceVisible = function(alliance) {
        return alliance == $scope.alliance;
    };

    $scope.isOperatingVisible = function(airline) {
        return $scope.earningPartners.indexOf(airline) >= 0;
    };

    $scope.scrollTo = function(desired) {
        setTimeout(function() {
            $('body').scrollTo(desired, 500);
        }, 100);
    };

    $scope.updateAlliance = function() {
        // Reset the earning alliance and partners
        $scope.earningAirline = null;
        $scope.earningPartners = [];
        $scope.operatingAirline = null;
        $scope.fareClass = null;
        $scope.scrollTo('#choose-earning');
    };

    $scope.updateEarning = function(earningPartners) {
        $scope.earningPartners = earningPartners;
        $scope.operatingAirline = null;
        $scope.fareClass = null;
        $scope.scrollTo('#choose-operating');
    };
    
    $scope.updateOperating = function() {
        $scope.scrollTo('#choose-fare-class');
        $scope.fareClass = null;
    };

    $scope.updateFareClass = function() {
        APIService.getRules($scope.earningAirline, $scope.operatingAirline,
            $scope.fareClass).then(function(rules) {
            $scope.rules = rules;
            $scope.scrollTo('#choose-rule');
        });
    };
});

$(document).ready(function() {
    $('.skip-to').on('click', function() {
        $('body').scrollTo($(this).attr('href'), 300);
        return false;
    });
});
