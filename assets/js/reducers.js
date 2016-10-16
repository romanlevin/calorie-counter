import { combineReducers } from 'redux'
import {
    REQUEST_USERS, RECEIVE_USERS, CREATE_USER, CREATED_USER,
    DELETE_USER, DELETED_USER
} from './userActions'
import {
    REQUEST_MEALS, RECEIVE_MEALS, CREATE_MEAL, CREATED_MEAL,
    DELETE_MEAL, DELETED_MEAL
} from './mealActions'

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
    console.log('meal action')
    console.log(action)
    switch (action.type) {
	case REQUEST_MEALS:
	    return {
		...state,
	    }
	case RECEIVE_MEALS:
	    return {
		...state,
		meals: action.meals,
	    }
	case CREATE_MEAL:
	    return state
	case CREATED_MEAL:
	    return {
		...state,
		users: [...state.meals, action.meal]
	    }
	case DELETE_MEAL:
	    return state
	case DELETED_MEAL:
	    const meal_id = action.meal_id
	    const index = state.meals.findIndex(meal => meal.id === meal_id)
	    return {
		meals: [
		    ...state.meals.slice(0, index),
		    ...state.meals.slice(index + 1)]
	    }
	default:
	    return state
    }
}

const rootReducer = combineReducers({
    users,
    meals
})

export default rootReducer
