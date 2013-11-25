$(document).ready(function () {
    $('#traveling-airline').delegate('li', 'click', function () {
        $('#fare-class').hide();
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

            $('#fare-class').slideDown();
        });
    });

    $('#fare-class').delegate('li', 'click', function () {
        $('#earning-airline').hide();
        var fareClass = $(this).data('pk');
        $('#fare-class .selected').removeClass('selected');
        $(this).addClass('selected');

        $.get('/api/mileages/' + fareClass + '/', function (airlines) {
            var i, airline, mileages, numMileages, rowHTML, j, mileage, k;
            var tableHTML = [];

            for (i in airlines) {
                airline = airlines[i];
                mileages = airline.mileages;
                numMileages = mileages.length;
                rowHTML = [];

                for (j in mileages) {
                    mileage = mileages[j];
                    rowHTML.push('<td>' + mileage.fare_name + '</td>' +
                        '<td>' + mileage.accrual_factor + '</td>' +
                        '<td>' + mileage.minimum_miles + '</td>' +
                        '<td>' + mileage.qualifying_miles + '</td>' +
                        '<td>' + mileage.qualifying_segments + '</td>' +
                        '<td>' + mileage.restrictions + '</td>');
                }

                tableHTML.push('<tr><td rowspan="' + numMileages + '">' +
                    airline.program + '</td>' + rowHTML[0] +'</tr>');
                for (k = 1; k < numMileages; k++) {
                    tableHTML.push('<tr>' + rowHTML[k] + '</tr>');
                }
            }
            $('#earning-airline tbody').html(tableHTML.join(''));

            $('#earning-airline').slideDown();
        });
    });
});
