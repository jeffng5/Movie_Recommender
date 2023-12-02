
const m_id = document.getElementById('heading')
console.log(m_id)


async function postFavorite() {
    
let response = await axios.post("http://127.0.0.1:5000/post-to-favorites", {m_id})
console.log(response.data)

}

postFavorite()

// const icon = document.getElementById('heading')

// icon.addEventListener("click", function(){postFavorite()
// }
// )

