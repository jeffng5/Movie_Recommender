// adding favorite movie to Favorite table

//favorite button
let button = document.querySelectorAll('img.favorited-movie-grid')
console.log(button)
//content of favorite button -- movie_id
const m_id = document.getElementById('title-detail').href
let attach= m_id.toString().slice(22,)
console.log(attach)
const image= document.getElementById("favorite")
console.log(image)
const image1 = document.querySelector("#unfavorite")
// const axios= require('axios')
;

console.log(image.toString())
let data ={'m_id': attach}


//axios POST request to Flask backend so that it can store to Favorite db 
async function postFavorite() {
let response = await axios.post("http://127.0.0.1:5000/post-to-favorites", data)
.then(function (response){
    console.log(response)
})
.catch(function (error){
console.log(error)

})
console.log(response.data)
console.log(image)
}

function fillIcon(){
document.getElementsByClassName("favorited-movie").id="unfavorited"
document.getElementById("unfavorite").src="../static/images/liked.png"

}



//unfavorite 

//axios POST request to Flask backend to delete Favorite from db

// let delete_m_id = document.getElementById('title-detail').href
// let delete_fav = document.getElementById('unfavorite')
// let data1= {
//     'movieId': m_id.toString.slice(22, ), "image1": delete_fav.toString()
// }


// async function deleteFavorite(){
//     let response2 = await axios.post("http://127.0.0.1:5000/post-to-favorites", {data1})
//     .then(function (response2){
//         console.log(response2)
//     })
//     .catch(function (error){
//     console.log(error)
    
//     })
//     console.log(response2.data)
//     console.log(image)
//     }




// function unfavoriteIcon(){
// button.innerHTML = '<img class="favorited-movie-grid" id="unfavorite" src="../static/images/favorited.png" height="25" width="25">'
// }

for (let ele of button){
    ele.addEventListener("click", function(){postFavorite(); fillIcon()})
    }

// for (let ele of button){
// ele.addEventListener("doubleclick", function() {deleteFavorite()})

// }
    
    
//     ; fillIcon()}

// catch(err){deleteFavorite(); unfavoriteIcon()}})

















//POST request on click of icon
// button.addEventListener("click", function(){postFavorite(); fillIcon()})



//adding watched movie to Watched table 

//getting the movie id data 
// const m_id_watched = document.getElementById('title-detail')

// //naming the button
// const button1 = document.getElementsByClassName('watched-movie-grid')

// //axios POST request to Flask backend to store to Watched db
// async function postWatched(){
// let resp = await axios.post("http://127.0.0.1:5000/post-to-watched", {m_id_watched})
// console.log(resp.data)
// }

// function fillIconW(){
//     button1.innerHTML('<img class="favorited-movie-grid" src="../static/images/watched-filled.png" height="25" width="25">')
// }



// //POST request on click on the watched icon
// button1.addEventListener("click", function() {postWatched(); fillIconW()
//})

