import { operateData } from './methods.js'

export function getTasks() {
    try {
        const tasks = operateData('http://127.0.0.1:8000/api/tasks/get_all_tasks', method='GET', is_protected=true)
        return tasks
    } catch (error) {
        console.error('getTasks error:', error);
    }
}


export function addTask() {
    try {
        const url = 'http://127.0.0.1:8000/api/tasks/get_all_tasks'
        fetch(url, {headers: getAuthHeader()})
        .then((response) => response.json())

    } catch (error) {
        console.error('addTask error:', error);
    }
}


export function deleteTask() {
    try {


    } catch (error) {
        console.error('deleteTask error:', error);
    }
}


export function updateTask() {
    try {


    } catch (error) {
        console.error('updateTask error:', error);
    }
}

