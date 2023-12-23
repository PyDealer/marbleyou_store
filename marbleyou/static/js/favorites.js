function addToFavorites(event) {
  event.preventDefault();
  var form = event.target;
  var type = form.querySelector('input[name="type"]').value;
  var stoneId = form.querySelector('input[name="stone_id"]').getAttribute('data-stone-id');
  var url = form.querySelector('input[name="stone_id"]').getAttribute('data-url');
  var favorites_button = form.querySelector('input[name="favorites_button"]').getAttribute('id');
  var favoritesButton = document.getElementById(favorites_button);
  var xhr = new XMLHttpRequest();
  xhr.open("POST", url);
  xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
  var csrfToken = form.querySelector('input[name="csrfmiddlewaretoken"]').value;
  xhr.onreadystatechange = function() {
    if (xhr.readyState === XMLHttpRequest.DONE) {
      if (xhr.status === 200) {
        //var sessionFavorites = document.getElementById("session-favorites");
        //var sessionFavoritesList = document.getElementById("session-list");
        var sessionFavoritesCount = document.getElementById("count_favorites");
        var sessionModalList = document.getElementById("modal_list");
        var response = JSON.parse(xhr.responseText);
        //var favoritesHTML = JSON.stringify(response.data);
        //sessionFavorites.innerHTML = favoritesHTML;
        //sessionFavoritesList.innerHTML = favoritesHTML;
        sessionFavoritesCount.innerHTML = response.count;
        if (response.status){
          favoritesButton.src = "/static/img/icons/Heart_fill.svg";
        }else{
          favoritesButton.src = "/static/img/icons/Heart.svg";
        };
        //var modallistHTML = JSON.stringify(response.modal_list);
        sessionModalList.innerHTML = response.modal_list
        //sessionFavorites.innerHTML = response.data;
      }
    }
  };
  xhr.setRequestHeader("X-CSRFToken", csrfToken);
  xhr.send("type=" + encodeURIComponent(type) + "&stone_id=" + encodeURIComponent(stoneId) + "&url_from=" + encodeURIComponent(url));
}

function clearFavorites(event) {
  event.preventDefault();
  var form = event.target;
  var url = form.querySelector('input[name="url"]').value;
  var sessionFavoritesCount = document.getElementById("count_favorites");
  var sessionModalList = document.getElementById("modal_list");
  var xhr = new XMLHttpRequest();
  xhr.open("POST", url);
  xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
  var csrfToken = form.querySelector('input[name="csrfmiddlewaretoken"]').value;
  xhr.onreadystatechange = function() {
    if (xhr.readyState === XMLHttpRequest.DONE) {
      if (xhr.status === 200) {
        var response = JSON.parse(xhr.responseText);
        var stoneIds = response.stone_ids
        for (var i = 0; i < stoneIds.length; i++){
          var stoneId = document.getElementById(stoneIds[i]+"_button");
          var favoritesButton = document.getElementById(stoneId.id);
          favoritesButton.src = "/static/img/icons/Heart.svg";
        };
        sessionFavoritesCount.innerHTML = 0;
        sessionModalList.innerHTML = response.modal_list
      }
    }
  };
  xhr.setRequestHeader("X-CSRFToken", csrfToken);
  xhr.send();
}