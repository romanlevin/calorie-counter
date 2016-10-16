import React, { Component, PropTypes } from 'react';
import { connect } from 'react-redux';
import { postMeal, deleteMeal } from './mealActions';

const MealElement = ({ text, calories, time, date, user, id, dispatch }) => (
    <li>
	{text} - {calories} calories
	<span onClick={e => dispatch(deleteMeal(id))}> ✗</span>
	<br />User: {user}
	<br /><time>{date}T{time}</time>
    </li>
)
const Meal = connect()(MealElement)

const NewMealForm = ({dispatch}) => {
    let text, calories, time, date;
    return <form onSubmit={e => {
	let allFields = [text, calories, time, date];
	e.preventDefault()

	if (!allFields.reduce((prev, field) => prev && !!field.value.trim(), true))
	{
	    return
	}
	dispatch(postMeal({
	    text: text.value,
	    calories: calories.value,
	    time: time.value,
	    date: date.value,
	}))
	allFields.map(field => field.value = '')
	}}>
	<input placeholder="text" name="text" id="text" ref={node => text = node}/><br />
	<input placeholder="calories" type="number" name="calories" id="calories" ref={node => calories = node}/><br />
	<input placeholder="HH:mm" name="time" id="time" type="time" ref={node => time = node}/><br />
	<input placeholder="YYYY-MM-DD" name="date" id="date" type="date" ref={node => date = node}/><br />
	<input type="submit" value="Create Meal"/>
    </form>
};

const NewMeal = connect()(NewMealForm)

export const Meals = ({ meals }) => (
    <div>
	<h1>Meals:</h1>
	<ul>
	    {meals.map(meal =>
		<Meal
		    key={meal.id}
		    {...meal}
		/>
	    )}
	</ul>
	<NewMeal/>
    </div>
);


