import React, { Component, PropTypes } from 'react';
import { connect } from 'react-redux';
import { fetchUsersIfNeeded } from './actions'
import { Users } from './users'



class App extends Component {
    static propTypes = {
	items: PropTypes.array.isRequired,
	isFetching: PropTypes.bool.isRequired,
	// isInvalidated: PropTypes.bool.isRequired,
	// lastUpdated: PropTypes.number,
	dispatch: PropTypes.func.isRequired
    }

    componentDidMount() {
	const { dispatch } = this.props;
	dispatch(fetchUsersIfNeeded())
    }

    render() {
	const { items, isFetching } = this.props
	const isEmpty = items.length === 0
	return <Users users={items} />
    }
}

const mapStateToProps = state => {
    const { users } = state
    return users || { isFetching: true, items: []}
}

export default connect(mapStateToProps)(App);
