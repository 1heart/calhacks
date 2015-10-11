var AutoCompleteSelect = React.createClass({displayName: 'AutoCompleteSelect',

	getInitialState: function(){
		return { searchString: '' };
	},

	handleChange: function(e){

		this.setState({searchString:e.target.value});
	},

	handleClick: function(e) {
		var newUser = e.target.innerText;
		if (newUser.length > 0) {
			this.setState({currUser: newUser});
		}
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
            	libraries[i] = <li className="dropdown-box" onClick={this.handleClick}>{libraries[i]}</li>
            }

	        return 	<div><h1 id="highlightBlue">Pay {this.state.currUser || ''}</h1><div className="input-search-wrapper">
				        <input type="text" className="input-search"value={this.state.searchString} onChange={this.handleChange} placeholder="Search here for recipient ID"/>
				        <ul> 
				        	{libraries}

				        </ul>
			        </div>
			        <PayForm currUser={this.state.currUser}/>

			        </div>
			        ;
        }

        return <div><h1>Pay {this.state.currUser || ''}</h1><div className="input-search-wrapper">
			        <input type="text" className="input-search" value={this.state.searchString} onChange={this.handleChange} placeholder="Search here for recipient ID"/>
			   	</div>
			    <PayForm />
		        </div>
		        ;

    }
});

var PayForm = React.createClass({ displayName: 'PayForm',
	render: function() {
		return (
			<form className="payForm">
				<div className="input-search-wrapper">
					<input className="input-search" type="number"  placeholder="Payment Amount"/><input  style={{'display': 'inline'}} type="hidden" value={this.props.currUser}/> 
				</div>
				<div className="input-search-wrapper">
					<input className="input-search" type="text" placeholder="Description"/>
				</div>
			</form>
			);
	}

});



var dummy  = ['1heart', 'cosmicac', 'vincent']


ReactDOM.render(
		<AutoCompleteSelect items={dummy} />,
		document.getElementById('autoCompleteSelect')
	);