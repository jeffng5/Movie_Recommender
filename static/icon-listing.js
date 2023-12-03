// adding favorite movie to Favorite table

//favorite button
const button = document.getElementsByClassName('favorited-movie-grid')

//content of favorite button -- movie_id
const m_id = document.getElementById('title-detail').innerHTML
const image= document.getElementById("favorite")
const image1 = document.getElementById("unfavorite")
console.log(m_id)

//axios POST request to Flask backend so that it can store to Favorite db 
async function postFavorite() {
let response = await axios.post("http://127.0.0.1:5000/post-to-favorites", {'movie_id': m_id, 'image' :image, "image1": image1})
console.log(response.data)
console.log(image)
}

function fillIcon(){
button.innerHTML('<img class="favorited-movie-grid" id= "favorite" src="../static/images/star-filled.png" height="25" width="25">')
}

button.addEventListener("click", function(){try {postFavorite(); fillIcon()}

catch(err){deleteFavorite(); unfavoriteIcon()}
    }
    )


//unfavorite 

//axios POST request to Flask backend to delete Favorite from db
async function deleteFavorite(){
    let response2 = await axios.post("http://127.0.0.1:5000/post-to-favorites", {'movie_id':m_id, 'image': image, "image1": image1})
    console.log(response2.data)

}


function unfavoriteIcon(){
button.innerHTML('<img class="favorited-movie-grid" id="unfavorite" src="../static/images/favorited.png" height="25" width="25">')
}

button.addEventListener("click", function(){ deleteFavorite(); unfavoriteIcon()


})




















//POST request on click of icon
button.addEventListener("click", function(){postFavorite(); fillIcon()})



//adding watched movie to Watched table 

//getting the movie id data 
const m_id_watched = document.getElementById('title-detail')

//naming the button
const button1 = document.getElementsByClassName('watched-movie-grid')

//axios POST request to Flask backend to store to Watched db
async function postWatched(){
let resp = await axios.post("http://127.0.0.1:5000/post-to-watched", {m_id_watched})
console.log(resp.data)
}

function fillIconW(){
    button1.innerHTML('<img class="favorited-movie-grid" src="../static/images/watched-filled.png" height="25" width="25">')
}



//POST request on click on the watched icon
button1.addEventListener("click", function() {postWatched(); fillIconW()
})

