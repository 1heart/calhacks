var AutoCompleteSelect = React.createClass({displayName: 'AutoCompleteSelect',

	getInitialState: function(){
		return { searchString: '' };
	},

	handleChange: function(e){

		this.setState({searchString:e.target.value});
	},

	handleClick: function(e) {
		this.setState({currUser: e.target.innerText});
	},

	render: function() {

		var libraries = this.props.items,
		searchString = this.state.searchString.trim().toLowerCase();

		if(searchString.length > 0){
            // We are searching. Filter the results.
            libraries = libraries.filter(function(l){
            	return l.toLowerCase().match( searchString );
            });
            for (var i=0; i<libraries.length; i++) {
            	libraries[i] = <li onClick={this.handleClick}>{libraries[i]}</li>
            }

	        return 	<div>
				        <input type="text" value={this.state.searchString} onChange={this.handleChange} placeholder="Search here for recipient ID" />
				        <ul> 
				        	{libraries}

				        </ul>
			        <PayForm currUser={this.state.currUser}/>

			        </div>
			        ;
        }

        return 	<div>
			        <input type="text" value={this.state.searchString} onChange={this.handleChange} placeholder="Search here for recipient ID" />
			    <PayForm />
		        </div>
		        ;

    }
});

var PayForm = React.createClass({ displayName: 'PayForm',
	render: function() {
		return (
			<form className="payForm">
				Pay <input  style={{'display': 'inline'}} type="number" /> BTC to { this.props.currUser || 'a friend'} <input  style={{'display': 'inline'}} type="hidden" value={this.props.currUser} /> for 
				<input style={{'display': 'inline'}} type="text" />
			</form>
			);
	}

});



var dummy  = ['1heart', 'cosmicac', 'vincent']


ReactDOM.render(
		<AutoCompleteSelect items={dummy} />,
		document.getElementById('autoCompleteSelect')
	);