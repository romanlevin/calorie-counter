export const REQUEST_USERS = 'REQUEST_USERS'
export const RECEIVE_USERS = 'RECEIVE_USERS'

export const requestUsers = () => ({
    type: REQUEST_USERS
})

export const receiveUsers = users => ({
    type: RECEIVE_USERS,
    users,
    receivedAt: Date.now()
})

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
