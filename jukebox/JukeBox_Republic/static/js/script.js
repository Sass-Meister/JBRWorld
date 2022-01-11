
function fill(data)
{
  $("#songname").html(data.songname)
  $("#album").attr("src", data.album_url)
  $("#artist").html(data.artist)
}

//$(document.ready())
setInterval(
  function(x) //repeated function
  {
    $.get(
        "refresh/",
        {},
        fill
    )
  },
  1000 //interval in ms
)


