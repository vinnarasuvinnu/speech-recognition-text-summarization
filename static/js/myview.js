function changeText(cont1,cont2,speed){
	var Otext=cont1.text();
	var Ocontent=Otext.split("");

	var i=0;
	function show(){
		if(i<Ocontent.length){
			cont2.append(Ocontent[i]);
			i=i+1;
		};
	};
	var Otimer=setInterval(show,speed);
};
function cool(){



	$.ajax({
			method:"POST",
			url:"/fmean",
			data:"",
			success:function(data){
				$("#type").empty();
				$("#type").append(data);
				$('#mailcont').fadeIn(4000);
				$('#mailcont').fadeOut(4000);

			}
		});
};

function noidea(){

		$.ajax({
			method:"POST",
			url:"/fcont",
			data:"",
			success:function(data){

				$("#type").empty();
				$("#type").append(data);
				$('#mailmean').fadeIn(4000);
				$('#mailmean').fadeOut(4000);
			}
		});



}

$(document).ready(function(){
			swal({
				title:"<i>Important note</i>",
				html:"Please exploer the help button in the top left corner to know more about the website",
				confirmButtonText:"Please check",
			});
			var btn=$(this);
			theme="blue";
		
			$('#mailsent').hide();
			$('#mailnot').hide();
			$('#mailmean').hide();
			$('#mailcont').hide();
			$('#mailco').hide();

			$('#mike').hide();
			$('#vnot').hide();
			$('#tco').hide()

	$("#taptap").click(function(){
		changeText($("#helping"),$(".onebyone"),150);
		clearInterval(Otimer);
	});

	$("#tap").click(function recur(){
		//alert("you clicked me");
		$('#mike').show();

		$.ajax({
			type:"POST",
			url:"/fullcore",
			data:"",
			success:function(data){

			if(data=="stop"){
			swal({
				title:"<i>Note</i>",
				html:"Speech recognition is stoped",
				confirmButtonText:"Continue",
			});			
				$('#mike').hide();
				return false;

			}
			
			$("#type").append(data);
				recur();
			}



		});

	});

	$("#ttap").click(function simp(){
		//alert("you clicked me");
		$('#mike').show();
		$.ajax({
			type:"POST",
			url:"/simple",
			data:"",
			success:function(data){
				if(data=="exit exit"){
					swal({
				title:"<i>Note</i>",
				html:"Speech recognition is stoped",
				confirmButtonText:"Continue",
				});			
				$('#mike').hide();
				return false;

				}
				$("#type").append(data+" ");	
				simp();
				}
		});

	});




	$("#fcontent").click(function mean(){
		//alert("this find doc");
		$.ajax({
			method:"POST",
			url:"/fmean",
			data:"",
			success:function(data){
				$("#type").empty();
				$("#type").append(data);
				$('#mailcont').fadeIn(4000);
				$('#mailcont').fadeOut(4000);

			}
		});
	});


	$("#setdata").click(function(){
		//alert("this find doc");
		$.ajax({
			method:"POST",
			url:"/filecsv",
			data:"",
			success:function(data){
				$('#mailco').fadeIn(4000);
				$('#mailco').fadeOut(4000);

			}
		});
	});



	$("#sdata").click(function(){
		//alert("this find doc");
		$.ajax({
			method:"POST",
			url:"/sumfile",
			data:"",
			success:function(data){
				$('#mailco').fadeIn(4000);
				$('#mailco').fadeOut(4000);

			}
		});
	});


	$("#tspeech").click(function(){
		//alert("this find doc");
		$.ajax({
			method:"POST",
			url:"/t2speech",
			data:"",
			success:function(data){
				$('#tco').fadeIn(4000);
				$('#tco').fadeOut(4000);

			}
		});
	});



	$("#fmeaning").click(function cont(){
		//alert("clicked meaning");
		$.ajax({
			method:"POST",
			url:"/fcont",
			data:"",
			success:function(data){

				$("#type").empty();
				$("#type").append(data);
				$('#mailmean').fadeIn(4000);
				$('#mailmean').fadeOut(4000);
			}
		});
	});

	$("#clearfile").click(function(){
		$("#type").empty();
		$('#mike').hide();
	});


	$('#summ').click(function(){
		//alert("no problem");
		var limit=prompt("How many line of summarization document you want");
		$.ajax({
			method:"POST",
			url:"/ssum",
			data:'vval='+limit,
			success:function(data){
				$("#type").empty();
				$("#type").append(data);
			}
		});

	});

	$('#mailme').click(function(){
		var nmatch=new RegExp("^[a-zA-z]+$");
		var mmatch=new RegExp("^[a-z0-9_.]+@[a-z_.]+.[a-z_]{2,3}$");
		var name=prompt("Enter your name:")
		while(name == null || !name.match(nmatch) ){
			name=prompt("please Enter a valid name:");
		}
		var mail=prompt("Enter your mail:");
		while(mail==null || !mail.match(mmatch)){
			mail=prompt("please Enter a valid Email:");
		}
		$.ajax({
			method:"POST",
			url:"/smail",
			data:'fname='+name+'&fmail='+mail,
			success:function(res){
				if(res==1){
				$('#mailsent').fadeIn(4000);
				$('#mailsent').fadeOut(4000);
			}
			else{
				$('#mailnot').fadeIn(4000);
				$('#mailnot').fadeOut(4000);
			}

			}
		});

	});


	$('#clearos').click(function(){
		$.ajax({
			method:"POST",
			url:"/fileclear",
			date:"",
			success:function(){
		swal({
				title:"<i>Note</i>",
				html:"Your file is cleared in os",
				confirmButtonText:"Continue",
			});			
			}
		});
	})


});