var dummy  = ['1heart', 'cosmicac', 'vincent']

var autocomplete = function(listOfNames, currString) {
	var resultArray = [];
	for (i = 0; i < listOfNames.length; i++) {
		if (listOfNames[i].indexOf(currString) > -1) {
			resultArray.push(listOfNames[i]);
		}
	}
	return resultArray;
}





