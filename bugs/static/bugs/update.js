





function postComment() {

	comment_text = document.getElementById( "id_comment_i").value;
	console.log(comment_text)

	url = window.location.href
	url = url.split('/')
	var pk = url[url.length - 1];
	console.log(pk)
	$.ajax(
	{
		type:"GET",
		url: "comment/",

		dataType: 'json',
		data:{
			pk: String(pk),
			comment: String(comment_text),
		},
		success: function(asdf) {
			let res = asdf.asdf
			location.reload();


		}
	})









}


async function addGroup(){
	userInput = document.getElementById( "add_groupI").value;
	console.log(userInput)
	document.getElementById( "add_groupD").style.border = '1px solid red';

	await sleep(1000);
	document.getElementById( "add_groupD").style.border = '0px solid #1a1a1a';;
}
async function addUser() {
	userInput = document.getElementById( "add_userI").value;
	console.log(userInput)
	url = window.location.href
	url = url.split('/')
	var pk = url[url.length - 1];
	console.log(pk)

		$.ajax(
		{
			type:"GET",
			url: "adduser/",

			dataType: 'json',
			data:{
				pk: String(pk),
				userInput: String(userInput),



			},
			success: function(asdf) {
				if (asdf.asdf){
					document.getElementById( "add_userD").style.border = '1px solid green';
					location.reload()

				}else{
					document.getElementById( "add_userD").style.border = '1px solid red';

				}

			}
		})  

	await sleep(1000);
	document.getElementById( "add_userD").style.border = '0px solid #1a1a1a';;
}


function supdate(){

	var s = document.getElementById( "id_severity" );
	id_severity = s.options[ s.selectedIndex ].value
	if(id_severity =='Low'){
		s.style.color= '#A0A0A0';
		s.style.border= '1px solid #A0A0A0';
	}
	if(id_severity =='High'){
		s.style.color= '#17a2b8';
		s.style.border= '1px solid #17a2b8';
	}
	if(id_severity =='Medium'){
		s.style.color= 'white';
		s.style.border= '1px solid white';
	}
	console.log(id_severity)

}
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
saveLoop()
async function saveLoop(){
	let hbhb = true
	while(hbhb = true){
		await sleep(1000);
		//console.log('saving status....')
		save()

	}
}
function save(){


	id_title = document.getElementById("id_title").value
	id_description = document.getElementById("id_description").value
	var s = document.getElementById( "id_severity" );
	id_severity = s.options[ s.selectedIndex ].value



	var userStatus = []   




	for(x = 0;x<=users.length-2;x+=1){ 

		id='check_'+users[x]
		check = document.getElementById(id).checked
		userStatus.push([users[x],check])



	}






	sendSave(userStatus)

}


function sendSave(userStatus){
	url = window.location.href
	url = url.split('/')
	var pk = url[url.length - 1];
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
			bugUsers: String(userStatus),


		},
		success: function(asdf) {
			let res = asdf.asdf
			console.log('finished')


		}
	})  
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}


