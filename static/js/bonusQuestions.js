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

function myFunction() {
  let hide = document.getElementById("myDIV");
  if (hide.style.display === "none") {
    hide.style.display = "block";
  } else {
    hide.style.display = "none";
  }
}

function darkTheme() {
   var element = document.body;
   element.classList.toggle("dark-mode");
   }

function sortQuestions () {
    document.addEventListener('DOMContentLoaded', function () {
                const table = document.getElementById('sortMe');
                const headers = table.querySelectorAll('th');
                const tableBody = table.querySelector('tbody');
                const rows = tableBody.querySelectorAll('tr');

                // Track sort directions
                const directions = Array.from(headers).map(function (header) {
                    return '';
                });

                // Transform the content of given cell in given column
                const transform = function (index, content) {
                    // Get the data type of column
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
                    // Get the current direction
                    const direction = directions[index] || 'asc';

                    // A factor based on the direction
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

                    // Remove old rows
                    [].forEach.call(rows, function (row) {
                        tableBody.removeChild(row);
                    });

                    // Reverse the direction
                    directions[index] = direction === 'asc' ? 'desc' : 'asc';

                    // Append new row
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

sortQuestions ()