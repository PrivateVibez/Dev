const APP_ID = 'aaaf10c903b44f4e8d2e637a888677f3'
const TOKEN = '007eJxTYLh5Kpkxhu2BxCfNtfMrOSb+3GdzZ/Lbx3xb4is5oz8ubDmowJCYmJhmaJBsaWCcZGKSZpJqkWKUamZsnmhhYWFmbp5mnFT0P+n+YYbk+rWTGRihEMRnYchNzMxjYAAA7X4jmA=='

// create Agora client
var client = AgoraRTC.createClient({
    mode: "live",
    codec: "vp8"
  });
  var localTracks = [];
  var localTrackState = {
    videoTrackEnabled: true,
    audioTrackEnabled: true
  }
  var remoteUsers = {};
  // Agora client options
  var options = {
    appid: APP_ID,
    channel: null,
    uid: null,
    token: TOKEN,
    channel: 'main'
  };
  
  $("#host-join").click(function (e) {
    options.role = "host";
  })
  
  $("#audience-join").click(function (e) {
    options.role = "audience";
  })
  
  $("#join-form").submit(async function (e) {
    e.preventDefault();
    $("#host-join").attr("disabled", true);
    $("#audience-join").attr("disabled", true);
    try {
      await join();
    } finally {
      $("#leave").attr("disabled", false);
    }
  })
  
  $("#leave").click(function (e) {
    leave();
  })
  
  async function join() {
    // create Agora client
    client.setClientRole(options.role);
    $("#mic-btn").prop("disabled", false);
    $("#video-btn").prop("disabled", false);
    if (options.role === "audience") {
      $("#mic-btn").prop("disabled", true);
      $("#video-btn").prop("disabled", true);
      // add event listener to play remote tracks when remote user publishs.
      client.on("user-published", handleUserPublished);
      client.on("user-joined", handleUserJoined);
      client.on("user-left", handleUserLeft);
    }
    // join the channel
    uid = await client.join(options.appid, options.channel, options.token || null);

    if (options.role === "host") {
      $('#mic-btn').prop('disabled', false);
      $('#video-btn').prop('disabled', false);
      client.on("user-published", handleUserPublished);
      client.on("user-joined", handleUserJoined);
      client.on("user-left", handleUserLeft);
      // create local audio and video tracks
      localTracks = await AgoraRTC.createMicrophoneAndCameraTracks();
      showMuteButton();
      // play local video track
      const player = `
        <div id="player-wrapper-${uid}">
          <p class="player-name">user ${uid}</p>
          <div id="player-${uid}" class="player"></div>
        </div>
      `
      document.getElementById('playerlist').insertAdjacentHTML('beforebegin',player);
      localTracks[1].play(`player-${uid}`);

      await client.publish(localTracks[0], localTracks[1]);
    }
  }
  
  async function leave() {
    for (trackName in localTracks) {
      var track = localTracks[trackName];
      if (track) {
        track.stop();
        track.close();
        $('#mic-btn').prop('disabled', true);
        $('#video-btn').prop('disabled', true);
        localTracks[trackName] = undefined;
      }
    }
    // remove remote users and player views
    remoteUsers = {};
    $("#remote-playerlist").html("");
    // leave the channel
    await client.leave();
    $("#local-player-name").text("");
    $("#host-join").attr("disabled", false);
    $("#audience-join").attr("disabled", false);
    $("#leave").attr("disabled", true);
    hideMuteButton();
  }
  
  async function subscribe(user, mediaType) {
    const uid = user.uid;
    // subscribe to a remote user
    await client.subscribe(user, mediaType);

    if (mediaType === "video") {
      const player = `
        <div id="player-wrapper-${uid}">
          <p class="player-name">remoteUser(${uid})</p>
          <div id="player-${uid}" class="player"></div>
        </div>
      `
      document.getElementById('playerlist').insertAdjacentHTML('beforeend',player);
      user.audioTrack.play(`player-${uid}`);
    }
    if (mediaType === "audio") {
      user.audioTrack.play(`player-${uid}`);
    }
  }
  
  // Handle user published
  let handleUserPublished = async(user, mediaType) => {
    const id = user.uid;
    remoteUsers[id] = user;
    await subscribe(user, mediaType);
  }
  
  // Handle user joined
  let handleUserJoined = async(user, mediaType) => {
    const id = user.uid;
    remoteUsers[id] = user;
    await subscribe(user, mediaType);
  }
  
  // Handle user left
  function handleUserLeft(user) {
    const id = user.uid;
    delete remoteUsers[id];
    $(`#player-wrapper-${id}`).remove();
  }

  // Mute audio click
$("#mic-btn").click(function (e) {
    if (localTrackState.audioTrackEnabled) {
      muteAudio();
    } else {
      unmuteAudio();
    }
  });
  
  // Mute video click
  $("#video-btn").click(function (e) {
    if (localTrackState.videoTrackEnabled) {
      muteVideo();
    } else {
      unmuteVideo();
    }
  })
  
  // Hide mute buttons
  function hideMuteButton() {
    $("#video-btn").css("display", "none");
    $("#mic-btn").css("display", "none");
  }
  
  // Show mute buttons
  function showMuteButton() {
    $("#video-btn").css("display", "inline-block");
    $("#mic-btn").css("display", "inline-block");
  }
  
  // Mute audio function
  async function muteAudio() {
    if (!localTracks.audioTrack) return;
    await localTracks.audioTrack.setEnabled(false);
    localTrackState.audioTrackEnabled = false;
    $("#mic-btn").text("Unmute Audio");
  }
  
  // Mute video function
  async function muteVideo() {
    if (!localTracks.videoTrack) return;
    await localTracks.videoTrack.setEnabled(false);
    localTrackState.videoTrackEnabled = false;
    $("#video-btn").text("Unmute Video");
  }
  
  // Unmute audio function
  async function unmuteAudio() {
    if (!localTracks.audioTrack) return;
    await localTracks.audioTrack.setEnabled(true);
    localTrackState.audioTrackEnabled = true;
    $("#mic-btn").text("Mute Audio");
  }
  
  // Unmute video function
  async function unmuteVideo() {
    if (!localTracks.videoTrack) return;
    await localTracks.videoTrack.setEnabled(true);
    localTrackState.videoTrackEnabled = true;
    $("#video-btn").text("Mute Video");
  }