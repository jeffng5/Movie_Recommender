
const mid = document.getELementById('title-detail').innerHTML
console.log(mid)


async function postFavorite() {
    
    let response = await axios.post("http://127.0.0.1:5000/post-to-favorites", mid)
    console.log(response.data)

}

const icon = document.querySelector('img.favorite-movie-grid')

icon.addEventListener("click", function(){postFavorite()
}
)