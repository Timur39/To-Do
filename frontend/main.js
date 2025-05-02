// browser-sync start --server --files "css/*.css *.js *.html"
import { getTasks, login } from './api/auth.js';


const inputElement = document.getElementById('title')
const createBtn = document.getElementById('create')
const listElement = document.getElementById('list')


let tasks = []


console.log(tasks);


function render () {
    tasks = [getTasks()]
    
    listElement.innerHTML = ''
    if (tasks.length === 0) {
        listElement.innerHTML = '<p>Нет элементов</p>'
    }
    for (let i = 0; i < tasks.length; i++) {
        listElement.insertAdjacentHTML('beforeend', getTaskTemplate(tasks[i], i))
    }
}

render()

createBtn.onclick = ()  => {
    if (!inputElement.value) {
        return
    }
    const newTask = {
        title: inputElement.value,
        is_completed: false
    }
    tasks.push(newTask)
    render()
    inputElement.value = ''
}


listElement.onclick = (event) => {
    if (event.target.dataset.index) {
        const index = Number(event.target.dataset.index)
        const type = event.target.dataset.type


        if (type === 'toggle') {
            tasks[index].is_completed = !tasks[index].is_completed

        } else if (type === 'remove') {
            tasks.splice(index, 1)
        }
        render()
    }
    
}

function getTaskTemplate(task, index) {
    console.log(task);
    
    return `
    <li>
        <input type="checkbox" class="task-checkbox" data-index="${index}" data-type="toggle" ${task?.is_completed ? 'checked' : ''}>
        <span class="task-title" style="${task.is_completed ? 'text-decoration: line-through;' : ''}" >${task.title}</span>
        <button class="delete-btn" data-index="${index}" data-type="remove">X</button>
    </li>
    `
}



