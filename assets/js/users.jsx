import React, { Component, PropTypes } from 'react';
import { connect } from 'react-redux';

const User = ({ username, id }) => (
    <li>
	{username}
    </li>
);

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
    </div>
);

