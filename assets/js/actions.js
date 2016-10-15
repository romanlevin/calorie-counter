import Cookies from 'js-cookie'
export const REQUEST_USERS = 'REQUEST_USERS'
export const RECEIVE_USERS = 'RECEIVE_USERS'
export const CREATE_USER = 'CREATE_USER'
export const CREATED_USER = 'CREATED_USER'

export const requestUsers = () => ({
    type: REQUEST_USERS
})

export const receiveUsers = users => ({
    type: RECEIVE_USERS,
    users,
    receivedAt: Date.now()
})

const createUser = (user) => ({
    type: CREATE_USER,
    user
});

const createdUser = user => ({
    type:CREATED_USER,
    user
});

const getCsrfToken = () => Cookies.get('csrftoken')
const headers = () => ({
    'X-CSRFToken': getCsrfToken(),
    'Content-Type': 'application/json',
})
const fetchOptions = () => ({
    headers: headers(),
    credentials: 'same-origin',
})

export const postUser = user => dispatch => {
    dispatch(createUser(user))

    console.log(user)
    return fetch('/api/users/', {
	method: 'POST',
	body: JSON.stringify(user),
	headers: headers(),
	...fetchOptions(),
	})
	.then(response => response.json())
	.then(json => dispatch(createdUser(json)))
}

const fetchUsers = () => dispatch => {
    dispatch(requestUsers)

    return fetch('/api/users/', {
	credentials: 'same-origin'
        })
	.then(response => response.json())
	.then(json => dispatch(receiveUsers(json)))
}

const shouldFetchUsers = state => {
    const users = state.users
    if (!users) {
	return true
    }
    if (users.isFetching) {
	return false
    }
    return true
}

export const fetchUsersIfNeeded = () => (dispatch, getState) => {
    if (shouldFetchUsers(getState())) {
	return dispatch(fetchUsers())
    }
}
