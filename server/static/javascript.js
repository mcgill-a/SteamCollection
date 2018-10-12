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
