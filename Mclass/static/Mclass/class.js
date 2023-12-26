document.addEventListener('DOMContentLoaded', function() {
    // Get all the elements with the class class-btn
    let buttons = document.querySelectorAll(".class-btn");

    // Loop through the buttons and add a click event listener to each one
    for (let button of buttons) {
      button.addEventListener("click", function() {
        // Call the toggleBorderBlue function with the clicked button as the argument
        toggleBorderBlue(this);
      });
    }
    // Get the element with the id content-btn
    let contentBtn = document.getElementById("content-btn");

    // Simulate a click on the element
    contentBtn.click();

});

// list all the students or requests in a classroom
function listStudents(id, type) {
    url = "";
    if (type === "s") {
        url = "students";
    } else {
        url = "requests";
    }
    const csrftoken = document.querySelector('#csrf').firstElementChild.value;
    fetch(url, {
        method: 'POST',
        headers: {'X-CSRFToken': csrftoken},
        mode: 'same-origin', // Do not send CSRF token to another domain.
        body: JSON.stringify({
            id: id,
        })
    })
    .then(response => response.json())
    .then(result => {
        document.querySelector("#inner-page").innerHTML = '';
        html = '';
        if (type === "s") {
            result.students.forEach((s) => {
                html += `
                <div class="flex items-center justify-between bg-gray-100 p-4 rounded-lg shadow-lg mt-2">
                    <h1 class="text-xl font-bold">${s.name}</h1>
                    <button class="bg-red-500 text-white px-4 py-2 rounded" onclick="kickStudent(${id}, ${s.id})">Kick out</button>
                </div>
                `;
            })
        } else {
            result.students.forEach((r) => {
                html += `
                <div class="flex items-center justify-between bg-gray-100 p-4 rounded-lg shadow-lg mt-2">
                <h1 class="text-xl font-bold">${r.name}</h1>
                    <div class="flex space-x-2">
                        <div class="relative group">
                            <button class="text-green-500" onclick="editRequest(${id}, ${r.id}, type='accept')">
                                <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
                                </svg>
                            </button>
                            <span class="opacity-0 group-hover:opacity-100 bg-gray-800 text-white text-xs absolute top-full left-1/2 transform -translate-x-1/2 p-1 rounded">Accept</span>
                        </div>
                        <div class="relative group">
                            <button class="text-red-500" onclicl="editRequest(${id}, ${r.id}, type='reject')">
                                <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
                                </svg>
                            </button>
                            <span class="opacity-0 group-hover:opacity-100 bg-gray-800 text-white text-xs absolute top-full left-1/2 transform -translate-x-1/2 p-1 rounded">Reject</span>
                        </div>
                    </div>
                </div>
                `;
            })
        }
        document.querySelector("#inner-page").innerHTML = html;
    })
}


// kicking students out of a class
function kickStudent(class_id, student_id) {
    const csrftoken = document.querySelector('#csrf').firstElementChild.value;
    fetch('kick', {
        method: 'POST',
        headers: {'X-CSRFToken': csrftoken},
        mode: 'same-origin', // Do not send CSRF token to another domain.
        body: JSON.stringify({
            student_id: student_id,
            class_id: class_id
        })
    })
    .then(response => response.json())
    .then(result => {
        listStudents(class_id, type="s");
    })
}


// Define a function that takes an element as a parameter
function toggleBorderBlue(element) {
    // Check if the element doesn't have the class class-btn
    if (!element.classList.contains("border-blue-600")) {

        // Remove the blue border from other btns
        let buttons = document.querySelectorAll(".class-btn.border-blue-600");
        for (let button of buttons) {
            button.classList.remove("border-blue-600");
        }
        // add the class border-blue-600 to the element
        element.classList.add("border-blue-600");

        // Get the element by id
        var settings_form = document.getElementById('settings_form');
        var content_form = document.getElementById('content_form');

        settings_form.style.display = 'none';
        content_form.style.display = 'none';
        let content_div = document.querySelector('#contentlist');
        content_div.innerHTML = '';

        if (element.id === "settings") {
            // Change its display to block
            settings_form.style.display = 'block';
        } else if (element.id === "content-btn") {
            content_form.style.display = 'block';
        }
    }
}


