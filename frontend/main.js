// browser-sync start --server --files "css/*.css *.js *.html"
import { getTasks, addTask, deleteTask, updateTask } from './api/tasks.js';

const inputElement = document.querySelector('#title')
const createBtn = document.querySelector('#create')
const listElement = document.querySelector('#list')
let tasks = []


if (!localStorage.getItem('accessToken')) {
    alert('Войдите в акаунт!')
    window.location.href = '/frontend/auth/auth.html'
}

await fetchTasks()

async function fetchTasks() {
    tasks = await getTasks()
    await renderTasks(tasks);
}

async function renderTasks(tasks) {
    listElement.innerHTML = ''

    if (tasks.length === 0) {
        listElement.innerHTML = '<p>Нет задач</p>'
    } else {
        tasks.forEach(task => {
            const li = document.createElement('li')

            li.className = task.is_completed ? 'completed' : ''
            li.innerHTML = getTaskTemplate(task)

            li.querySelector('input').addEventListener('change', async () => {
                try {
                    await updateTask(task.id, {
                        title: task.title,
                        description: task.description,
                        priority: task.priority,
                        is_completed: !task.is_completed
                    })
                    li.classList.toggle('completed')
                    task.is_completed = !task.is_completed
                    await renderTasks(tasks)
                } catch (error) {
                    console.error('Update error:', error);
                }
            })

            li.querySelector('.delete-btn').addEventListener('click', async () => {
                await deleteTask(task.id)
                tasks.pop(task)
                li.remove()
            })
            listElement.appendChild(li)
        })
    }
}

createBtn.addEventListener('click', async () => {
    if (!inputElement.value) {
        return
    }
    const response = await addTask({
        'title': inputElement.value.trim(),
        'description': '',
        'priority': 0,
        'is_completed': false,
        'date': new Date().toISOString().slice(0, 10)
    })
    inputElement.value = ''
    const createdTask = await response.json()
    createdTask['id'] = tasks[tasks.length - 1].id + 1
    tasks.push(createdTask)

    await renderTasks(tasks)
})

setInterval(() => {
    localStorage.removeItem('accessToken')
    location.reload()
}, 1000000000)


function getTaskTemplate(task) {
    return `
        <input type="checkbox" class="btn task-checkbox" data-index="${task.id}" data-type="toggle" ${task?.is_completed ? 'checked' : ''}>
        <span class="task-title" style="${task?.is_completed ? 'completed' : ''}">${task.title}</span>
        <span class="priority">${'★'.repeat(task.priority)}</span>
        <button class="btn delete-btn" data-index="${task.id}" data-type="remove">X</button>
    `
}
