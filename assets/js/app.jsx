import React, { Component, PropTypes } from 'react';
import { connect } from 'react-redux';
import { fetchUsersIfNeeded } from './userActions'
import { fetchMealsIfNeeded } from './mealActions'
import { Users } from './users'
import { Meals } from './meals'


class App extends Component {
    static propTypes = {
	users: PropTypes.array.isRequired,
	meals: PropTypes.array.isRequired,
	dispatch: PropTypes.func.isRequired
    }

    componentDidMount() {
	const { dispatch } = this.props;
	dispatch(fetchUsersIfNeeded())
	dispatch(fetchMealsIfNeeded())
    }

    render() {
	const { users, meals } = this.props
	return (
	    <div>
		<Users users={users} />
		<Meals meals={meals} />
	    </div>
		)
    }
}

const mapStateToProps = state => {
    const { users, meals } = state
    return {
	users: state.users.users || [],
	meals: state.meals.meals || []
    }
}

export default connect(mapStateToProps)(App);
