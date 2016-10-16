import Cookies from 'js-cookie'

const getCsrfToken = () => Cookies.get('csrftoken')

const headers = () => ({
    'X-CSRFToken': getCsrfToken(),
    'Content-Type': 'application/json',
})

const fetchOptions = () => ({
    headers: headers(),
    credentials: 'same-origin',
})

export default (url, options) => fetch(url, {...fetchOptions(), ...options})
