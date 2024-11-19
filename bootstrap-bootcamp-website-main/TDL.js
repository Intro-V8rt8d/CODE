const newItem = document.getElementById('newItem');
const Add = document.getElementById('add');
const list = document.getElementById('list');
const clear = document.getElementById('clearList')
//Empty array to hold task data
let tasks = []


    function addTask(title) {
        const task = { id: Date.now(), title, completed: false };
        tasks.push(task);
        addTaskToDOM(task)
        newItem.value = '';
    

        // Create a new list item only for the latest task
        // const newListItem = document.createElement('li');
        // newListItem.innerHTML = `ID: ${task.id} | Item: ${task.title} | Completed: ${task.completed}`;

        // // Append the new list item directly to the list
        // list.appendChild(newListItem);
    }
    
    function addTaskToDOM(task){
            const taskItem = document.createElement('li')
            taskItem.className = `task-item ${task.completed ? 'completed' : ''} text-light`
            taskItem.innerHTML = 
            `<input type="checkbox" onclick = 'linethrough(this)'>
            <p>${task.title}</p> 
            <div><button class = "btn btn-outline-dark text-light" onclick = "deleteTask(this)">Delete</button></div>`

            

            list.appendChild(taskItem)
        }
        //<button onclick = "toggleComplete(${task.id})">Toggle Completed</button>


        function linethrough(checkbox){

            const listItem = checkbox.parentElement;
            const move = listItem.parentElement;

            if (checkbox.checked) {
                move.appendChild(listItem)
                listItem.style.textDecoration = 'line-through'
                listItem.style.textDecorationColor = 'red'
            }
            else{
                listItem.style.textDecoration = 'none'
            }
        }

        function deleteTask(button){
        const listItem = button.parentElement.parentElement;
        listItem.remove();

        }


        // function toggleComplete(id){
        //     const task = tasks.find(task => task.id === id)
        //     if (task){
        //         task.completed === !task.completed
        //         renderTasks()
        //     }
        //     else{

        //     }
        // }

        function renderTasks(){
            list.innerHTML = ""
            tasks.forEach(addTaskToDOM)
        }
    //console.log(tasks)

Add.addEventListener('click', () => {
    const listHolder = newItem.value.trim()
    addTask(listHolder)
})

renderTasks()

clear.addEventListener('click', () => {
    if (list.children.length === 0 ) {
        console.log('not needed')
    }
    else{
        list.innerHTML = ''
    }
})

//<input type="checkbox" style="width: 20px; height: 23px; margin-right: 5px;" id='checkbox'> 

/*result.forEach(eachrecord => {
    //Programmatically create a new div
    const name = document.createElement('div')
    name.classList.add('eachrecord')
    name.innerHTML = `<h2>${eachrecord.id}) ${eachrecord.title}</h2> <p>${eachrecord.body}</p>`

    //putting the new div and all its elements h2 and p inside the old div
    container.appendChild(name)
});*/