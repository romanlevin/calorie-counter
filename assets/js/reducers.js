import { combineReducers } from 'redux'
import {
    REQUEST_USERS, RECEIVE_USERS, CREATE_USER, CREATED_USER,
    DELETE_USER, DELETED_USER
} from './actions'

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
	case DELETE_USER:
	    return state
	case DELETED_USER:
	    const user_id = action.user_id
	    const index = state.users.findIndex(user => user.id === user_id)
	    return {
		users: [
		    ...state.users.slice(0, index),
		    ...state.users.slice(index + 1)]
	    }
	default:
	    return state
    }
}

const meals = (state = {
    meals: [],
}, action) => {
    switch (action.type) {
	default:
	    return state
    }
}

const rootReducer = combineReducers({
    users,
    meals
})

export default rootReducer
