function devSearch() {
  // Declare variables 
  var input, filter, table, tr, td, i;
  input = document.getElementById("devTableSearch");
  filter = input.value.toUpperCase();
  table = document.getElementById("devTable");
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
  document.getElementById("btn_discover").addEventListener('click', () => {
    scrollTo(document.getElementById("discover"));
  });

function sortTable() {
  var table, rows, switching, i, x, y, shouldSwitch;
  table = document.getElementById("devTable");
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
      if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
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
function sortByCount() {
  var table, rows, switching, i, x, y, shouldSwitch;
  table = document.getElementById("devTable");
  switching = true;
  while (switching) {
    switching = false;
    rows = table.rows;
    for (i = 1; i < (rows.length - 1); i++) {
      shouldSwitch = false;
      x = rows[i].getElementsByTagName("TD")[1];
      y = rows[i + 1].getElementsByTagName("TD")[1];
	  console.log(y);
      if (x.innerHTML < y.innerHTML) {
        shouldSwitch = true;
        break;
      }
    }
    if (shouldSwitch) {
      rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
      switching = true;
    }
  }
}

function toggleDisabled(_checked, id) {
	if (_checked)
	{
		document.getElementById(id).removeAttribute('disabled')
		document.getElementById(id).disabled = false;
		document.getElementById(id).style.background = 'white';
	}
	else
	{
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
