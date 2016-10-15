import React, { Component, PropTypes } from 'react';
import { connect } from 'react-redux';
import { postUser, deleteUser } from './actions';

const UserElement = ({ username, id, dispatch }) => (
    <li>
	{username}
	<span onClick={e => dispatch(deleteUser(id))}>✗</span>
    </li>
)
const User = connect()(UserElement)

const NewUserForm = ({dispatch}) => {
    let username, password, calorie_limit;
    return <form onSubmit={e => {
	e.preventDefault()
	if (!username.value.trim() || !password.value.trim()) {
	    return
	}
	dispatch(postUser({
	    username: username.value,
	    password: password.value,
	    calorie_limit: calorie_limit.value,
	}))
	username.value = ''
	password.value = ''
	calorie_limit.value = ''
	}}>
	<input placeholder="username" name="username" id="username" ref={node => username = node}/><br />
	<input placeholder="password" type="password" name="password" id="password" ref={node => password = node}/><br />
	<input placeholder="calorie limit" name="calorie_limit" id="calorie_limit" ref={node => calorie_limit = node}/><br />
	<input type="submit" value="createUser"/>
    </form>
};

const NewUser = connect()(NewUserForm)

export const Users = ({ users }) => (
    <div>
	<h1>Users:</h1>
	<ul>
	    {users.map(user =>
		<User
		    key={user.id}
		    {...user}
		/>
	    )}
	</ul>
	<NewUser/>
    </div>
);

