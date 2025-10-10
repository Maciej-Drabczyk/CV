document.addEventListener("DOMContentLoaded", () => {


    document.querySelector('#new_post_form').onsubmit = function(e) {
        e.preventDefault()
        const content = document.querySelector('.form-control').value;
        fetch('/new_post', {
            method: 'POST',
            body: JSON.stringify({
                content: content
            })
        })
        .then(response => response.json())
        .then(data => {
            load_posts()
        })
    }

    load_posts()
})

function load_posts() {
    document.querySelector('#all_posts').style.display = "block"
    document.querySelector('#profile_page').style.display = "none"

    document.querySelector('.form-control').value = ""

    document.querySelector('#posts_list').innerHTML = ""

    fetch('posts')
    .then(response => response.json())
    .then(posts => {
        posts.forEach(post => {
            document.querySelector("#posts_list").insertAdjacentHTML('beforeend', 
                `<div class="post">
                    <b class="post_creator">${post['creator']}</b>
                    <p>${post['content']}<p>
                    <p> <3 </p>
                    <small>${post['date']}</small>
                </div>`
            )
        });

        document.querySelectorAll(".post_creator").forEach(post => {
            const user = JSON.parse(document.getElementById('user').textContent)
            if(post.innerHTML === user) {
                post.insertAdjacentHTML('afterend', `<p>Edit</p>`)
            }
        })
    })
}

function load_profile() {
    document.querySelector('#all_posts').style.display = "none"
    document.querySelector('#profile_page').style.display = "block"
}

