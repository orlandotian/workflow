    var app = angular.module('app', []);
    app.controller('controller', controller);
    function controller($scope, $http) {

        var MONTHS = ['JANUARY', 'FEBRUARY', 'MARCH', 'APRIL', 'MAI', 'JUNE', 'JULY', 'AUGUST', 'SEPTEMBER', 'OCTOBER', 'NOVEMBER', 'DECEMBER'];
        var WEEKDAYS = ['SUNDAY', 'MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY', 'SATURDAY'];
        init(new Date());

        function init(date) {
            $scope.defaultDate = date;
            $scope.year = $scope.defaultDate.getFullYear();
            $scope.monthIndex = $scope.defaultDate.getMonth();

            $scope.monthStr = monthStr;
            $scope.weekStr = weekStr;
            $scope.isDefaultDate = isDefaultDate;
            $scope.dayClick = dayClick;
            $scope.nextMonth = nextMonth;
            $scope.keydown = keydown;
            $scope.updateTask = updateTask;
            $scope.isToday = isToday;
            $scope.formateDate = formateDate;
            $scope.showDialog = showDialog;
            $scope.menuChecked = menuChecked;

            $scope.barStyle = {};

            $http.get('/currentUser').then(function (result) {
                $scope.currentUser = result.data;
            });
            $http.get('/myMembers').then(function (result) {
                $scope.members = result.data;
                for(var i = 0; i < $scope.members.length; i++) {
                    $scope.members[i].checked = (i == 0);
                }

            });

            var week = null;
            var weeks = [];
            var dayNum = new Date($scope.year, $scope.monthIndex, 0).getDate();
            for(var i = 1; i < dayNum + 1; i++) {
                var date = new Date($scope.year, $scope.monthIndex, i);
                var weekIndex = date.getDay();
                week = week || [null, null, null, null, null ,null, null];
                week[weekIndex] = {
                    day : i,
                    week : weekStr(3)[weekIndex],
                    date : date
                };
                if(weekIndex === 6 || i === dayNum) {
                    weeks.push(week);
                    week = null;
                }
            }

            $scope.weeks = weeks;

        }

        function nextMonth(del) {
            var date = $scope.defaultDate;
            date.setMonth(date.getMonth() + del)
            init(date)
        }

        function weekStr(size) {
            return WEEKDAYS.map(function(name) {
                return name.slice(0, size);
            })
        };

        function monthStr(index) {
            return MONTHS[index];
        }

        function isDefaultDate(day) {
            if (!day) { return; }
            return dateEqual(day.date, $scope.defaultDate);
        }

        function isToday(day) {
            if (!day) { return; }
            return dateEqual(day.date, new Date());
        }

        function dateEqual(date1, date2) {
            return (date1.getFullYear() ===  date2.getFullYear()) &&
                (date1.getMonth() ===  date2.getMonth()) &&
                (date1.getDate() ===  date2.getDate());
        }

        function dayClick(day) {
            if (!day) { return; }
            if(isDefaultDate(day)) {
                showDialog();
            } else {
                $scope.defaultDate = day.date;
            }
        }

        function showDialog() {
            if(!$scope.dialog.newTask || $scope.dialog.newTask == '') {
                $scope.dialog.addHidden = true;
            }
            $scope.dialog.hideDialog = false;
            if($scope.dialog.onlyToday) {
                $scope.dialog.tasks = $scope.events[formateDate($scope.defaultDate)];
            } else {
                tasks = [];
                angular.forEach($scope.events, function (event) {
                    tasks = tasks.concat(event)
                });
                $scope.dialog.tasks = tasks;
            }
        }

        function updateTask(task) {
            $http.post('/task/updateState',{id:task.id})
                .then(function (result) {
                    rebindEvent($scope.weeks);
                });
        }

        $scope.$watch('weeks', function (weeks) {
            rebindEvent(weeks);
        });

        function rebindEvent(weeks) {
            uids = [];
            angular.forEach($scope.members, function (member) {
                if(member.checked) {
                    uids.push(member.id);
                }
            });
            $http.post('/task', {year:$scope.year, month: $scope.monthIndex + 1, uid: uids})
                .then(function (result) {
                    events = result.data;
                    $scope.events = events;
                    angular.forEach(weeks, function (week) {
                        angular.forEach(week, function (day) {
                            if(!day) return;
                            day.events = events[formateDate(day.date)];
                        })
                    })
                    if($scope.dialog.hideDialog == false) {
                        showDialog()
                    }
                })
        }

        function keydown(event) {
            if(event.key == 'Enter' || event.keyCode == 13) {
                addEvent();
            }
        }

        function addEvent() {
            if ($scope.dialog.newTask && $scope.dialog.newTask != '') {
                $http.post('/task/add', {newTask:$scope.dialog.newTask, addTime:formateDate($scope.defaultDate)})
                    .then(function (result) {
                        $scope.dialog.newTask = ''
                        rebindEvent($scope.weeks);
                    })
            }
        }

        $scope.$watch('menuVisible', function (newVal) {
            if(newVal) {
                $scope.barStyle = {"left": "0%"}
            } else {
                $scope.barStyle = {"left": "-30%"}
            }
        })

        function menuChecked() {
            rebindEvent($scope.weeks);
        }
    };

    function formateDate(date) {
        return date.getFullYear() + "/"
            + ((date.getMonth()+1) < 10 ? '0' : '') + (date.getMonth()+1) + "/"
            + (date.getDate() < 10 ? '0' : '') + date.getDate();
    }



