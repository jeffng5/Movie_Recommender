// adding favorite movie to Favorite table

//favorite button
let button = document.querySelector('img.favorited-movie')
console.log(button)
//content of favorite button -- movie_id
let m_id = document.getElementsByTagName('h3')[0].id
// let fav= document.getElementById('favorite')
// console.log(fav)
console.log(m_id)

// const axios= require('axios')

// let data ={'movie_id':m_id}


//axios POST request to Flask backend so that it can store to Favorite db 
async function postFavorite() {
let response = await axios.post("http://127.0.0.1:5000/post-to-favorites", {'movie_id' : m_id})
.then(function (response){
    console.log(response)
})
.catch(function (error){
console.log(error)

})
console.log('OK')
}

function fillIcon(){
// document.getElementsByClassName("favorited-movie").id="unfavorited"
let ele= document.getElementsByTagName("img")[1]
console.log(ele)
ele.src = "../static/images/liked.png"
ele.id= 'unfavorite'

}

function laggard(){
let ele1 = document.getElementsByTagName("img")[1]
}

button.addEventListener("click", function(){postFavorite(); fillIcon()})
//unfavorite 

//axios POST request to Flask backend to delete Favorite from db

// let delete_m_id = document.getElementById('title-detail').href
// let delete_fav = document.getElementById('unfavorite')
// let data1= {
//     'movieId': m_id.toString.slice(22, ), "image1": delete_fav.toString()
// }

// bttn= document.getElementById('unfavorite')

// bttn.addEventListener("click", function(){try {unfillIcon()}
// catch{err} 

async function deleteFavorite(){
    let response2 = await axios.post("http://127.0.0.1:5000/post-to-unfavorites", {'movie_id' : m_id})
    .then(function (response2){
        console.log(response2)
    })
    .catch(function (error){
    console.log(error)
    
    })
    console.log(response2.data)
    console.log(image)
    }

function unfillIcon() {
        let ele= document.getElementByTagName("img")[1].classList.toggle("yellow")
        console.log(ele)
        ele.src = "../static/images/unliked.png"
        ele.id= 'favorite'
}

button.addEventListener('mousedown', function(){ deleteFavorite(); unfillIcon()})

// function unfavoriteIcon(){
// button.innerHTML = '<img class="favorited-movie-grid" id="unfavorite" src="../static/images/favorited.png" height="25" width="25">'
// }




//}


// })














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
