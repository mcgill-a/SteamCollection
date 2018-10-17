function tableSearch(selected_table_search, selected_table) {
  // Declare variables 
  var input, filter, table, tr, td, i;
  input = document.getElementById(selected_table_search);
  filter = input.value.toUpperCase();
  table = document.getElementById(selected_table);
  tr = table.getElementsByTagName("tr");

  // Loop through all table rows, and hide those who don't match the search query
  for (i = 0; i < tr.length; i++) {
    td = tr[i].getElementsByTagName("td")[0];
    if (td) {
      if (td.innerHTML.toUpperCase().indexOf(filter) > -1) {
        tr[i].style.display = "";
      } else {
        tr[i].style.display = "none";
      }
    }
  }
}

function scrollTo(element) {
  window.scroll({
    top: element.getBoundingClientRect().top + window.scrollY,
    left: 0,
    behavior: 'smooth'
  });
}

document.getElementById("btn-return").addEventListener('click', () => {
  scrollTo(document.getElementById("navbar"));
});

function sortController(selected_table) {

  if (document.getElementById("table-sort").value === 'A')
  {
    tableSortA(selected_table);
  }
  else if (document.getElementById("table-sort").value === 'Z')
  {
    tableSortZ(selected_table);
  }
  else if (document.getElementById("table-sort").value === 'L')
  {
    sortByCountL(selected_table)
  }
  else if (document.getElementById("table-sort").value === 'H')
  {
    sortByCountL(selected_table)
  }
}


function tableSortA(selected_table) {
  var table, rows, switching, i, x, y, shouldSwitch;
  table = document.getElementById(selected_table);
  switching = true;
  /*Make a loop that will continue until
  no switching has been done:*/
  while (switching) {
    //start by saying: no switching is done:
    switching = false;
    rows = table.rows;
    /*Loop through all table rows (except the
    first, which contains table headers):*/
    for (i = 1; i < (rows.length - 1); i++) {
      //start by saying there should be no switching:
      shouldSwitch = false;
      /*Get the two elements you want to compare,
      one from current row and one from the next:*/
      x = rows[i].getElementsByTagName("TD")[0];
      y = rows[i + 1].getElementsByTagName("TD")[0];
      //check if the two rows should switch place:
      if (x.innerText.toLowerCase() > y.innerText.toLowerCase()) {
        //if so, mark as a switch and break the loop:
        shouldSwitch = true;
        break;
      }
    }
    if (shouldSwitch) {
      /*If a switch has been marked, make the switch
      and mark that a switch has been done:*/
      rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
      switching = true;
    }
  }
}

function tableSortZ(selected_table) {
  var table, rows, switching, i, x, y, shouldSwitch;
  table = document.getElementById(selected_table);
  switching = true;
  /*Make a loop that will continue until
  no switching has been done:*/
  while (switching) {
    //start by saying: no switching is done:
    switching = false;
    rows = table.rows;
    /*Loop through all table rows (except the
    first, which contains table headers):*/
    for (i = 1; i < (rows.length - 1); i++) {
      //start by saying there should be no switching:
      shouldSwitch = false;
      /*Get the two elements you want to compare,
      one from current row and one from the next:*/
      x = rows[i].getElementsByTagName("TD")[0];
      y = rows[i + 1].getElementsByTagName("TD")[0];
      //check if the two rows should switch place:
      if (x.innerText.toLowerCase() < y.innerText.toLowerCase()) {
        //if so, mark as a switch and break the loop:
        shouldSwitch = true;
        break;
      }
    }
    if (shouldSwitch) {
      /*If a switch has been marked, make the switch
      and mark that a switch has been done:*/
      rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
      switching = true;
    }
  }
}

function sortByCountL(selected_table) {
  var table, rows, switching, i, x, y, shouldSwitch;
  table = document.getElementById(selected_table);
  switching = true;
  /*Make a loop that will continue until
  no switching has been done:*/
  while (switching) {
    //start by saying: no switching is done:
    switching = false;
    rows = table.rows;
    /*Loop through all table rows (except the
    first, which contains table headers):*/
    for (i = 1; i < (rows.length - 1); i++) {
      //start by saying there should be no switching:
      shouldSwitch = false;
      /*Get the two elements you want to compare,
      one from current row and one from the next:*/
      x = rows[i].getElementsByTagName("TD")[1];
      y = rows[i + 1].getElementsByTagName("TD")[1];
      //check if the two rows should switch place:
      xval = parseInt(x.innerText)
      yval = parseInt(y.innerText)
      if (parseInt(x.innerText) > parseInt(y.innerText)) {
        //if so, mark as a switch and break the loop:
        shouldSwitch = true;
        break;
      }
    }
    if (shouldSwitch) {
      /*If a switch has been marked, make the switch
      and mark that a switch has been done:*/
      rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
      switching = true;
    }
  }
}

function sortByCountH(selected_table) {
  var table, rows, switching, i, x, y, shouldSwitch;
  table = document.getElementById(selected_table);
  switching = true;
  /*Make a loop that will continue until
  no switching has been done:*/
  while (switching) {
    //start by saying: no switching is done:
    switching = false;
    rows = table.rows;
    /*Loop through all table rows (except the
    first, which contains table headers):*/
    for (i = 1; i < (rows.length - 1); i++) {
      //start by saying there should be no switching:
      shouldSwitch = false;
      /*Get the two elements you want to compare,
      one from current row and one from the next:*/
      x = rows[i].getElementsByTagName("TD")[1];
      y = rows[i + 1].getElementsByTagName("TD")[1];
      //check if the two rows should switch place:
      xval = parseInt(x.innerText)
      yval = parseInt(y.innerText)
      if (parseInt(x.innerText) < parseInt(y.innerText)) {
        //if so, mark as a switch and break the loop:
        shouldSwitch = true;
        break;
      }
    }
    if (shouldSwitch) {
      /*If a switch has been marked, make the switch
      and mark that a switch has been done:*/
      rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
      switching = true;
    }
  }
}

function toggleDisabled(_checked, id) {
  if (_checked) {
    document.getElementById(id).removeAttribute('disabled')
    document.getElementById(id).disabled = false;
    document.getElementById(id).style.background = 'white';
  }
  else {
    document.getElementById(id).value = "";
    document.getElementById(id).disabled = true;
    document.getElementById(id).style.background = '#b5b5b5';
  }
}

function resetSearchForm() {

  document.getElementById('txt-appid').style.background = '#b5b5b5';
  document.getElementById('txt-name').style.background = '#b5b5b5';
  document.getElementById('txt-genre').style.background = '#b5b5b5';
  document.getElementById('txt-developer').style.background = '#b5b5b5';
  document.getElementById('txt-category').style.background = '#b5b5b5';

  document.getElementById('chk-appid').checked = false;
  document.getElementById('chk-name').checked = false;
  document.getElementById('chk-genre').checked = false;
  document.getElementById('chk-developer').checked = false;
  document.getElementById('chk-category').checked = false;

  document.getElementById('txt-appid').value = "";
  document.getElementById('txt-name').value = "";
  document.getElementById('txt-genre').value = "";
  document.getElementById('txt-developer').value = "";
  document.getElementById('txt-category').value = "";
}  
