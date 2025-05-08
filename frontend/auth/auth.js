import { login, logout } from '../api/auth.js';


document.addEventListener('DOMContentLoaded', () => {
    const form = document.querySelector('form')

    form.addEventListener('submit', async (event) => {
        event.preventDefault()

        const email = document.querySelector('#email').value
        const password = document.querySelector('#password').value

        if (!email || !password) {
            alert('Заполните все поля!')
            return
        }

        if (await login(email, password)) {
            window.location.href = '/frontend/index.html'
            setInterval(() => {
                localStorage.removeItem('accessToken')
            }, 1000)()
        }
    })
})