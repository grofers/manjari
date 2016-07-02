var module = angular.module("todoApp", ['ngRoute', 'ui.bootstrap']);
module.config(function($interpolateProvider, $httpProvider) {
    $interpolateProvider.startSymbol('[[').endSymbol(']]');
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
});

module.config(['$routeProvider',
    function($routeProvider) {
        $routeProvider.
        when('/users', {
            templateUrl: static_url + 'angular_code/partial_views/register.html',
            controller: 'RegisterController'
        }).
        when('/user/sessions', {
            templateUrl: static_url + 'angular_code/partial_views/login.html',
            controller: 'LoginController'
        }).
        when('/tasks', {
            templateUrl: static_url + 'angular_code/partial_views/tasks.html',
            controller: 'TaskController'
        }).
        when('/logout', {
            templateUrl: static_url + 'angular_code/partial_views/logout.html',
            controller: 'LogoutController'
        }).
        when('/', {
            templateUrl: static_url + 'angular_code/partial_views/initial.html',
        }).
        otherwise({
            redirectTo: '/'
        });
    }
]);

module.controller("RegisterController", function($scope, $http, $window) {

    $scope.register = function(user) {
        var data = $scope.user;
        $http.post("/api/v1/users/", data).success(function(data, status) {
            $window.location.href = '#/user/sessions';
        }).error(function(data, status) {
            console.log(data);

        })

    };

});

module.controller("LoginController", function($scope, $http, $window) {

    $scope.login = function(user) {
        var data = $scope.user;
        $http.post("/api/v1/user/sessions/", data).success(function(data, status) {

            $window.location.href = '#/tasks';

            console.log(data);
        }).error(function(data, status) {
            console.log(data);

        })

    };
});

module.controller("LogoutController", function($scope, $http) {


    $http.post("/api/v1/logout/").success(function(data, status) {

        console.log(data);
    }).error(function(data, status) {
        console.log(data);

    })


});

module.controller("TaskController", function($scope, $http, $filter, $timeout) {

    $scope.task_set = {}
    $scope.query = {}
    $scope.queryBy = '$'

    $scope.get_today_tasks = function() {
        $http.get("/api/v1/tasks/?q=1").success(function(response) {
            $scope.task_set = response.data.tasks;
            $scope.delete_value = 1;
        }).error(function(data, status) {
            console.log(data);
        })
    }
    $scope.get_today_tasks();

    $scope.get_week_tasks = function() {
        $http.get("/api/v1/tasks/?q=7").success(function(response) {
            $scope.task_set = response.data.tasks;
            $scope.delete_value = 2;
        }).error(function(data, status) {
            console.log(data);
        })
    }

    $scope.get_tasks = function() {
        $http.get("/api/v1/tasks/").success(function(response) {
            $scope.task_set = response.data.tasks;
            $scope.delete_value = 3;
        }).error(function(data, status) {
            console.log(data);
        })
    }

    $scope.toggle_showme = function() {
            $scope.showme = $scope.showme === true ? false: true;
    };

    $scope.toggle_showedit = function() {
            $scope.showdit = $scope.showdit === true ? false: true;
    };

    $scope.today = function() {
        return $scope.date = new Date();
    };
    $scope.today();
    $scope.showWeeks = true;

    $scope.clear = function() {
        return $scope.date = null;
    };

    $scope.disabled = function(date, mode) {
        return mode === 'day' && (date.getDay() === 0 || date.getDay() === 6);
    };

    $scope.toggleMin = function() {
        var _ref;
        return $scope.minDate = (_ref = $scope.minDate) != null ? _ref : {
            "null": new Date()
        };
    };
    $scope.toggleMin();
    $scope.open = function($event) {
        $event.preventDefault();
        $event.stopPropagation();
        return $scope.opened = true;

    };
      $scope.getDayClass = function(date, mode) {
    if (mode === 'day') {
      var dayToCheck = new Date(date).setHours(0,0,0,0);
      var currentDay = new Date().setHours(0,0,0,0);

        if (dayToCheck === currentDay) {
          return 'highlight-current-date'; 
        }
    }

    return '';
  };

    $scope.task_add = function(task) {
        $scope.today();
        var task_data =$scope.task;
        var date = task_data.date;
        if (date == null){
          $scope.fullDate = null;
        }
        else {
        var time = task_data.time;
        var d = new Date(date.getFullYear(), date.getMonth(), date.getDate(), time.getHours(), time.getMinutes());
        $scope.fullDate = d;
      }
        var data = {
            "description": task_data.description,
            "due_date": $scope.fullDate,
        };
        var defaultForm={
            description : "",
            date : $scope.today(),
            time : new Date()
        }
        $scope.task_form.$setPristine();
        $scope.task = angular.copy(defaultForm);
        $http.post("/api/v1/tasks/", data).success(function(data, status) {
            $scope.showadd = true;
            if ($scope.delete_value == 1) {
                $scope.get_today_tasks();
            }
            if ($scope.delete_value == 2) {
                $scope.get_week_tasks();
            } 
            if ($scope.delete_value == 3) {
                $scope.get_tasks();
            }
            $timeout(function() {
                $scope.showadd = false;
            }, 500);
        }).error(function(data, status) {
            console.log(data);
        })
    }

    $scope.getMyCtrlScope = function() {
         return $scope;   
    }



    $scope.task_done = function(id) {

    };
    $scope.task_delete = function(id) {
        $http.delete("/api/v1/tasks/" + id).success(function(response) {
            if ($scope.delete_value == 1) {
                $scope.get_today_tasks();
            }
            if ($scope.delete_value == 2) {
                $scope.get_week_tasks();
            } 
            if ($scope.delete_value == 3) {
                $scope.get_tasks();
            }
            $scope.showdel = true;
            $timeout(function() {
                $scope.showdel = false;
            }, 500);
        }).error(function(data, status) {
            console.log(data);
        })
    }
    $scope.dateOptions = {
        'year-format': "'yy'",
        'starting-day': 1
    };
    $scope.time = new Date();
    $scope.ismeridian = true;
});

module.controller("EditController", function($scope, $http, $timeout) {

    $scope.task_update = function(edit,task) {
      var new_task = $scope.edit;
      var id = $scope.task.id;
      var date = new_task.date;
      if (date == null) {
         $scope.fullDate = null;
      }
      else {
      var time = new_task.time;
      var d = new Date(date.getFullYear(), date.getMonth(), date.getDate(), time.getHours(), time.getMinutes());
      $scope.fullDate = d;
    }
      var data = {
            "description": new_task.description,
            "due_date": $scope.fullDate,
        };
      $http.put("/api/v1/tasks/"+ id +"/", data).success(function(data, status) {
            console.log(data);

            if ($scope.delete_value == 1) {
                $scope.get_today_tasks();
            }
            if ($scope.delete_value == 2) {
                $scope.get_week_tasks();
            } 
            if ($scope.delete_value == 3) {
                $scope.get_tasks();
            }
           $timeout(function() {
                $scope.toggle_showedit();
            }, 500);

        }).error(function(data, status) {
            console.log(data);
        })
    }
});


