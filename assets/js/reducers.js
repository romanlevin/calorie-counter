import { combineReducers } from 'redux'
import { REQUEST_USERS, RECEIVE_USERS } from './actions'

const users = (state = {
    isFetching: false,
    didInvalidate: false,
    users: [],
}, action) => {
    switch (action.type) {
	case REQUEST_USERS:
	    return {
		...state,
		isFetching: true,
		didInvalidate: false,
	    }
	case RECEIVE_USERS:
	    return {
		...state,
		isFetching: false,
		didInvalidate: false,
		users: action.users,
		lastUpdated: action.receivedAt
	    }
	default:
	    return state
    }
}

const rootReducer = combineReducers({
    users
})

export default rootReducer
