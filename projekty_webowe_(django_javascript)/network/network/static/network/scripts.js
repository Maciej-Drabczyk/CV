document.addEventListener("DOMContentLoaded", () => {
    //All_posts
    if(document.querySelector('#new_post_form') != null) {
        document.querySelector('#new_post_form').addEventListener('submit', (e) => {
            e.preventDefault()
            const content = document.querySelector('.form-control').value
            fetch("/new_post", {
                method: "POST",
                body: JSON.stringify({
                    content: content
                })
            })
            .then(response => response.json())
            .then(data => {
                location.reload()
            })
        })
    }

    //profile_page
    if(document.querySelector('#follow_button') != null) {
        const follow = document.querySelector('#follow_button')
        follow.addEventListener('click', () => follow_toggle(true, follow.dataset.profile))
        const unfollow = document.querySelector('#unfollow_button')
        unfollow.addEventListener('click', () => follow_toggle(false, unfollow.dataset.profile))
    }

    if(document.querySelector(".post") != null) {
        like_buttons()
    }

    if(document.querySelector(".edit") != null) {
        edit_buttons()
    }
})

function like_buttons() {
    document.querySelectorAll('.like').forEach(like => {
        like.addEventListener('click', () => {
            like_dislike(true, like.dataset.id)
        })
    })

    document.querySelectorAll('.dislike').forEach(dislike => {
        dislike.addEventListener('click', () => {
            like_dislike(false, dislike.dataset.id)
        })
    })
}


function like_dislike(toggle, id) {
    fetch("/like_toggle", {
        method: "POST",
        body: JSON.stringify({
            toggle: toggle,
            id: id
        })
    })
    .then(response => response.json())
    .then(data => {
        if(toggle) {
            document.querySelector(`[data-id="${id}"][data-type="like"]`).style.display = "none"
            document.querySelector(`[data-id="${id}"][data-type="dislike"]`).style.display = "block"
        }
        else {
            document.querySelector(`[data-id="${id}"][data-type="like"]`).style.display = "block"
            document.querySelector(`[data-id="${id}"][data-type="dislike"]`).style.display = "none"
        }
        document.querySelector(`[data-id="${id}"][data-type="like_count"]`).innerHTML = `Likes: ${data[`${id}`]}`
    })
}

function edit_buttons() {
    document.querySelectorAll('.edit').forEach(edit => {
        edit.addEventListener('click', () => {
            edit.style.display = "none"
            start_edit_post( edit.dataset.id)
        })
    })
    document.querySelectorAll('.accept').forEach(accept => {
        accept.addEventListener('click', () => {
            edit(accept.dataset.id)           
        })
    })
}

function start_edit_post(post_id) {
    const content = document.querySelector(`[data-id="${post_id}"][data-type="post_content"]`)
    content.style.display="none"

    const textarea = document.querySelector(`[data-id="${post_id}"][data-type="post_edit"]`)
    textarea.value = content.innerHTML
    textarea.style.display = "block"

    const accept = document.querySelector(`[data-type="accept"][data-id="${post_id}"]`)
    accept.style.display="block"   
}

function edit(post_id) {
    console.log("XD");
    
    const content = document.querySelector(`[data-id="${post_id}"][data-type="post_content"]`)
    const textarea = document.querySelector(`[data-id="${post_id}"][data-type="post_edit"]`)
    const accept = document.querySelector(`[data-type="accept"][data-id="${post_id}"]`)
    
    fetch('/edit', {
        method: "PUT",
        body: JSON.stringify({
            post_id: post_id,
            new_content: textarea.value
        })
    })
    .then(response => response.json())
    .then(data => {
        accept.style.display="none"

        content.style.display="block"
        content.innerHTML = textarea.value

        textarea.style.display = "none"

        document.querySelector(`[data-id="${post_id}"][data-type="edit"]`).style.display = "block"
    }) 
}

function follow_toggle(toggle, profile) {
    fetch("/follow_toggle", {
        method: "POST",
        body: JSON.stringify({
            profile: profile,
            toggle: toggle
        })
    })
    .then(response => response.json())
    .then(data => {
        if(toggle) {
            document.querySelector("#follow_button").style.display = "none"
            document.querySelector("#unfollow_button").style.display = "block"
        } 
        else {
            document.querySelector("#follow_button").style.display = "block"
            document.querySelector("#unfollow_button").style.display = "none"  
        }
        document.querySelector('#follows_count').innerHTML = data['count']
    })
}