$(document).ready(function () {
    $('a[data-toggle="tab"]').on('shown.bs.tab', function (e) {
        $.fn.dataTable.tables( {visible: true, api: true} ).columns.adjust();
    });

    var futuresTable = $('#futures-table').DataTable({
        "tag": "futures",
        "scrollY":         "70vh",
        "scrollCollapse": true,
        "paging": false,
        "select": "single",

        "language": {
            "url": "https://cdn.datatables.net/plug-ins/1.10.19/i18n/Russian.json",
            "decimal": ","
        },
        "saveState": true,
        // "searching": false,
        "ajax": "/polls/futures",
        "columns": [
            {
                "data": "pk"
            },
            { 
                "data": "fields.base"
            },
            {
                "data": "fields.exec_date",
                "type": "date"
            },
        ]
    });

    var tradesTable = $('#trades-table').DataTable({
        "tag": "trades",
        "scrollY":         "65vh",
        "scrollCollapse": true,
        "paging": false,
        "select": "single",

        "language": {
            "url": "https://cdn.datatables.net/plug-ins/1.10.19/i18n/Russian.json",
            "decimal": ","
        },
        "saveState": true,
        "ajax": "/polls/trades",
        "columns": [
            {
                "data": "pk"
            },
            {
                "data": "fields.torg_date",
                "type": "date"
            },
            {
                "data": "fields.day_end",
                "type": "date"
            },
            {
                "data": "fields.quotation",
                "className": "dt-right"
            },
            {
                "data": "fields.min_quot",
                "className": "dt-right"
            },
            {
                "data": "fields.max_quot",
                "className": "dt-right"
            },
            {
                "data": "fields.num_contr",
                "className": "dt-right"
            },
        ]
    });

    var renderNumber = function (data) {
        return (new Number(data)).toFixed(6);
    };

    var reportTable = $('#report-table').DataTable({
        "tag": "report",
        "scrollY":         "70vh",
        "scrollCollapse": true,
        "paging": false,

        "language": {
            "url": "https://cdn.datatables.net/plug-ins/1.10.19/i18n/Russian.json",
            "decimal": ","
        },
        "saveState": true,
        // "searching": false,
        "ajax": "/polls/report",
        "columns": [
            {
                "data": "pk"
            },
            {
                "data": "fields.quotation",
                "className": "dt-right"
            },
            { 
                "data": "fields.torg_date",
                "className": "dt-right"
            },
            {
                "data": "fields.rk",
                "render": renderNumber,
                "className": "dt-right"
            },
            {
                "data": "fields.xk",
                "render": renderNumber,
                "className": "dt-right"
            }
        ]
    });

    var summaryTable = $('#summary-table').DataTable({
        "scrollY": "70vh",
        "scrollCollapse": true,
        "paging": false,
        "language": {
            "url": "https://cdn.datatables.net/plug-ins/1.10.19/i18n/Russian.json",
            "decimal": ","
        },
        "select": "single",
        "saveState": true,
        "columns": [
            {
                "data": "pk"
            },
            {
                "data": "fields.count",
                "className": "dt-right",
            },
            {
                "data": "fields.avg",
                "className": "dt-right",
                "render": renderNumber,
            },
            {
                "data": "fields.stddev",
                "className": "dt-right",
                "render": renderNumber,
            },
            {
                "data": "fields.variance",
                "className": "dt-right",
                "render": renderNumber,
            },
            {
                "data": "fields.min",
                "className": "dt-right",
                "render": renderNumber,
            },
            {
                "data": "fields.max",
                "className": "dt-right",
                "render": renderNumber,
            },
            {
                "data": "fields.normal",
                "className": "dt-center"
            }
        ]
    });

    //futures-buttons-functions

    var displayError = function(id) {
        return function (xhr, textStatus, errorThrown) {
            var alert = $('#' + id);
            alert.text(xhr.responseText);
            alert.show();
        };
    };

    $("#futures-create-button").click(function (e) {
        $("#futures-create-alert").hide();
    });

    $("#futures-create-ok-button").click(function (e) {
        var code = $("#futures-create-code-input").val();
        var date = $("#futures-create-date-input").val();
        var request = {
            "code" : 'SU' + code + 'RMFS',
            "date" : date
        };
        $.ajax({
            "method": "POST",
            "url": "/polls/futures",
            "data": JSON.stringify(request),
            "success": function (data, status, jq) {
                $("#futuresCreateModal").modal('hide');
                futuresTable.ajax.reload();
            },
            "error": displayError('futures-create-alert')
        });
    });

    $("#futures-delete-ok-button").click(function (e) {
        var td = $("#futures-table tr.selected td:first-child()");
        $.ajax({
            "method": "delete",
            "url": "/polls/futures/" + td.text(),
            "success": function() {
                $("#futuresDeleteModal").modal('hide');
                futuresTable.ajax.reload();
            }
        });
    });

    $("#futures-edit-button").click(function (e) {
        $("#futures-edit-alert").hide();
        var td = $("#futures-table tr.selected td");
        var name = td[0].innerText;
        $("#futures-edit-original-name").val(name);
        $("#futures-edit-code-input").val(td[1].innerText.substring(2,7));
        $("#futures-edit-date-input").val(td[2].innerText);
    });

    $("#futures-edit-ok-button").click(function (e) {
        var originalName = $("#futures-edit-original-name").val();
        var code = $("#futures-edit-code-input").val();
        var date = $("#futures-edit-date-input").val();
        var request = {
            "code" : 'SU' + code + 'RMFS',
            "date" : date
        };
        $.ajax({
            "method": "put",
            "url": "/polls/futures/" + originalName,
            "data": JSON.stringify(request),
            "success": function() {
                $("#futuresEditModal").modal('hide');
                futuresTable.ajax.reload();
            },
            "error": displayError('futures-edit-alert')
        });
    });

     //trades-buttons-functions
    $("#trades-create-button").click(function (e) {
        $("#trades-create-alert").hide();
    });

    $("#trades-create-ok-button").click(function (e) {
        var name = $("#trades-create-name-input").val();
        var torg_date = $("#trades-create-torg-date-input").val();
        var day_end = $("#trades-create-day-end-input").val();
        var quotation = $("#trades-create-quotation-input").val();
        var max_quot = $("#trades-create-max-quot-input").val();
        var min_quot = $("#trades-create-min-quot-input").val();
        var num_contr = $("#trades-create-num-contr-input").val();
        var request = {
            "name" : name,
            "torg_date" : torg_date,
            "day_end" : day_end,
            "quotation" : quotation,
            "max_quot" : max_quot,
            "min_quot" : min_quot,
            "num_contr" : num_contr
        };
        $.ajax({
            "method": "POST",
            "url": "/polls/trades",
            "data": JSON.stringify(request),
            "success": function (data, status, jq) {
                $("#tradesCreateModal").modal('hide');
                tradesTable.ajax.reload();
            },
            "error": displayError('trades-create-alert')
        });
    });

    $("#trades-delete-ok-button").click(function (e) {
        var td = $("#trades-table tr.selected td");
        $.ajax({
            "method": "DELETE",
            "url": `/polls/trades/${td[1].innerText}/${td[0].innerText}`,
            "success": function() {
                $("#tradesDeleteModal").modal('hide');
                tradesTable.ajax.reload();
            }
        });
    });

    $("#trades-edit-button").click(function (e) {
        $('#trades-edit-alert').hide();
        var td = $("#trades-table tr.selected td");
        var name = td[0].innerText;
        $("#trades-edit-name-input").val(name);
        $("#trades-edit-original-name").val(name);
        var torg_date = td[1].innerText;
        $("#trades-edit-torg-date-input").val(torg_date);
        $("#trades-edit-original-torg-date").val(torg_date);
        $("#trades-edit-day-end-input").val(td[2].innerText);
        $("#trades-edit-quotation-input").val(td[3].innerText);
        $("#trades-edit-min-quot-input").val(td[4].innerText);
        $("#trades-edit-max-quot-input").val(td[5].innerText);
        $("#trades-edit-num-contr-input").val(td[6].innerText);
    });

    $("#trades-edit-ok-button").click(function (e) {
        var originalName = $("#trades-edit-original-name").val();
        var originalDate = $("#trades-edit-original-torg-date").val();
        var name = $("#trades-edit-name-input").val();
        var torg_date = $("#trades-edit-torg-date-input").val();
        var day_end = $("#trades-edit-day-end-input").val();
        var quotation = $("#trades-edit-quotation-input").val();
        var max_quot = $("#trades-edit-max-quot-input").val();
        var min_quot = $("#trades-edit-min-quot-input").val();
        var num_contr = $("#trades-edit-num-contr-input").val();
        var request = {
            "name" : name,
            "torg_date" : torg_date,
            "day_end" : day_end,
            "quotation" : quotation,
            "max_quot" : max_quot,
            "min_quot" : min_quot,
            "num_contr" : num_contr
        };
        $.ajax({
            "method": "PUT",
            "url": "/polls/trades/" + originalDate + "/" + originalName,
            "data": JSON.stringify(request),
            "success": function() {
                $("#tradesEditModal").modal('hide');
                tradesTable.ajax.reload();
            },
            "error": displayError('trades-edit-alert')
        });
    });

    $("#summary-button").click(function (e){
        $("#summary-alert").hide();
        var dateFrom = $("#summary-date-from-input").val();
        var dateTo = $("#summary-date-to-input").val();
        $.ajax({
            "method": "GET",
            "dataType": "json",
            "url": `/polls/summary?from=${dateFrom}&to=${dateTo}`,
            "success": function (data) {
                summaryTable.clear();
                summaryTable.rows.add(data);
                summaryTable.draw();
            },
            "error": displayError("summary-alert")
        });
    });

    $("#summary-table tbody").on("click", "tr", function () {
        var row = $(this);

        if (row.hasClass("selected")) {
            return;
        }

        var cells = row.children("td");
        var name = cells[0].innerText;
        var dateFrom = $("#summary-date-from-input").val();
        var dateTo = $("#summary-date-to-input").val();

        var url = `${window.location.origin}/polls/history?name=${name}&from=${dateFrom}&to=${dateTo}`;
        Highcharts.chart("summary-chart", {
            title: {
                text: `История фьючерса ${name}`
            },
            yAxis: {
                title: {
                    text: 'Величина изменения xk'
                }
            },
            data: {
                csvURL: url,
                firstRowAsNames: false,
                startRow: 1
            },
            series: [{
                name: 'Изменение процентной ставки за два дня'
            }]
        });                
    });

    var attachTextFilter = function (filterId, table, columnIndex) {
        var tableId = table.settings()[0].sTableId;

        var filter = $('#' + filterId);
        filter.on('change keyup clear', function() {
            table.draw();
        });

        $.fn.dataTable.ext.search.push(
            function(settings, data, dataIndex) {
                if (settings.sTableId != tableId) {
                    return true;
                }

                return (data[columnIndex] || "").includes(filter.val());
            });
        return filter;
    };

    var attachDateFilter = function (filterBaseId, table, columnIndex) {
        var tableId = table.settings()[0].sTableId;

        var filterFrom = $('#' + filterBaseId + '-from');
        var filterTo = $('#' + filterBaseId + '-to');
        filterFrom.change(function() { table.draw(); });
        filterTo.change(function() { table.draw(); });
        $.fn.dataTable.ext.search.push(
            function(settings, data, dataIndex) {
                if (settings.sTableId != tableId) {
                    return true;
                }

                var item = Date.parse(data[columnIndex]);

                var from = Date.parse(filterFrom.val());
                if (from && (item < from)) {
                    return false;
                }

                var to = Date.parse(filterTo.val());
                if (to && (to < item)) {
                    return false;
                }

                return true;
            });
    };

    var attachRangeFilter = function (filterBaseId, table, columnIndex) {
        var tableId = table.settings()[0].sTableId;

        var filterFrom = $('#' + filterBaseId + '-from');
        var filterTo = $('#' + filterBaseId + '-to');

        filterFrom.on('change keyup clear', function() { table.draw(); });
        filterTo.on('change keyup clear', function() { table.draw(); });
        
        $.fn.dataTable.ext.search.push(
            function(settings, data, dataIndex) {
                if (settings.sTableId != tableId) {
                    return true;
                }

                var item = parseFloat(data[columnIndex]);

                var from = parseFloat(filterFrom.val());
                if (!isNaN(from) && (item < from)) {
                    return false;
                }

                var to = parseFloat(filterTo.val());
                if (!isNaN(to) && (to < item)) {
                    return false;
                }

                return true;
            });
    };

    //futures filtres
    var futuresNameFilter = attachTextFilter('futures-name-filter', futuresTable, 0);
    var futuresCodeFilter = attachTextFilter('futures-code-filter', futuresTable, 1);
    attachDateFilter('futures-date-filter', futuresTable, 2);
    //trades filtres
    var tradesNameFilter = attachTextFilter('trades-name-filter', tradesTable, 0);
    attachDateFilter('trades-date-filter', tradesTable, 1);
    attachDateFilter('trades-expiration-filter', tradesTable, 2);
    attachRangeFilter('trades-quotation-filter', tradesTable, 3);
    attachRangeFilter('trades-min-quot-filter', tradesTable, 4);
    attachRangeFilter('trades-max-quot-filter', tradesTable, 5);
    attachRangeFilter('trades-quantity-filter', tradesTable, 6);
    //report filtres
    var reportNameFilter = attachTextFilter('report-name-filter', reportTable, 0);
    attachRangeFilter('report-quotation-filter', reportTable, 1);
    attachDateFilter('report-torg-date-filter', reportTable, 2);
    attachRangeFilter('report-rk-filter', reportTable, 3);
    attachRangeFilter('report-xk-filter', reportTable, 4);
});

var hash = window.location.hash;
hash && $('ul.nav a[href="' + hash + '"]').tab('show');

$('.nav-pills a').click(function (e) {
    $(this).tab('show');
    var scrollmem = $('body').scrollTop() || $('html').scrollTop();
    window.location.hash = this.hash;
    $('html,body').scrollTop(scrollmem);
});