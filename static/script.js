// const input = document.querySelector('#fruit');
// const suggestions = document.querySelector('.suggestions ul');

//cleaning the fruit list
const fruits = ['Apple', 'Apricot', 'Avocado', 'Banana', 'Bilberry', 'Blackberry', 'Blackcurrant', 'Blueberry', 'Boysenberry', 'Currant', 'Cherry', 'Coconut', 'Cranberry', 'Cucumber', 'Custard apple', 'Damson', 'Date', 'Dragonfruit', 'Durian', 'Elderberry', 'Feijoa', 'Fig', 'Gooseberry', 'Grape', 'Raisin', 'Grapefruit', 'Guava', 'Honeyberry', 'Huckleberry', 'Jabuticaba', 'Jackfruit', 'Jambul', 'Juniper berry', 'Kiwifruit', 'Kumquat', 'Lemon', 'Lime', 'Loquat', 'Longan', 'Lychee', 'Mango', 'Mangosteen', 'Marionberry', 'Melon', 'Cantaloupe', 'Honeydew', 'Watermelon', 'Miracle fruit', 'Mulberry', 'Nectarine', 'Nance', 'Olive', 'Orange', 'Clementine', 'Mandarine', 'Tangerine', 'Papaya', 'Passionfruit', 'Peach', 'Pear', 'Persimmon', 'Plantain', 'Plum', 'Pineapple', 'Pomegranate', 'Pomelo', 'Quince', 'Raspberry', 'Salmonberry', 'Rambutan', 'Redcurrant', 'Salak', 'Satsuma', 'Soursop', 'Star fruit', 'Strawberry', 'Tamarillo', 'Tamarind', 'Yuzu']
const cleanFruits = fruits.map(fruit => fruit.toLowerCase());

// getting a search term from user input	
function addSelect2(event) {
	let searchTerm = event.target.value
	const fruitFilter = cleanFruits.filter(function (val) { return val.includes(searchTerm) });
	let select = document.querySelector("select");
	select.innerHTML = ""
//display the matching items **not original code, forgot to cite	
	for (let i = 0; i < fruitFilter.length; i++) {
		let opt = fruitFilter[i];
		let el = document.createElement("option");
		el.textContent = opt;
		el.value = opt;
		el.id = opt
		select.appendChild(el);} 
}
// event listeners 
let bttn = document.querySelector('input#fruit')
bttn.addEventListener('keyup', (event) => {
	event.preventDefault();
	addSelect2(event)
})

// code to place the dropdown selection into the searchBar 

let select = document.querySelector('select')
select.addEventListener("click", (e) => {
	e.preventDefault();
	bttn.value = e.target.value
})
	



