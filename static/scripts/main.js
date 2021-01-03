console.log("Javascript Loaded.");
currrent_video_id = 0
firstRun = true

clips_processed = []

next_video = "";

document.getElementById("goodbutton").onclick = function(){
    document.getElementById("goodoutput").textContent += clips_processed[currrent_video_id] + "\n";

    var bad_lines = document.getElementById("badoutput").textContent.split("\n")
    var long_lines = document.getElementById("longoutput").textContent.split("\n")

    if(bad_lines.includes(clips_processed[currrent_video_id])){
        index = bad_lines.indexOf(clips_processed[currrent_video_id])
        bad_lines.splice(index, 1)
        document.getElementById("badoutput").textContent = bad_lines.join("\n")
    }

    if(long_lines.includes(clips_processed[currrent_video_id])){
        index = long_lines.indexOf(clips_processed[currrent_video_id])
        long_lines.splice(index, 1)
        document.getElementById("longoutput").textContent = long_lines.join("\n")
    }
}

document.getElementById("badbutton").onclick = function(){
    document.getElementById("badoutput").textContent += clips_processed[currrent_video_id]+ "\n";

    var good_lines = document.getElementById("goodoutput").textContent.split("\n")
    var long_lines = document.getElementById("longoutput").textContent.split("\n")

    if(good_lines.includes(clips_processed[currrent_video_id])){
        index = good_lines.indexOf(clips_processed[currrent_video_id])
        good_lines.splice(index, 1)
        document.getElementById("goodoutput").textContent = good_lines.join("\n")
    }

    if(long_lines.includes(clips_processed[currrent_video_id])){
        index = long_lines.indexOf(clips_processed[currrent_video_id])
        long_lines.splice(index, 1)
        document.getElementById("longoutput").textContent = long_lines.join("\n")
    }
}

document.getElementById("longbutton").onclick = function(){
    document.getElementById("longoutput").textContent += clips_processed[currrent_video_id] + "\n";

    var good_lines = document.getElementById("goodoutput").textContent.split("\n")
    var bad_lines = document.getElementById("badoutput").textContent.split("\n")

    if(good_lines.includes(clips_processed[currrent_video_id])){
        index = good_lines.indexOf(clips_processed[currrent_video_id])
        good_lines.splice(index, 1)
        document.getElementById("goodoutput").textContent = good_lines.join("\n")
    }

    if(bad_lines.includes(clips_processed[currrent_video_id])){
        index = bad_lines.indexOf(clips_processed[currrent_video_id])
        bad_lines.splice(index, 1)
        document.getElementById("badoutput").textContent = bad_lines.join("\n")
    }
}

function loadVideo(value) {
    console.log("Loading Video with id " + value)
    var video = document.getElementsByTagName('video')[0];
    var sources = video.getElementsByTagName('source');
    sources[0].src = '/static/videos/'+value+'.mp4';
    video.load();
}

$(function() {
    $('#nextbutton').on('click', function(e) {
        document.getElementById("nextbutton").disabled = true;
        setTimeout(function(){document.getElementById("nextbutton").disabled = false;},10000);

        e.preventDefault()

        if (firstRun) {
            var lines = document.getElementById("input-textarea").value.split('\n');
            if(document.getElementById("input-textarea").value.length > 5){
                    
                c = "despacito"
                $.post( "/initial_download", {
                    post1:lines[0], 
                    post2:lines[1],
                    post3:lines[2]
                })

                clips_processed.push(lines[0])
                clips_processed.push(lines[1])
                clips_processed.push(lines[2])


                lines.shift();
                lines.shift();
                lines.shift();

                var new_lines = lines.join("\n")
                document.getElementById("input-textarea").value = new_lines

                alert("First few videos are being downloaded, video player will update in a few seconds...")
                setTimeout(() => {  loadVideo(0); }, 10000);
                firstRun = false

                $.post( "/reset_folders", {
                    data:"fuck you get out my code"
                })
            } else {
                alert("Do you have disabilities? Input some clips first you bellend.")
            }

            
        } else {
            loadVideo(currrent_video_id+1)
            currrent_video_id = currrent_video_id+1
            if(document.getElementById("input-textarea").value.length > 5){
                var lines = document.getElementById("input-textarea").value.split('\n');
                console.log("Downloading " + lines[0])
                $.post( "/download_video", {post_url: lines[0]})
    
                clips_processed.push(lines[0])
                lines.shift()
                
                var new_lines = lines.join("\n")
                document.getElementById("input-textarea").value = new_lines
            } else {
                alert("No videos left...")
            }
        }
    });
  });