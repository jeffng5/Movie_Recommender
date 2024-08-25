

// let fav= document.getElementById('favorite')
// console.log(fav)


// const axios= require('axios')

// let data ={'movie_id':m_id}

// function fillIcon(){

// let ele= document.getElementsByTagName("img")[1]
// console.log(ele)
// ele.src = "../static/images/liked.png"
// ele.id= 'unfavorite'

// }



    

// function unfillIcon() {
//         let ele2= document.getElementsByTagName("img")[1]
//         console.log(ele2)
//         ele2.src = "../static/images/unliked.png"
//         ele2.id= 'favorite'
// }

// async function deleteFavorite(){

//     let response2 = await axios.post("http://127.0.0.1:5000/post-to-unfavorites", {'movie_id' : m_id})
//         console.log(response2)}


// async function postFavorite(){
//     let movie_title = document.getElementsByClassName('movie').value
//     console.log(movie_title)
//     // let resp = await axios.post("http://127.0.0.1:5000/post-to-favorites", {'movie_id' : m_id, 'title': movie_title })
//     }

// const button = document.querySelector('img.favorited-movie')

// console.log(button)



// button.addEventListener("click", async()=> {postFavorite() ; fillIcon()})

// button.addEventListener('dblclick', async()=> {deleteFavorite(); unfillIcon()})



// let m_id_watched = document.getElementsByTagName('h3')[0].id
// // //naming the button
// const button1 = document.querySelector('img.watched-movie')
// console.log(button1)
// // //axios POST request to Flask backend to store to Watched db
// async function postWatched(){
//     let resp3 = await axios.post("http://127.0.0.1:5000/post-to-watched", {"movie_id" :m_id_watched})

// }

// function fillIconW(){
//     let watchIcon = document.getElementsByTagName('img')[2]
//     watchIcon.src = "../static/images/watched-filled.png"
//     watchIcon.id= "watched"
// }
// button1.addEventListener("click", function(){postWatched(); fillIconW()})

// async function postUnwatched(){
//     let resp4 = await axios.post("http://127.0.0.1:5000/post-to-unwatched", {"movie_id": m_id_watched})
//    }

// function unfillIconW(){    
//     let watchIconU = document.getElementsByTagName('img')[2]
//     watchIconU.src = "../static/images/check-eye.png"
//     watchIconU.id = "unwatched"
// }

// button1.addEventListener("dblclick", function(){postUnwatched(); unfillIconW() })




// async function deleteFavoriteFromList(){

//     let response2 = await axios.post("http://127.0.0.1:5000/favorited-watched", {'movie_id' : m_id})
//         console.log(response2)}


