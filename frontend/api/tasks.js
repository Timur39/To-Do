import { operateData } from './methods.js'

export async function getTasks() {
    try {
        let url = 'http://127.0.0.1:8000/api/users/me'
        const response = await operateData({
            url: url,
            method: 'GET',
            isProtected: true
        })
        const usersData = response.ok ? await response.json() : []
        
        return usersData ? usersData?.tasks : []
    } catch (error) {
        console.error('getTasks error:', error);   
    }
}

export async function addTask(params = {}) {
    try {
        const url = 'http://127.0.0.1:8000/api/tasks/create_task'
        const createdTask = await operateData({
            url: url,
            method: 'POST',
            data: params,
            isProtected: true
        })
        return createdTask
    } catch (error) {
        console.error('addTask error:', error);
    }
}

export async function deleteTask(taskId) {
    try {
        const url = `http://127.0.0.1:8000/api/tasks/delete_task/${+taskId}`
        const deletedTask = await operateData({
            url: url,
            method: 'DELETE',
            isProtected: true
        })
        return deletedTask
    } catch (error) {
        console.error('deleteTask error:', error);
    }
}

export async function updateTask(taskId, params) {
    try {
        const url = `http://127.0.0.1:8000/api/tasks/update_task/${taskId}`
        const updatedTask = await operateData({
            url: url,
            method: 'POST',
            data: params,
            isProtected: true
        })
        return updatedTask
    } catch (error) {
        console.error('updateTask error:', error);
    }
}
