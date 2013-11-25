$(document).ready(function () {
    $('#traveling-airline').delegate('li', 'click', function () {
        $('#fare-class,#earning-airline,#mileage-table').hide();
        $('#fare-class .selected,#earning-airline .selected').removeClass(
            'selected');
        $('#earning-airline').hide();

        var airline = $(this).data('airline');

        // Add the selected class, remove it from the previous selection
        $('#traveling-airline .selected').removeClass('selected');
        $(this).addClass('selected');

        $.get('/api/fareclasses/' + airline + '/', function (fareClasses) {
            var gridHTML = [];
            var i, fareClass;

            for (i in fareClasses) {
                fareClass = fareClasses[i];
                gridHTML.push('<li data-pk="' + fareClass.pk + '">' +
                    fareClass.class_code + '</li>');
            }

            $('#fare-class ul').html(gridHTML.join(''));

            $('#fare-class').slideDown(200, function () {
                $.scrollTo('#fare-class', 300);
            });
        });
    });

    var mileageData;

    $('#fare-class').delegate('li', 'click', function () {
        $('#earning-airline,#mileage-table').hide();
        var fareClass = $(this).data('pk');
        $('#fare-class .selected').removeClass('selected');
        $('#earning-airline .selected').removeClass('selected');
        $(this).addClass('selected');

        // Hide the airlines that we can't earn with
        var listItems = $('#earning-airline li');
        listItems.hide();

        $.get('/api/mileages/' + fareClass + '/', function (airlines) {
            var pk, airline;

            for (pk in airlines) {
                airline = airlines[pk];

                // Show this airline
                listItems.filter('[data-airline="' + pk + '"]').show();
            }

            mileageData = airlines;

            $('#earning-airline').slideDown(200, function () {
                $.scrollTo('#earning-airline', 300);
            });
        });
    });

    $('#earning-airline').delegate('li', 'click', function () {
        $('#mileage-table').hide();
        var pk = $(this).data('airline');
        $('#earning-airline .selected').removeClass('selected');
        $(this).addClass('selected');

        var airline = mileageData[pk];

        // Edit the h2
        $('#frequent-flyer-program').text(airline.program);

        // Fill in the table
        $('#qualifying-miles').text(airline.qualifying_miles);
        $('#qualifying-segments').text(airline.qualifying_segments);
        var i, mileage;
        var tableHTML = [];
        var mileages = airline.mileages;
        for (i in mileages) {
            mileage = mileages[i];
            tableHTML.push('<tr><td>' + mileage.fare_name + '</td>' +
                '<td>' + mileage.accrual_factor + '</td>' +
                '<td>' + mileage.minimum_miles + '</td>' +
                '<td>' + mileage.qualifying_miles + '</td>' +
                '<td>' + mileage.qualifying_segments + '</td>' +
                '<td>' + mileage.restrictions + '</td></tr>');
        }
        $('#mileage-table tbody').html(tableHTML.join(''));

        // Show the table
        $('#mileage-table').slideDown(200, function () {
            $.scrollTo('#mileage-table', 300);
        });
    });
});
