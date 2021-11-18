const list = document.querySelector('#book-list ul');
const forms = document.forms;

// you receive an array of objects which you must sort in the by the key "sortField" in the "sortDirection"
function getSortedItems(items, sortField, sortDirection) {
    console.log(items)
    console.log(sortField)
    console.log(sortDirection)

    // === SAMPLE CODE ===
    // if you have not changed the original html uncomment the code below to have an idea of the
    // effect this function has on the table
    //
    if (sortDirection === "asc") {
        const firstItem = items.shift()
        if (firstItem) {
            items.push(firstItem)
        }
    } else {
        const lastItem = items.pop()
        if (lastItem) {
            items.push(lastItem)
        }
    }

    return items
}

// you receive an array of objects which you must filter by all it's keys to have a value matching "filterValue"
function getFilteredItems(items, filterValue) {
    console.log(items)
    console.log(filterValue)

    // === SAMPLE CODE ===
    // if you have not changed the original html uncomment the code below to have an idea of the
    // effect this function has on the table
    //
    for (let i=0; i<filterValue.length; i++) {
        items.pop()
    }

    return items
}

function toggleTheme() {
    console.log("toggle theme")
}

function increaseFont() {
    console.log("increaseFont")
}

function decreaseFont() {
    console.log("decreaseFont")
}

function increase(){
    document.getElementByClass("question-td").style.fontSize = "x-large";
}

function increaseQuestionFont(){

    document.getElementsByClass("question-td").addEventListener("click", increase);
}

function filter(){
const list = document.querySelector('#book-list ul');
const forms = document.forms;

const searchBar = forms['search-questions'].querySelector('input');
searchBar.addEventListener('keyup', (e) => {
  const term = e.target.value.toLowerCase();
  const questions = list.getElementsByTagName('td');
  Array.from(questions).forEach((book) => {
    const title = question.firstElementChild.textContent;
    if(title.toLowerCase().indexOf(e.target.value) != -1){
      question.style.display = 'block';
    } else {
      question.style.display = 'none';
    }
  });
});
}

function myFunctionHide() {
  let hide = document.getElementById("myDIV");
  if (hide.style.display === "none") {
    hide.style.display = "block";
  } else {
    hide.style.display = "none";
  }
}

function sortQuestions () {
    document.addEventListener('DOMContentLoaded', function () {
                const table = document.getElementById('sortMe');
                const headers = table.querySelectorAll('th');
                const tableBody = table.querySelector('tbody');
                const rows = tableBody.querySelectorAll('tr');

                const directions = Array.from(headers).map(function (header) {
                    return '';
                });

                const transform = function (index, content) {

                    const type = headers[index].getAttribute('data-type');
                    switch (type) {
                        case 'number':
                            return parseFloat(content);
                        case 'string':
                        default:
                            return content;
                    }
                };

                const sortColumn = function (index) {

                    const direction = directions[index] || 'asc';

                    const multiplier = direction === 'asc' ? 1 : -1;

                    const newRows = Array.from(rows);

                    newRows.sort(function (rowA, rowB) {
                        const cellA = rowA.querySelectorAll('td')[index].innerHTML;
                        const cellB = rowB.querySelectorAll('td')[index].innerHTML;

                        const a = transform(index, cellA);
                        const b = transform(index, cellB);

                        switch (true) {
                            case a > b:
                                return 1 * multiplier;
                            case a < b:
                                return -1 * multiplier;
                            case a === b:
                                return 0;
                        }
                    });

                    [].forEach.call(rows, function (row) {
                        tableBody.removeChild(row);
                    });

                    directions[index] = direction === 'asc' ? 'desc' : 'asc';

                    newRows.forEach(function (newRow) {
                        tableBody.appendChild(newRow);
                    });
                };

                [].forEach.call(headers, function (header, index) {
                    header.addEventListener('click', function () {
                        sortColumn(index);
                    });
                });
            });


}

function decrease(){
    let elements = document.getElementsByClassName('row');
    for(let i = 0; i < elements.length; i++){
        let element = elements[i];
        let style = window.getComputedStyle(element, null).getPropertyValue('font-size');
        let currentSize = parseInt(style);
        currentSize--;
        element.style.fontSize = currentSize.toString() + 'px';
    }

}

function increase(){
    let elements = document.getElementsByClassName('row');
    for(let element of elements){
        let style = window.getComputedStyle(element, null).getPropertyValue('font-size');
        let currentSize = parseInt(style);
        currentSize++;
        element.style.fontSize = currentSize.toString() + 'px';
    }

}



function myFunction() {

  let input, filter, table, tr, td, i, txtValue;
  input = document.getElementById("myInput");
  filter = input.value.toUpperCase();
  table = document.getElementById("sortMe");
  tr = table.getElementsByTagName("tr");

  for (i = 0; i < tr.length; i++) {
    td = tr[i].getElementsByTagName("td")[1];
    if (td) {
      txtValue = td.textContent || td.innerText;
      if (txtValue.toUpperCase().indexOf(filter) > -1) {
        tr[i].style.display = "";
      } else {
        tr[i].style.display = "none";
      }
    }
  }
}

sortQuestions();
myFunction();
document.getElementById("increase").addEventListener("click", increase);
document.getElementById("decrease").addEventListener("click", decrease);