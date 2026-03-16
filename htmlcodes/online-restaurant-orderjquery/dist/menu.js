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
	// Theme: apply saved preference (default light)
	var saved = localStorage.getItem("cafeholic-theme");
	if (saved === "dark") document.body.setAttribute("data-theme", "dark");
	else document.body.removeAttribute("data-theme");

	$("#themeToggle").on("click", function () {
		var isDark = document.body.getAttribute("data-theme") === "dark";
		if (isDark) {
			document.body.removeAttribute("data-theme");
			localStorage.setItem("cafeholic-theme", "light");
		} else {
			document.body.setAttribute("data-theme", "dark");
			localStorage.setItem("cafeholic-theme", "dark");
		}
	});

	// Allow nav/logo/external links to navigate; prevent default for in-page action links (cart, dialogs)
	$("a").click(function (event) {
		var href = $(this).attr("href") || "";
		if (href.indexOf("index.html") >= 0 || href.indexOf("login.html") >= 0 || href.indexOf("http") === 0) return;
		event.preventDefault();
	});

	var numOfOrders = 0;
	$(".num").text(numOfOrders);

	var API_BASE = window.CAFEHOLIC_API_BASE || "http://localhost:3001";
	var AUTH_KEY = "cafeholic-auth";
	function getStoredAuth() {
		try { return JSON.parse(localStorage.getItem(AUTH_KEY) || "null"); } catch (e) { return null; }
	}
	function getWallet() {
		var auth = getStoredAuth();
		if (auth && auth.user && typeof auth.user.walletBalance === "number") return auth.user.walletBalance;
		return 0;
	}
	function setWallet(val) {
		$("#walletBalance").text(Math.round(val));
		var auth = getStoredAuth();
		if (auth && auth.user) {
			auth.user.walletBalance = val;
			localStorage.setItem(AUTH_KEY, JSON.stringify(auth));
		}
	}
	function updateNavAndCartWallet() {
		var auth = getStoredAuth();
		if (auth && auth.token) {
			$("#navLogin").hide();
			$("#navWallet").css("display", "inline-flex");
			$("#navWalletBalance").text(Math.round(auth.user.walletBalance || 0));
			$("#walletBalance").text(Math.round(auth.user.walletBalance || 0));
			$.ajax({
				url: API_BASE + "/api/wallet",
				headers: { "Authorization": "Bearer " + auth.token },
				success: function (data) {
					var bal = data.balance || 0;
					$("#walletBalance").text(Math.round(bal));
					$("#navWalletBalance").text(Math.round(bal));
					if (auth.user) auth.user.walletBalance = bal;
					localStorage.setItem(AUTH_KEY, JSON.stringify(auth));
				}
			});
		} else {
			$("#navWallet").hide();
			$("#navLogin").css("display", "inline-block");
			$("#walletBalance").text("—");
		}
	}
	updateNavAndCartWallet();

	// Image fallback: show placeholder when menu photo is missing
	var placeholderMenu = "../../photos/placeholder.svg";
	$(".recipe img").on("error", function () {
		this.onerror = null;
		$(this).attr("src", placeholderMenu);
	}).each(function () {
		if (this.complete && this.naturalWidth === 0) $(this).attr("src", placeholderMenu);
	});

	// hide dialogs on start
	$("#thanksMessage, #finishOrderDialog").hide();
		$("[id^='checkOrder']").hide();

	// open dialog on click and init total
	function openDialog(selector) {
		$(selector).dialog({
			hide: "blind",
			show: "blind",
			width: "450px",
			closeText: "X",
			open: function () {
				var num = $(this).data("recipe-num");
				if (num !== undefined) updateTotal("totalDialog" + num);
			}
		});
	}
	$(document).on("click", "[id^='addToCart']", function () {
		var checkId = "checkOrder" + this.id.replace("addToCart", "");
		openDialog("#" + checkId);
	});

	// Update total for a dialog: base (portion) + 10 per checked ingredient
	function updateTotal(dialogId) {
		var recipeNum = dialogId.replace("totalDialog", "");
		var $dialog = $("#" + dialogId).closest("[id^='checkOrder']");
		var basePrice = parseInt($dialog.find("input[type='radio']:checked").val(), 10) || 20;
		var extras = 0;
		$("#recipe" + recipeNum).children("li").children("input").each(function () {
			if ($(this).is(":checked")) extras += 10;
		});
		var total = basePrice + extras;
		$("#" + dialogId).find(".totalAmount").text(total);
	}

	function setupRecipeHandlers() {
		for (var x = 1; x <= 62; x++) {
			(function (i) {
				var $recipe = $("#recipe" + i);
				if (!$recipe.length) return;
				// Portion change
				$recipe.closest("[id^='checkOrder']").find("input[type='radio']").off("change.portion").on("change.portion", function () {
					updateTotal("totalDialog" + i);
				});
				// Ingredient checkbox change
				$recipe.find("input[type='checkbox']").off("change.ingredient").on("change.ingredient", function () {
					updateTotal("totalDialog" + i);
				});
				// Initial total
				updateTotal("totalDialog" + i);
			})(x);
		}
	}

	setupRecipeHandlers();

	$(".addIngredient").on("click", function () {
		// Creates input field and two buttons for adding an ingrediant that's not on the list
		var inputIng = '<input type="text" id="newIngredient">';
		var confirmInput = '<a class="btnStyle3 btnStyle confirmInput">Add</a>';
		var cancelInput = '<a class="btnStyle3 btnStyle cancelInput">Cancel</a>';
		var inputWrap = '<div class="addIngredientWrap">' + inputIng + confirmInput + cancelInput + '</div>'
		$(this).parent().children("ul").after(inputWrap);
    $("#newIngredient").focus();
    $("#newIngredient").attr("placeholder", "separate ingredients with a comma");

		// Confirm button adds the new ingrediant to the list of ingrediants
		$(".addIngredientWrap > .confirmInput").on("click", function () {
			if ($("#newIngredient").val() != "") {
				var newIngredient = ($(".addIngredientWrap input").val()).split(",");
				var newCheckbox = '<input type="checkbox" checked>';
				for (var i = 0; i < newIngredient.length; i++) {
					$(this).parent().siblings("ul").append("<li>" + newCheckbox + newIngredient[i].trim() + "  (+10Rs)</li>");
				}
				setupRecipeHandlers();
				$(this).parent().remove();
			} else {
				$("#newIngredient").attr("placeholder", "Please add ingrediant");
			}
		});
		// Remove button hides the input
		$(".addIngredientWrap > .cancelInput").on("click", function () {
			$(this).parent().remove();
		})
	})// add ingredient button

	$(".listOver").on("click", function () {
		var totalAmount = $(this).parent().children(".totalDialog").find(".totalAmount").text();
		var priceNum = parseFloat(totalAmount) || 0;
		var orderName = '<h3 class="orderName"><span>' + $(this).parent().siblings(".ui-dialog-titlebar").children("span").text() + '</span><a class="delBtn">×</a></h3>';
		var orderIngredients = '<ul class="orderIngredients"></ul>';
		var orderPrice = '<h3 class="orderPrice"><span>' + priceNum + '</span> ₹</h3>';
		var horisontalLine = '<hr>';
		$(".cart").children("#listOfOrders").append("<li>" + orderName + orderIngredients + orderPrice + horisontalLine + "</li>");

		$(this).parent().children("ul").children().children("input:checked").each(function () {
			var selectedIngredient = $(this).parent().text();
			$(".orderIngredients").last().append("<li>" + selectedIngredient + "</li>");
		});

		$("#cartToggle").prop("checked", true);
		$(this).parent(".ui-dialog-content").dialog("close");

		numOfOrders = $("#listOfOrders").children().length;
		$(".num").text(numOfOrders);

		// Recalculate cart total from all order prices
		var totalOrderPrice = 0;
		$("#listOfOrders").children("li").children(".orderPrice").children("span").each(function () {
			totalOrderPrice += parseFloat($(this).text()) || 0;
		});
		$(".cart > h3 > span").text(totalOrderPrice + " ₹");

		// Remove order from cart
		$(".delBtn").on("click", function () {
			$(this).parents("li").remove();
			numOfOrders = $("#listOfOrders").children().length;
			$(".num").text(numOfOrders);
			var totalOrderPrice = 0;
			$("#listOfOrders").children("li").children(".orderPrice").children("span").each(function () {
				totalOrderPrice += parseFloat($(this).text()) || 0;
			});
			$(".cart > h3 > span").text(totalOrderPrice + " ₹");
		});
	}); // List over (done button)

	$(".finishOrder").on("click", function () {
		$("#finalOrderList > ol").children().remove();
		$(".orderName").children("span").each(function(){
			var finalOrder = '<li>' + $(this).text() + '</li>';
			$("#finalOrderList > ol").append(finalOrder);
		});
		var totalOrderPrice = 0;
		$("#listOfOrders").children("li").children(".orderPrice").children("span").each(function () {
			totalOrderPrice += parseFloat($(this).text()) || 0;
		});
		$("#dialogOrderTotal").text(totalOrderPrice);
		$("#finishOrderDialog").dialog({
			hide: "blind",
			show: "blind",
			width: "500px",
			closeText: "X"
		});
	});

	$(".order").on("click", function () {
		var name = $("#buyerName").val();
		var number = $("#buyerNumber").val();
		var table = $("#buyerTable").val();
		$("#buyerInfo").children("p").remove();

		if (name === "" || number === "" || table === "") {
			$("#buyerInfo").append('<p>Fill up all the inputs</p>');
			return;
		}

		var auth = getStoredAuth();
		if (!auth || !auth.token) {
			$("#buyerInfo").append('<p>Please <a href="../../login.html">login</a> to place an order.</p>');
			localStorage.setItem("cafeholic-return-url", window.location.href);
			return;
		}

		var totalOrderPrice = parseFloat($("#dialogOrderTotal").text()) || 0;
		var paymentMethod = $("input[name=paymentMethod]:checked").val() || "cash";
		var payViaWallet = paymentMethod === "wallet";

		if (payViaWallet) {
			var balance = getWallet();
			if (balance < totalOrderPrice) {
				$("#buyerInfo").append('<p>Insufficient wallet balance. Need ₹' + totalOrderPrice + ', you have ₹' + Math.round(balance) + '.</p>');
				return;
			}
		}

		var items = [];
		$(".orderName").children("span").each(function () { items.push($(this).text()); });

		$.ajax({
			url: API_BASE + "/api/orders",
			method: "POST",
			headers: { "Content-Type": "application/json", "Authorization": "Bearer " + auth.token },
			data: JSON.stringify({
				items: items,
				total: totalOrderPrice,
				paymentMethod: paymentMethod,
				buyerName: name,
				buyerPhone: number,
				buyerTable: table
			}),
			success: function (data) {
				if (data.walletBalance !== undefined) setWallet(data.walletBalance);
				updateNavAndCartWallet();
				$("#finishOrderDialog").dialog("close");
				$("#listOfOrders").empty();
				$(".cart > h3 > span").text("0 ₹");
				$(".num").text("0");
				$("#cartToggle").prop("checked", false);
				$("#buyerName").val("");
				$("#buyerNumber").val("");
				$("#buyerTable").val("");
				$("#thanksMessage").dialog({ hide: "blind", show: "blind", width: "400px" });
				setTimeout(function () { $("#thanksMessage").dialog("close"); }, 3000);
			},
			error: function (xhr) {
				var msg = (xhr.responseJSON && xhr.responseJSON.error) || "Order failed. Try again.";
				$("#buyerInfo").append('<p>' + msg + '</p>');
			}
		});
	});

})