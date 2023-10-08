

// list all the students in a classroom
function showStudents(id) {
    const csrftoken = document.querySelector('#csrf').firstElementChild.value;
    fetch('students', {
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
        result.students.forEach((s) => {
            html += `
            <div class="flex items-center justify-between bg-gray-100 p-4 rounded-lg shadow-lg mt-2">
                <h1 class="text-xl font-bold">${s.name}</h1>
                <button class="bg-red-500 text-white px-4 py-2 rounded" onclick="kickStudent(${id}, ${s.id})">Kick</button>
            </div>
            `;
        })
        document.querySelector("#inner-page").innerHTML = html;
    })
}


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
        showStudents(class_id);
    })
}