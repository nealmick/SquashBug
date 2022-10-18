

function completeBug(){
  console.log('completeBug')

  url = window.location.href
  url = url.split('/')
  var pk = url[url.length - 1];
  console.log(pk)
  location.href='/complete/'+pk

}

function delBug(){
  console.log('delBUg')

  url = window.location.href
  url = url.split('/')
  var pk = url[url.length - 1];
  console.log(pk)
  location.href='/del/'+pk

}
function save(){
    id_title = document.getElementById("id_title").value
    id_description = document.getElementById("id_description").value
    var s = document.getElementById( "id_severity" );
    id_severity = s.options[ s.selectedIndex ].value



    console.log(id_title)
    console.log(id_severity)
    console.log(id_description)
    sendSave()
    
}


function sendSave(){
    url = window.location.href
    url = url.split('/')
    var pk = url[url.length - 1];
    console.log(pk)
    $.ajax(
      {
          type:"GET",
          url: "save/",
          
          dataType: 'json',
          data:{
            pk: String(pk),
            id_title: String(id_title),
            id_severity: String(id_severity),
            id_description: String(id_description),

          },
          success: function(asdf) {
            let res = asdf.asdf
            console.log('finished')

  
        }
      })  
  }



