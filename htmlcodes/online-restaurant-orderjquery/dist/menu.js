// Sticky Navigation Menu JS Code
let nav = document.querySelector("nav");
let scrollBtn = document.querySelector(".scroll-button a");
console.log(scrollBtn);
let val;
window.onscroll = function() {
  if(document.documentElement.scrollTop > 20){
    nav.classList.add("sticky");
    scrollBtn.style.display = "block";
  }else{
    nav.classList.remove("sticky");
    scrollBtn.style.display = "none";
  }

}





$(document).ready(function() {
  

	$( "a" ).click(function( event ) {
  		event.preventDefault();
	});

	var numOfOrders = 0;
	$(".num").text(numOfOrders);

	// hide dialogs on start
	$("#thanksMessage, #checkOrderCholeBhature, #checkOrderPavBhaji, #checkOrderChowmein, #checkOrderMacaroni, #checkOrderPasta, #checkOrderChilliPotato, #checkOrderFrenchFries, #checkOrderChholeChawal, #checkOrderRajmaChawal, #checkOrderColdCoffee, #checkOrderChocolateShake, #checkOrderFrooti, #finishOrderDialog").hide();

	// open dialog on click
	$("#addToCartCholeBhature").on("click", function () {
		$("#checkOrderCholeBhature").dialog({
				hide: "blind",
            	show : "blind",
            	width: "400px",
              closeText: "X"});
	})

	$("#addToCartPavBhaji").on("click", function () {
		$("#checkOrderPavBhaji").dialog({
				hide: "blind",
            	show : "blind",
            	width: "400px",
              closeText: "X"});
	})

	$("#addToCartChowmein").on("click", function () {
		$("#checkOrderChowmein").dialog({
				hide: "blind",
            	show : "blind",
            	width: "400px",
              closeText: "X"});
	})

	$("#addToCartMacaroni").on("click", function () {
		$("#checkOrderMacaroni").dialog({
				hide: "blind",
            	show : "blind",
            	width: "400px",
              closeText: "X"});
	})

	$("#addToCartPasta").on("click", function () {
		$("#checkOrderPasta").dialog({
				hide: "blind",
            	show : "blind",
            	width: "400px",
              closeText: "X"});
	})

	$("#addToCartChilliPotato").on("click", function () {
		$("#checkOrderChilliPotato").dialog({
				hide: "blind",
            	show : "blind",
            	width: "400px",
              closeText: "X"});
	})

	$("#addToCartFrenchFries").on("click", function () {
		$("#checkOrderFrenchFries").dialog({
				hide: "blind",
            	show : "blind",
            	width: "400px",
              closeText: "X"});
	})

	$("#addToCartChholeChawal").on("click", function () {
		$("#checkOrderChholeChawal").dialog({
				hide: "blind",
            	show : "blind",
            	width: "400px",
              closeText: "X"});
	})

	$("#addToCartRajmaChawal").on("click", function () {
		$("#checkOrderRajmaChawal").dialog({
				hide: "blind",
            	show : "blind",
            	width: "400px",
              closeText: "X"});
	})

	$("#addToCartColdCoffee").on("click", function () {
		$("#checkOrderColdCoffee").dialog({
				hide: "blind",
            	show : "blind",
            	width: "400px",
              closeText: "X"});
	})

	$("#addToCartChocolateShake").on("click", function () {
		$("#checkOrderChocolateShake").dialog({
				hide: "blind",
            	show : "blind",
            	width: "400px",
              closeText: "X"});
	})

	$("#addToCartFrooti").on("click", function () {
		$("#checkOrderFrooti").dialog({
				hide: "blind",
            	show : "blind",
            	width: "400px",
              closeText: "X"});
	})

	// increase/decrease the price of order if an item is added/removed
	function checkboxChange(x) {
		var priceDialog = 0;
		$("#recipe"+x).children("li").children("input").each(function () {
			if($(this).is(":checked")){
				priceDialog+=10;
			}
				$("#totalDialog"+x+">span").text(priceDialog);
			$(this).change(function () {
				if ($(this).is(":checked")) {
					priceDialog += 10;
					console.log(priceDialog);
					$("#totalDialog"+x+">span").text(priceDialog);
				}else{
					priceDialog -= 10;
					$("#totalDialog"+x+">span").text(priceDialog);
				}
			})
		});
	}

	$('#recipe1').children('li').click(checkboxChange(1));
	$('#recipe2').children('li').click(checkboxChange(2));
	$('#recipe3').children('li').click(checkboxChange(3));
	$('#recipe4').children('li').click(checkboxChange(4));
	$('#recipe5').children('li').click(checkboxChange(5));
	$('#recipe6').children('li').click(checkboxChange(6));
	$('#recipe7').children('li').click(checkboxChange(7));
	$('#recipe8').children('li').click(checkboxChange(8));
	$('#recipe9').children('li').click(checkboxChange(9));
	$('#recipe10').children('li').click(checkboxChange(10));
	$('#recipe11').children('li').click(checkboxChange(11));
	$('#recipe12').children('li').click(checkboxChange(12));

	$(".addIngredient").on("click", function () {
		// Creates input field and two buttons for adding an ingrediant that's not on the list
		var inputIng = '<input type="text" id="newIngredient">';
		var confirmInput = '<a class="btnStyle3 btnStyle confirmInput">Rs;</a>';
		var cancelInput = '<a class="btnStyle3 btnStyle cancelInput">Rs;</a>';
		var inputWrap = '<div class="addIngredientWrap">' + inputIng + confirmInput + cancelInput + '</div>'
		$(this).parent().children("ul").after(inputWrap);
    $("#newIngredient").focus();
    $("#newIngredient").attr("placeholder", "separate ingredients with a comma");

		// Confirm button adds the new ingrediant to the list of ingrediants
		$(".addIngredientWrap > .confirmInput").on("click", function () {
			if ($("#newIngredient").val() != "") {
        //split takes the value of the input and splits it into separate array elements after every comma
				var newIngredient = ($(".addIngredientWrap input").val()).split(",");
				var newCheckbox = '<input type="checkbox" checked>';
        
        for (var i = 0; i < newIngredient.length; i++){
         $(this).parent().siblings("ul").append("<li>" + newCheckbox + newIngredient[i] + "  (+10Rs)</li>");
        }
				

				$('#recipe1').children('li').click(checkboxChange(1));
				$('#recipe2').children('li').click(checkboxChange(2));
				$('#recipe3').children('li').click(checkboxChange(3));
				$('#recipe4').children('li').click(checkboxChange(4));
				$('#recipe5').children('li').click(checkboxChange(5));
				$('#recipe6').children('li').click(checkboxChange(6));
				$('#recipe7').children('li').click(checkboxChange(7));
				$('#recipe8').children('li').click(checkboxChange(8));
				$('#recipe9').children('li').click(checkboxChange(9));
				$('#recipe10').children('li').click(checkboxChange(10));
				$('#recipe11').children('li').click(checkboxChange(11));
				$('#recipe12').children('li').click(checkboxChange(12));

				$(this).parent().remove();
			}else{
				$("#newIngredient").attr("placeholder", "Please add ingrediant");
			}
		});
		// Remove button hides the input
		$(".addIngredientWrap > .cancelInput").on("click", function () {
			$(this).parent().remove();
		})
	})// add ingredient button

	$(".listOver").on("click", function () {
		var orderName = '<h3 class="orderName"><span>' + $(this).parent().siblings(".ui-dialog-titlebar").children("span").text() + '</span><a class="delBtn">Rs;</a>' +'</h3>';
		var orderIngredients = '<ul class="orderIngredients"></ul>';
		var orderPrice = '<h3 class="orderPrice"><span>' + $(this).parent().children(".totalDialog").children("span").text() + '</span>Rs<h3>'
		var horisontalLine = '<hr>';
		$(".cart").children("#listOfOrders").append("<li>" + orderName + orderIngredients + orderPrice + horisontalLine + "</li>");

		$(this).parent().children("ul").children().children("input:checked").each(function () {
			var selectedIngredient = $(this).parent().text();
			$(".orderIngredients").last().append("<li>" + selectedIngredient + "</li>");
		})

		// opens the cart side menu
		if ($('#cartToggle').prop('checked')) {
			$("#cartToggle").prop("checked", true);
		}else{
			$("#cartToggle").prop("checked", true);
		}

		$(this).parent(".ui-dialog-content").dialog("close");

		numOfOrders = $("#listOfOrders").children().length;
		$(".num").text(numOfOrders);

		// display total price in cart orders
		var totalOrderPrice = 0;
		$("#listOfOrders").children("li").children(".orderPrice").children("span").each(function () {
			var price = parseFloat($(this).text());
			totalOrderPrice += price;
			$(".cart > h3 > span").text(totalOrderPrice + "Rs");
		});

		// remove order from cart
		$(".delBtn").on("click", function () {
			var removePrice = $(this).parent().parent().children(".orderPrice").children("span").text();
			totalOrderPrice -= removePrice;
			$(".cart > h3 > span").text(totalOrderPrice + "Rs");

			$(this).parents("li").remove();
			numOfOrders = $("#listOfOrders").children().length;
			$(".num").text(numOfOrders);
		})
	}); // List over (done button)

	$(".finishOrder").on("click", function () {
     $("#finalOrderList > ol").children().remove();
		$(".orderName").children("span").each(function(){
			var finalOrder = '<li>' + $(this).text() + '</li>';
			$("#finalOrderList > ol").append(finalOrder);
		})

		$("#finishOrderDialog").dialog({
			hide: "blind",
	    	show : "blind",
	    	width: "500px",
        closeText: "X"
	    });
	})

	$(".order").on("click", function () {
		var name = $("#buyerName").val();
		var number = $("#buyerNumber").val();
		var table = $("#buyerTable").val();

		if (name != "" && number != "" && table != "") {
			$("#finishOrderDialog").dialog("close");
			$("#buyerInfo").children("p").remove();
			$("#thanksMessage").dialog({
				hide: "blind",
		    	show : "blind",
		    	width: "400px"
		    });
		    setTimeout(function(){
		    	$("#thanksMessage").dialog("close");
		    }, 3000);
		}else{
			$("#buyerInfo").append('<p>Fill up all the inputs</p>');
		}
	})

})