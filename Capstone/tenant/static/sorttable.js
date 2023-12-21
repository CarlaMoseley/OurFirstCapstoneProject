function makeSortable(table) {
    var headers = table.getElementsByTagName('th');
    for (var i = 0; i < headers.length; i++) {
      headers[i].addEventListener('click', function() {
        sortTable(table, this.cellIndex);
      });
    }
  }
  
  function sortTable(table, column) {
    var rows, switching, i, x, y, shouldSwitch;
    switching = true;
    while (switching) {
      switching = false;
      rows = table.rows;
      for (i = 1; i < rows.length - 1; i++) {
        shouldSwitch = false;
        x = rows[i].getElementsByTagName('td')[column];
        y = rows[i + 1].getElementsByTagName('td')[column];
        if (isNaN(x.innerHTML)) {
          shouldSwitch = x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase();
        } else {
          shouldSwitch = Number(x.innerHTML) > Number(y.innerHTML);
        }
        if (shouldSwitch) {
          rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
          switching = true;
          break;
        }
      }
    }
  }