// show content
// a function for showing the content cards
function showContent(class_id, page=1) {
    const csrftoken = document.querySelector('#csrf').firstElementChild.value;
    
    fetch('content', {
        method: 'POST',
        headers: {'X-CSRFToken': csrftoken},
        mode: 'same-origin', // Do not send CSRF token to another domain.
        body: JSON.stringify({
            page: page,
            class_id: class_id,
        })
    })
    .then(response => response.json())
    .then(result => {
        // clean the container div
        let content_div = document.querySelector('#contentlist');
        content_div.innerHTML = '';
        // loop and add the classes cards
        result.content.forEach((r) => {
            let content_card = createCard(name=r.name, type=r.type, url=r.url);
            content_div.appendChild(content_card);
        })
        
        // add paginator buttons
        if (page > 1) {
            let pg = `
                <div class="flex justify-center mt-2">
                    <ul class="flex items-center">`;
            if (result.has_previous) {
                pg += `<li>
                        <button class="bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded-l shadow-lg transform transition duration-300 ease-in-out hover:scale-105" onclick="showClasses('${filter}', ${page - 1})">
                            Prev
                        </button>
                    </li>`;
            } else {}
            pg += `<li>
                        <span class="bg-white text-blue-500 font-bold py-2 px-4 border border-blue-500 shadow-lg">
                            Page <span id="current-page">${page}</span> of <span id="total-pages">${result.num_pages}</span>
                        </span>
                    </li>`;
            if (result.has_next) {
                pg += `<li>
                        <button class="bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded-r shadow-lg transform transition duration-300 ease-in-out hover:scale-105" onclick="showClasses('${filter}', ${page + 1})">
                            Next
                        </button>
                    </li>`;
            } else {}
            pg += `</ul>
            </div>
            `;
            document.querySelector('#contentlist').innerHTML += pg;
        }
    })
}


// Define a function that takes name and type as parameters
function createCard(name, type, url) {
    // Create a div element for the card container
    let card = document.createElement("div");
    card.className = "mt-4 bg-white mx-auto max-w-sm shadow-lg rounded-lg overflow-hidden";
  
    // Create a div element for the card content
    let content = document.createElement("div");
    content.className = "sm:flex sm:items-center px-6 py-4";
  
    // Create a div element for the card text
    let text = document.createElement("div");
    text.className = "text-center sm:text-left sm:flex-grow";
  
    // Create a p element for the name
    let nameP = document.createElement("p");
    nameP.className = "text-xl leading-tight";
    nameP.textContent = name;
  
    // Create a p element for the type
    let typeP = document.createElement("p");
    typeP.className = "text-xs font-semibold rounded-full px-4 py-1 leading-normal bg-blue-700 border border-blue focus:outline-none text-white text-sm font-semibold text-center";
    typeP.style.marginTop = "20px";
    typeP.textContent = type;
  
    // Create a div element for the button
    let buttonDiv = document.createElement("div");
    buttonDiv.className = "flex justify-center items-center";
  
    // Create a a element for the button link
    let buttonA = document.createElement("a");
    buttonA.href = url;
  
    // Create a button element for the button
    let button = document.createElement("button");
    button.className = "text-xs font-semibold rounded-full px-4 py-1 leading-normal bg-green-700 border border-green focus:outline-none text-white text-sm font-semibold hover:bg-green-500";
    button.textContent = "Open";
  
    // Append the elements to their parents
    buttonA.appendChild(button);
    buttonDiv.appendChild(buttonA);
    text.appendChild(nameP);
    text.appendChild(typeP);
    text.appendChild(buttonDiv);
    content.appendChild(text);
    card.appendChild(content);
  
    // Return the card element
    return card;
  }