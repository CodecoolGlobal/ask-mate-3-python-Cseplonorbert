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

