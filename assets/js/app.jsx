import React, { Component, PropTypes } from 'react';
import { connect } from 'react-redux';
import { fetchUsersIfNeeded } from './userActions'
import { Users } from './users'


class App extends Component {
    static propTypes = {
	users: PropTypes.array.isRequired,
	// isFetching: PropTypes.bool.isRequired,
	// isInvalidated: PropTypes.bool.isRequired,
	// lastUpdated: PropTypes.number,
	dispatch: PropTypes.func.isRequired
    }

    componentDidMount() {
	const { dispatch } = this.props;
	dispatch(fetchUsersIfNeeded())
    }

    render() {
	const { users, isFetching } = this.props
	const isEmpty = users.length === 0
	return <Users users={users} />
    }
}

const mapStateToProps = state => {
    const { users } = state
    return users || { isFetching: true, users: []}
}

export default connect(mapStateToProps)(App);
