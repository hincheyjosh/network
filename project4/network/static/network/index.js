
function editPost(id) {
    const postBody = document.querySelector(`#post${id}body`)
    postBody.style.display = "none"
    const editView = document.querySelector(`#editView${id}`)
    editView.style.display = "block"

    const form = document.querySelector(`#editForm${id}`)

    form.addEventListener("submit", function() {
        const body = document.querySelector(`#editText${id}`).value
        fetch(`/edit/${id}`, {
            method: 'POST',
            body: JSON.stringify({
                body: body
            })
        })
        .then(() => {
            postBody.innerHTML = body
            editView.style.display = 'none'
            postBody.style.display = 'block'
        })
    })
    return false
}


function like(id) {
    fetch(`/like/${id}`, {
        method: 'POST',
        body: JSON.stringify({
            like: 'yes'
        })
    })
    .then(response => response.json())
    .then(data => {
        document.querySelector(`#likeSection${id}`).innerHTML = `
        <p  id="likeSection{{post.id}}" class="card-text like" onclick="unlike(${id})"
        >&#129293; ${data[0]['likes']}</p>`
    })
    return false
}


function unlike(id) {
    fetch(`/like/${id}`, {
        method: 'POST',
        body: JSON.stringify({
            like: 'no'
        })
    })
    .then(response => response.json())
    .then(data => {
        document.querySelector(`#likeSection${id}`).innerHTML = `
        <p id="likeSection{{post.id}}" class="card-text like" onclick="like(${id})"
        >&#129293; ${data[0]['likes']}</p>`
    })
    return false
}


