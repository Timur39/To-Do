import { operateData } from './methods.js'

export async function login() {
    try {
        const params = {
            grant_type: 'password',
            username: 'user@example5.com',
            password: 'string',
            scope: '',
            client_id: 'user@example3.com',
            client_secret: 'user@example3.com'
        }
        const cred = operateData('http://127.0.0.1:8000/api/auth/login', params, 'POST', is_protected=true)

        localStorage.setItem('accessToken', cred.access_token)
    } catch (error) {
        console.error('Login error:');
    }
}

export async function logout() {
    try {
        localStorage.removeItem('accessToken');
        localStorage.removeItem('refreshToken');
    } catch (error) {
        console.error('Logout error:');
    }
}


export async function register() {
    try {

    } catch (error) {
        console.error('Register error:');
    }
}



