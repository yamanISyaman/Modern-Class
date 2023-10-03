document.addEventListener('DOMContentLoaded', function() {
    // show all the classes as default
    showClasses('all', 1);
});


// a function for showing the classes
function showClasses(filter, page) {
    const csrftoken = document.querySelector('#csrf').firstElementChild.value;
    fetch('', {
        method: 'POST',
        headers: {'X-CSRFToken': csrftoken},
        mode: 'same-origin', // Do not send CSRF token to another domain.
        body: JSON.stringify({
            filter: filter,
            page: page,
        })
    })
    .then(response => response.json())
    .then(result => {
        // clean the container div
        document.querySelector('#classes-list').innerHTML = '';
        // loop and add the classes cards
        result.classes.forEach((r) => {
            let vcolor = 'blue';
            let v = 'Public';
            if (r.private) {
                v = 'Private';
                vcolor = 'gray'
            } else {}
            let ccolor = 'green';
            let c = 'Available';
            if (r.closed) {
                c = 'Closed';
                ccolor = 'red'
            } else {}
            let image = 'https://img.freepik.com/free-vector/hand-drawn-flat-design-stack-books-illustration_23-2149341898.jpg';
            if (r.image != '') {
                image = r.image;
            } else {}
            document.querySelector('#classes-list').innerHTML += `
                <div class="flex justify-center mt-2">
                    <div class="p-4 border border-gray-300 shadow-lg rounded-lg">
                        <div class="mb-4 flex flex-col items-center">
                            <span class="text-xl font-bold text-blue-600">${r.title}</span>
                            <img src="${image}" alt="Class Image" class="mt-4 rounded-lg" width="400" height="400">
                        </div>
                        <p class="max-w-md text-gray-700">${r.details}</p>
                        <div class="mt-4 flex items-center justify-between">
                            <span class="text-sm font-semibold text-gray-600">Teacher: ${r.teacher}</span>
                            <span class="text-sm font-semibold text-gray-600">Category: ${r.category}</span>
                            <div class="flex">
                                <span class="mr-2 px-2 py-1 border border-${ccolor}-500 bg-${ccolor}-100 text-xs font-bold text-${ccolor}-500 rounded-full">${c}</span>
                                <span class="mr-2 px-2 py-1 border border-${vcolor}-500 bg-${vcolor}-100 text-xs font-bold text-${vcolor}-500 rounded-full">${v}</span>
                            </div>
                        </div>
                    </div>
                </div>
                `;
            })
        
        // add paginator buttons
        let pg = `
            <div class="flex justify-center">
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
        document.querySelector('#classes-list').innerHTML += pg;
    })
}
