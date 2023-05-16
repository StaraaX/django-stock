function SearchBar() {
    // Declare variables
    var input, filter, table, tr, td, i, txtValue;
    input = document.getElementById("myInput");
    filter = input.value.toUpperCase();
    table = document.getElementsByClassName("tproducts")[0];
    tr = table.getElementsByTagName("tr");

    // Loop through all table rows, and hide those who don't match the search query
    for (i = 0; i < tr.length; i++) {
        td1 = tr[i].getElementsByTagName("td")[0];
        td2 = tr[i].getElementsByTagName("td")[1];
        if (td1) {
            txtValue1 = td1.textContent || td1.innerText;
            txtValue2 = td2.textContent || td2.innerText;
            if (txtValue1.toUpperCase().includes(filter) || txtValue2.toUpperCase().includes(filter)) {
                tr[i].style.display = "";
            } else {
                tr[i].style.display = "none";
            }
        }
    }
}


const printbtn = document.getElementById('print-button');
printbtn.addEventListener('click', function () {
    window.print();
}
)


function checkboxChanged(checkbox) {
    var row = checkbox.parentNode.parentNode;
    var inputs = row.querySelectorAll("input");
    if (checkbox.checked) {
        row.style.backgroundColor = "#d04462";
        for (var i = 1; i < inputs.length; i++) {
            inputs[i].disabled = false;
        }
    } else {
        row.style.backgroundColor = "#2a292e";
        for (var i = 1; i < inputs.length; i++) {
            inputs[i].disabled = true;
        }
    }
}


function Changed(input) {
    let row = input.parentNode.parentNode;
    let prix_ht = row.children[2].children[0].value;
    let qte = row.children[4].children[0].value;
    console.log(row.children[5].children[0])
    row.children[5].innerText = prix_ht * qte + " DA"
}

function Changed2(input) {
    let row = input.parentNode.parentNode;
    let prix = row.children[2].children[0].value;
    let qte = row.children[3].children[0].value;
    console.log(row.children[4].children[0])
    row.children[4].innerText = prix * qte + " DA"
}


// *************************************************************************
