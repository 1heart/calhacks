var AutoCompleteSelect = React.createClass({displayName: 'AutoCompleteSelect',

	getInitialState: function(){
		return { searchString: '' };
	},

	handleChange: function(e){

		this.setState({searchString:e.target.value});
	},

	handleClick: function(e) {
		console.log(e);
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
            	libraries[i] = <li onClick={this.handleClick(i)}>{libraries[i]}</li>
            }

	        return 	<div>
				        <input type="text" value={this.state.searchString} onChange={this.handleChange} placeholder="Type here" />
				        <ul> 
				        	{libraries}

				        </ul>
			        <PayForm />

			        </div>
			        ;
        }

        return 	<div>
			        <input type="text" value={this.state.searchString} onChange={this.handleChange} placeholder="Type here" />
			    <PayForm />
		        </div>
		        ;

    }
});

var PayForm = React.createClass({ displayName: 'PayForm',
	getInitialState: function() {
		return {};
	},
	render: function() {
		return <div>FORM</div>
	}

});



var dummy  = ['1heart', 'cosmicac', 'vincent']


ReactDOM.render(
		<AutoCompleteSelect items={dummy} />,
		document.getElementById('autoCompleteSelect')
	);