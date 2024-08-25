
let m_id = document.getElementsByTagName('h3')[0].id


function favoriteIcon() {
    let icon = document.getElementsByTagName("img")[1]
    console.log(icon)
    icon.src = '../static/images/liked.png'
    icon.id = 'unfavorite'

}

async function callToPostLike() {

    let title = document.getElementsByTagName('h3')[0].innerText
    console.log(title)
    fetch(`/${m_id}`,
        {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                title: `${title}`
            }),
        }).then(response => response.json()).then(data => console.log(data))
        .catch((err)=>{
            console.log(err)
        })
}


let button = document.getElementsByTagName("img")[1]
console.log(button)
button.addEventListener('click', function (e) { e.preventDefault(); favoriteIcon(); callToPostLike() })



function watchedIcon() {
    let icon = document.getElementsByTagName('img')[2]
    icon.src = '../static/images/watched-filled.png'
    icon.id = 'unwatched'

}

async function callToWatched() {

    fetch(`/post-to-watched`,
        {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                movie_id: `${m_id}`
            }),
        }).then(response => response.json()).then(data => console.log(data))
        .catch((err)=>{
            console.log(err)
        })
}

let watchedButton = document.getElementsByTagName("img")[2]
console.log(watchedButton)
watchedButton.addEventListener('click', function (e) { e.preventDefault(); watchedIcon(); callToWatched() })