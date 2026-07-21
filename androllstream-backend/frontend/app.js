async function api(url, method = "GET", data = null) {
    let options = { method };
    if (data instanceof FormData) options.body = data;
    return await fetch(url, options).then(r => r.json());
}

// Homepage – load videos
if (document.getElementById("video-list")) {
    api("/api/videos/all").then(videos => {
        let list = document.getElementById("video-list");
        videos.forEach(v => {
            let div = document.createElement("div");
            div.innerHTML = `
                <a href="video.html?id=${v.id}">
                    <div class="thumb"></div>
                    <h3>${v.title}</h3>
                </a>
            `;
            list.appendChild(div);
        });
    });
}

// Video player
if (window.location.pathname.endsWith("video.html")) {
    const params = new URLSearchParams(window.location.search);
    const id = params.get("id");

    api(`/api/videos/${id}`).then(video => {
        document.getElementById("video-title").innerText = video.title;
        document.getElementById("video-description").innerText = video.description;
        document.getElementById("player").src = `/api/stream/${id}/playlist.m3u8`;
    });
}

// Upload
if (document.getElementById("upload-form")) {
    document.getElementById("upload-form").onsubmit = async e => {
        e.preventDefault();
        let form = new FormData(e.target);
        let res = await api("/api/videos/upload", "POST", form);
        document.getElementById("upload-result").innerText = JSON.stringify(res, null, 2);
    };
}

// Register
if (document.getElementById("register-form")) {
    document.getElementById("register-form").onsubmit = async e => {
        e.preventDefault();
        let form = new FormData(e.target);
        let res = await api("/api/users/register", "POST", form);
        alert("Account created!");
        window.location = "login.html";
    };
}

// Login
if (document.getElementById("login-form")) {
    document.getElementById("login-form").onsubmit = async e => {
        e.preventDefault();
        let form = new FormData(e.target);
        let res = await api("/api/users/login", "POST", form);
        localStorage.setItem("user_id", res.id);
        alert("Logged in!");
        window.location = "index.html";
    };
}

// Channel page
if (window.location.pathname.endsWith("channel.html")) {
    const params = new URLSearchParams(window.location.search);
    const id = params.get("id");

    api(`/api/channels/${id}`).then(channel => {
        document.getElementById("channel-name").innerText = channel.name;
        document.getElementById("channel-description").innerText = channel.description;
    });

    api(`/api/videos/channel/${id}`).then(videos => {
        let list = document.getElementById("channel-videos");
        videos.forEach(v => {
            let div = document.createElement("div");
            div.innerHTML = `
                <a href="video.html?id=${v.id}">
                    <div class="thumb"></div>
                    <h3>${v.title}</h3>
                </a>
            `;
            list.appendChild(div);
        });
    });
}
