import { combineReducers } from 'redux'
import { REQUEST_USERS, RECEIVE_USERS, CREATE_USER, CREATED_USER } from './actions'

const users = (state = {
    users: [],
}, action) => {
    switch (action.type) {
	case REQUEST_USERS:
	    return {
		...state,
	    }
	case RECEIVE_USERS:
	    return {
		...state,
		users: action.users,
	    }
	case CREATE_USER:
	    return state
	case CREATED_USER:
	    return {
		...state,
		users: [...state.users, action.user]
	    }
	default:
	    return state
    }
}

const rootReducer = combineReducers({
    users
})

export default rootReducer
