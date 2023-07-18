const APP_ID = 'aaaf10c903b44f4e8d2e637a888677f3'
const CHANNEL = 'main'
const TOKEN = '007eJxTYLh5Kpkxhu2BxCfNtfMrOSb+3GdzZ/Lbx3xb4is5oz8ubDmowJCYmJhmaJBsaWCcZGKSZpJqkWKUamZsnmhhYWFmbp5mnFT0P+n+YYbk+rWTGRihEMRnYchNzMxjYAAA7X4jmA=='
let UID

config = {
    mode: "live", 
    codec: "vp8",
}

const client = AgoraRTC.createClient(config)

let localTracks = []
let remoteUsers = {}

let joinAndDisplayLocalStream = async () => {
    client.on('user-published', handleUserJoined)

    UID = await client.join(APP_ID, CHANNEL, TOKEN, null)
    if(config.role === "host"){

        localTracks = await AgoraRTC.createMicrophoneAndCameraTracks()

        let player = `
                    <div class="video-container" id="user-container-${UID}">
                        <div class="username-wrapper"><span class="username">username</span></div>
                        <div class="video-player" id="user-${UID}"></div>
                    </div>
                    `
        document.getElementById('video-streams').insertAdjacentHTML('beforeend', player)

        localTracks[1].play(`user-${UID}`)

        await client.publish([localTracks[0], localTracks[1]])
    }
}

handleUserJoined = async (user, mediaType) => {
    remoteUsers[user.uid] = user
    await client.subscribe(user, mediaType)

    if(mediaType === 'video'){
        let player = document.getElementById(`user-container-${user.uid}`)
        if(player != null){
            player.remove()
        }
    
        player = `
                    <div class="video-container" id="user-container-${user.uid}">
                        <div class="username-wrapper"><span class="username">username</span></div>
                        <div class="video-player" id="user-${user.uid}"></div>
                    </div>
                    `
        document.getElementById('video-streams').insertAdjacentHTML('beforeend', player)
        user.videoTrack.play(`user-${user.uid}`)
    }
    if(mediaType === 'audio'){
        user.audioTrack.play()
    }
}

$("#host").click(function (e) {
    config.role = "host";
    client.setClientRole("host");
    joinAndDisplayLocalStream()
  })
  
$("#audience").click(function (e) {
config.role = "audience";
client.setClientRole("audience");
joinAndDisplayLocalStream()
}) 
