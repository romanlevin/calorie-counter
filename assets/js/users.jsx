import React, { Component, PropTypes } from 'react';
import { connect } from 'react-redux';

const User = ({ username, id }) => (
    <li>
	{username}
    </li>
);

export const Users = ({ users }) => (
    <ul>
	{users.map(user =>
	    <User
		key={user.id}
		{...user}
	    />
	)}
    </ul>
);

