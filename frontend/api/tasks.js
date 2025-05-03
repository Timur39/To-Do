import { operateData } from './methods.js'

export function getTasks() {
    try {
        const url = 'http://127.0.0.1:8000/api/tasks/get_all_tasks'
        const tasks = operateData(url, 'GET', is_protected=true)
        return tasks
    } catch (error) {
        console.error('getTasks error:', error);
    }
}

export function addTask() {
    try {
        const url = 'http://127.0.0.1:8000/api/tasks/create_task'
        params = {}
        const createdTask = operateData(url, 'POST', params, is_protected=true)
        return createdTask
    } catch (error) {
        console.error('addTask error:', error);
    }
}

export function deleteTask(taskId) {
    try {
        const url = `http://127.0.0.1:8000/api/tasks/delete_task/${taskId}`
        params = {}
        const deletedTask = operateData(url, 'DELETE', params, is_protected=true)
        return deletedTask
    } catch (error) {
        console.error('deleteTask error:', error);
    }
}

export function updateTask(taskId) {
    try {
        const url = `http://127.0.0.1:8000/api/tasks/update_task/${taskId}`
        params = {}
        const updatedTask = operateData(url, 'POST', params, is_protected=true)
        return updatedTask
    } catch (error) {
        console.error('updateTask error:', error);
    }
}
