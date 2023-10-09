

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


// accept or reject a request
function editRequest(class_id, student_id, type) {
    const csrftoken = document.querySelector('#csrf').firstElementChild.value;
    fetch('editrequest', {
        method: 'POST',
        headers: {'X-CSRFToken': csrftoken},
        mode: 'same-origin', // Do not send CSRF token to another domain.
        body: JSON.stringify({
            student_id: student_id,
            class_id: class_id,
            type: type
        })
    })
    .then(response => response.json())
    .then(result => {
        listStudents(class_id, type="r");
    })
}