import fetch from './fetch'
export const REQUEST_MEALS = 'REQUEST_MEALS'
export const RECEIVE_MEALS = 'RECEIVE_MEALS'
export const CREATE_MEAL = 'CREATE_MEAL'
export const CREATED_MEAL = 'CREATED_MEAL'
export const DELETE_MEAL = 'DELETE_MEAL'
export const DELETED_MEAL = 'DELETED_MEAL'

export const requestMeals = () => ({
    type: REQUEST_MEALS
})

export const receiveMeals = meals => ({
    type: RECEIVE_MEALS,
    meals,
})

const createMeal = meal => ({
    type: CREATE_MEAL,
    meal
});

const createdMeal= meal => ({
    type: CREATED_MEAL,
    meal
});

const deleteMealAction = meal_id => ({
    type: DELETE_MEAL,
    meal_id
})

const deletedMeal = meal_id => ({
    type: DELETED_MEAL,
    meal_id
})

export const deleteMeal = meal_id => dispatch => {
    dispatch(deleteMealAction(meal_id))
    return fetch(`/api/meals/${meal_id}`, {
	method: 'DELETE',
    })
	.then(response => dispatch(deletedMeal(meal_id)))
}

export const postMeal = meal => dispatch => {
    dispatch(createMeal(meal))

    return fetch('/api/meals/', {
	method: 'POST',
	body: JSON.stringify(meal),
	})
	.then(response => response.json())
	.then(json => dispatch(createdMeal(json)))
}

const fetchMeals = () => dispatch => {
    dispatch(requestMeals)

    return fetch('/api/meals/', {
	credentials: 'same-origin'
        })
	.then(response => response.json())
	.then(json => dispatch(receiveMeals(json)))
}

const shouldFetchMeals = state => {
    const meals = state.meals
    if (!meals) {
	return true
    }
    if (meals.isFetching) {
	return false
    }
    return true
}

export const fetchMealsIfNeeded = () => (dispatch, getState) => {
    if (shouldFetchMeals(getState())) {
	return dispatch(fetchMeals())
    }
}
