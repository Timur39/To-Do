import { operateData } from './methods.js'

export async function login(email = '', password = '') {
    try {
        let response = await operateData({
            url: 'http://127.0.0.1:8000/api/auth/login',
            data: { username: email, password: password },
            method: 'POST',
            isProtected: true,
            isForm: true
        })
        if (response.ok) {
            const cred = await response.json()
            await logout()
            localStorage.setItem('accessToken', cred.access_token)
            return true
        } else {
            alert('Ощибка авторизации')
            return 
        }
    } catch (error) {
        console.error('Login error:', error);
    }
}

export async function logout() {
    try {
        localStorage.removeItem('accessToken');
        // localStorage.removeItem('refreshToken');
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
