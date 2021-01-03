console.log("Javascript Loaded.");
currrent_video_id = 0
firstRun = true

clips_processed = ["https://www.reddit.com/r/perfectlycutscreams/comments/cvt1s9/nword_ticket/",
"https://www.reddit.com/r/perfectlycutscreams/comments/hkyiz5/i_dont_think_he_has_a_gf_anymore/",
"https://www.reddit.com/r/perfectlycutscreams/comments/ehmr54/i_peaked_in_terms_of_laziness_last_night/"]

next_video = "";

document.getElementById("goodbutton").onclick = function(){
    document.getElementById("goodoutput").textContent += clips_processed[currrent_video_id] + "\n";
}

document.getElementById("badbutton").onclick = function(){
    document.getElementById("badoutput").textContent += clips_processed[currrent_video_id]+ "\n";
}

document.getElementById("longbutton").onclick = function(){
    document.getElementById("longoutput").textContent += clips_processed[currrent_video_id] + "\n";
}

function loadVideo(value) {
    var video = document.getElementsByTagName('video')[0];
    var sources = video.getElementsByTagName('source');
    sources[0].src = '/static/videos/'+value+'.mp4';
    video.load();
}

$(function() {
    $('#nextbutton').on('click', function(e) {
        e.preventDefault()

        if (firstRun) {
            
            c = "despacito"
            $.post( "/initial_download", {post_urls: c})

            alert("First few videos are being downloaded, video player will update in a few seconds...")
            setTimeout(() => {  loadVideo(1); }, 10000);
            firstRun = false
            
        } else {
            loadVideo(currrent_video_id+1)
            currrent_video_id = currrent_video_id+1
            if(document.getElementById("input-textarea").value.length > 5){
                console.log("Downloading Video " + current_video)
                $.post( "/download_video", {post_url: current_video})
    
                console.log(current_video)
                clips = document.getElementById("input-textarea").value.split("\n");
                current_video = clips.pop();
                console.log(current_video)
            
                document.getElementById("input-textarea").value = clips.join("\n")
    
            } else {
                alert("No videos left...")
            }
        }
    });
  });